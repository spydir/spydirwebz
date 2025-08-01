import json
import pytest
from logic_validator import validate_puzzle

def test_impossible_unique():
    # Uses the example puzzle in /example
    with open("example/web_impossible.json") as f:
        puzzle = json.load(f)
    result = validate_puzzle(puzzle)
    assert result['status'] == 'valid'
    assert result['solution']['actor'] == "FluxSignal"

def test_ambiguous_fails():
    puzzle = {
        "actors": ["A", "B", "C"],
        "vectors": ["X", "Y", "Z"],
        "assets": ["S1", "S2", "S3"],
        "stolen_data": ["D1", "D2", "D3"],
        "solution": {"actor": "A", "vector": "X", "asset": "S2", "stolen_data": "D1"},
        "clues": [
            {"text": "A did not use Y.", "type": "negation"},
            {"text": "B did not use Z.", "type": "negation"},
            {"text": "C did not use X.", "type": "negation"}
            # No confirmation clue: ambiguous triplets
        ]
    }
    result = validate_puzzle(puzzle)
    assert result['status'] == 'ambiguous'
