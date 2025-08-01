import json
from logic_validator import validate_puzzle

def test_easy_valid():
    puzzle = {
        "actors": ["A", "B", "C"],
        "vectors": ["X", "Y", "Z"],
        "assets": ["S1", "S2", "S3"],
        "stolen_data": ["D1", "D2", "D3"],
        "solution": {"actor": "A", "vector": "X", "asset": "S2", "stolen_data": "D1"},
        "clues": [
            {"text": "A used X on S2.", "type": "affirmative"},
            {"text": "B did not use Y.", "type": "negation"},
            {"text": "The vector X was used against S2.", "type": "affirmative"},
            {"text": "Only attacks on S2 resulted in D1.", "type": "data-inference"}
        ]
    }
    result = validate_puzzle(puzzle)
    assert result['status'] == 'valid'
    assert result['solution']['actor'] == "A"
