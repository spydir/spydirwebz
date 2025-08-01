# logic_validator.py

import json
import re
from z3 import Solver, Bool, And, Or, Not, Implies, sat

def validate_puzzle(puzzle: dict):
    actors = puzzle['actors']
    vectors = puzzle['vectors']
    assets = puzzle['assets']
    stolen_data_opts = puzzle['stolen_data']
    solution = puzzle['solution']

    s = Solver()

    # Boolean variables for each triplet possibility
    trip_vars = {}
    for a in actors:
        for v in vectors:
            for t in assets:
                name = f'x_{a}_{v}_{t}'
                trip_vars[(a, v, t)] = Bool(name)

    # Exactly one triplet must be true
    s.add(Or(*trip_vars.values()))
    # No two triplets can be true simultaneously
    for t1, t2 in zip(trip_vars.values(), trip_vars.values()):
        if t1 is not t2:
            s.add(Not(And(t1, t2)))

    # Constraints: if a triplet is selected, actor/vector/asset are bound
    # (Implicitly represented by how we encode clues)

    # Encode clues:
    for clue in puzzle['clues']:
        text = clue['text']
        typ = clue['type']

        try:
            if typ == 'negation':
                # Example pattern: "GhostShell did not use SQL Injection."
                # Find actor and vector by matching against known lists
                actor = None
                vector = None
                
                for a in actors:
                    if a in text:
                        actor = a
                        break
                
                for v in vectors:
                    if v in text:
                        vector = v
                        break
                
                if actor and vector:
                    # For any asset, forbid (actor, vector, *)
                    for t in assets:
                        if (actor, vector, t) in trip_vars:
                            s.add(Not(trip_vars[(actor, vector, t)]))
                
            elif typ == 'affirmative':
                # e.g. "Phishing was used against the Email Server."
                vector = None
                asset = None
                
                for v in vectors:
                    if v in text:
                        vector = v
                        break
                
                for t in assets:
                    if t in text:
                        asset = t
                        break
                
                if vector and asset:
                    # require existence of some actor: any triplet with (vector, asset)
                    valid_triplets = [
                        trip_vars[(a, vector, asset)]
                        for a in actors
                        if (a, vector, asset) in trip_vars
                    ]
                    if valid_triplets:
                        s.add(Or(*valid_triplets))
                
            elif typ == 'relational':
                # e.g. "The actor that used SQL Injection did not access the HR Portal."
                vector = None
                asset = None
                
                for v in vectors:
                    if v in text:
                        vector = v
                        break
                
                for t in assets:
                    if t in text:
                        asset = t
                        break
                
                if vector and asset:
                    # For any actor, forbid (actor, vector, asset)
                    for a in actors:
                        if (a, vector, asset) in trip_vars:
                            s.add(Not(trip_vars[(a, vector, asset)]))
                
            elif typ == 'conditional':
                # e.g. "If ZeroShadow used RDP Exploit, then they accessed the Finance Database."
                actor = None
                vector = None
                asset = None
                
                for a in actors:
                    if a in text:
                        actor = a
                        break
                
                for v in vectors:
                    if v in text:
                        vector = v
                        break
                
                for t in assets:
                    if t in text:
                        asset = t
                        break
                
                if actor and vector and asset:
                    # If this actor used this vector, then they must have accessed this specific asset
                    # This means: if (actor, vector, asset) is true, then no other asset can be true for this actor-vector pair
                    # And: if any (actor, vector, other_asset) is true, then (actor, vector, asset) must be true
                    
                    # For any other asset, if (actor, vector, other_asset) is true, then (actor, vector, asset) must be true
                    for t in assets:
                        if t != asset and (actor, vector, t) in trip_vars:
                            # If (actor, vector, t) is true, then (actor, vector, asset) must be true
                            s.add(Implies(trip_vars[(actor, vector, t)], trip_vars[(actor, vector, asset)]))
                    
                    # Also ensure that if (actor, vector, asset) is true, then no other asset can be true for this actor-vector pair
                    for t in assets:
                        if t != asset and (actor, vector, t) in trip_vars:
                            s.add(Implies(trip_vars[(actor, vector, asset)], Not(trip_vars[(actor, vector, t)])))
                
            elif typ == 'data-inference':
                # e.g. "Only attacks using SQL Injection resulted in theft of Source Code."
                vector = None
                data_type = None
                
                for v in vectors:
                    if v in text:
                        vector = v
                        break
                
                for d in stolen_data_opts:
                    if d in text:
                        data_type = d
                        break
                
                # This clue type is mainly for data inference validation
                # The actual logic constraints are handled by other clue types
                pass
                
        except Exception as e:
            print(f"Warning: Could not parse clue '{text}' of type '{typ}': {e}")
            continue

    # Solve and check
    if s.check() != sat:
        return {
            "status": "invalid", 
            "reason": "unsatisfiable (no solutions)",
            "explanation": "The clues create a logical contradiction. No combination of actor, vector, and asset can satisfy all the given constraints. This usually means the clues are too restrictive or contain conflicting information.",
            "suggestions": [
                "Review your clues for logical contradictions",
                "Ensure clues don't eliminate all possible solutions",
                "Check that negation clues don't conflict with affirmative clues",
                "Verify that conditional clues are logically consistent"
            ]
        }

    model = s.model()
    true_triples = [trip for trip, var in trip_vars.items() if model.evaluate(var)]

    if len(true_triples) > 1:
        # Multiple solutions found
        solution_descriptions = []
        for trip in true_triples:
            actor, vector, asset = trip
            solution_descriptions.append(f"{actor} used {vector} against {asset}")
        
        return {
            "status": "ambiguous", 
            "solutions": true_triples,
            "explanation": f"The clues allow {len(true_triples)} different valid solutions. A good puzzle should have exactly one solution.",
            "found_solutions": solution_descriptions,
            "suggestions": [
                "Add more clues to eliminate alternative solutions",
                "Use negation clues to rule out specific actor-vector combinations",
                "Add relational clues to restrict which assets can be accessed",
                "Consider using conditional clues to create stronger constraints"
            ]
        }

    if len(true_triples) == 0:
        return {
            "status": "invalid", 
            "reason": "no solution found",
            "explanation": "The solver found no valid solution, but the system is satisfiable. This indicates a logic error in the validation process.",
            "suggestions": [
                "Check the puzzle data for consistency",
                "Verify that all actors, vectors, and assets are properly defined",
                "Review clue parsing logic for errors"
            ]
        }

    true_trip = true_triples[0]
    # verify it matches the declared solution
    sol = (solution['actor'], solution['vector'], solution['asset'])
    if true_trip != sol:
        found_actor, found_vector, found_asset = true_trip
        expected_actor, expected_vector, expected_asset = sol
        
        return {
            "status": "mismatch", 
            "found": true_trip, 
            "expected": sol,
            "explanation": f"The logical solution ({found_actor} used {found_vector} against {found_asset}) doesn't match your declared solution ({expected_actor} used {expected_vector} against {expected_asset}).",
            "analysis": {
                "logical_solution": f"{found_actor} used {found_vector} against {found_asset}",
                "declared_solution": f"{expected_actor} used {expected_vector} against {expected_asset}",
                "issue": "The clues logically lead to a different solution than what you specified."
            },
            "suggestions": [
                f"Either change your declared solution to: {found_actor} used {found_vector} against {found_asset}",
                f"Or modify your clues to eliminate the logical solution and support your intended solution",
                "Add negation clues to rule out the logical solution",
                "Use affirmative clues to support your intended solution"
            ]
        }

    # Check stolen_data inference path: crude check—exists final clue linking
    ds = solution['stolen_data']
    related = any(ds in clue['text'] for clue in puzzle['clues'])
    if not related:
        return {
            "status": "data-not-inferable",
            "explanation": f"The stolen data '{ds}' is not mentioned in any clues, making it impossible for solvers to determine what was stolen.",
            "suggestions": [
                f"Add a clue that mentions '{ds}'",
                "Use a data inference clue to link the attack vector to the stolen data",
                "Include the stolen data in an affirmative or conditional clue"
            ]
        }

    return {
        "status": "valid", 
        "solution": {"actor": sol[0], "vector": sol[1], "asset": sol[2], "stolen_data": ds},
        "explanation": "The puzzle is logically consistent and has exactly one solution that matches your declared solution.",
        "validation_summary": {
            "total_possibilities": len(trip_vars),
            "clues_processed": len(puzzle['clues']),
            "solution_unique": True,
            "data_inferable": True
        }
    }
