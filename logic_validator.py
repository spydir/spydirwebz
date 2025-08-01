# logic_validator.py

import json
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

        # Parse basic patterns manually
        if typ == 'negation':
            # Example pattern: "GhostShell did not use SQL Injection."
            parts = text.split()
            if "did not use" in text:
                a = parts[0]
                v = parts[-1].strip('.')
                # For any asset, forbid (a, v, *)
                for t in assets:
                    s.add(Not(trip_vars[(a, v, t)]))
        elif typ == 'affirmative':
            # e.g. "Phishing was used against the Email Server."
            parts = text.split()
            v = parts[0]
            asset = parts[-1].strip('.')
            # require existence of some actor: any triplet with (v, asset)
            require = Or(*[
                trip_vars[(a, v, asset)]
                for a in actors
            ])
            s.add(require)
        elif typ == 'relational':
            # e.g. "The actor that used SQL Injection did not access the HR Portal."
            # Basic pattern: vector X → asset ≠ Y
            # (vector relation to asset)
            try:
                v = parts[5]
                asset = parts[-1].strip('.')
                for a in actors:
                    s.add(Not(trip_vars[(a, v, asset)]))
            except:
                pass
        elif typ == 'conditional':
            # e.g. "If ZeroShadow used RDP Exploit, then they accessed the Finance Database."
            parts = text.replace(',', '').split()
            if parts[0] == "If" and "then" in parts:
                a = parts[1]
                v = parts[3]
                asset = parts[-1].strip('.')
                for t in assets:
                    if t != asset:
                        s.add(Implies(trip_vars[(a, v, t)], False))
        # Add parsing for other types as needed (comparative, multi-clause, etc.)

    # Solve and check
    if s.check() != sat:
        return {"status": "invalid", "reason": "unsatisfiable (no solutions)"}

    model = s.model()
    true_triples = [trip for trip, var in trip_vars.items() if model.evaluate(var)]

    if len(true_triples) > 1:
        return {"status": "ambiguous", "solutions": true_triples}

    true_trip = true_triples[0]
    # verify it matches the declared solution
    sol = (solution['actor'], solution['vector'], solution['asset'])
    if true_trip != sol:
        return {"status": "mismatch", "found": true_trip, "expected": sol}

    # Check stolen_data inference path: crude check—exists final clue linking
    ds = solution['stolen_data']
    related = any(ds in clue['text'] for clue in puzzle['clues'])
    if not related:
        return {"status": "data-not-inferable"}

    return {"status": "valid", "solution": {"actor": sol[0], "vector": sol[1], "asset": sol[2], "stolen_data": ds}}
