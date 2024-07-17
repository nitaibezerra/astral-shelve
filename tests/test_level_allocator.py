from typing import Dict, List

import pytest

from astral_shelve.pdf_generator.repetition_bar_allocator import LevelAllocator


@pytest.mark.parametrize("input_str, expected_output", [
    ("1-2,3-4,1-4,2-3", [1, 1, 2, 3]),
    ("1-2,3-4,1-4,2-3,3-5", [1, 1, 2, 3, 4]),
    ("1-3,4-6,1-6,2-5", [1, 1, 2, 3]),
    ("1-2,2-3,3-4,4-5,5-6", [1, 2, 3, 4, 5]),
    ("1-5,2-6,3-7,4-8", [1, 2, 3, 4]),
    ("1-1,2-2,3-3", [1, 1, 1]),
    ("1-1,1-2,2-3", [1, 2, 3]),
    ("1-1,1-2,5-6", [1, 2, 1]),
])
def test_allocate_levels(input_str: str, expected_output: List[int]):
    allocator = LevelAllocator()
    assert allocator.allocate_levels(input_str) == expected_output


@pytest.mark.parametrize("input_str, expected_output", [
    ("1-2,3-4,1-4,2-3", [{'start': 1, 'end': 2, 'level': 1}, {'start': 3, 'end': 4, 'level': 1},
                         {'start': 1, 'end': 4, 'level': 2}, {'start': 2, 'end': 3, 'level': 3}]),
    ("1-2,3-4,1-4,2-3,3-5", [{'start': 1, 'end': 2, 'level': 1}, {'start': 3, 'end': 4, 'level': 1},
                             {'start': 1, 'end': 4, 'level': 2}, {'start': 2, 'end': 3, 'level': 3},
                             {'start': 3, 'end': 5, 'level': 4}]),
    ("1-3,4-6,1-6,2-5", [{'start': 1, 'end': 3, 'level': 1}, {'start': 4, 'end': 6, 'level': 1},
                         {'start': 1, 'end': 6, 'level': 2}, {'start': 2, 'end': 5, 'level': 3}]),
    ("1-2,2-3,3-4,4-5,5-6", [{'start': 1, 'end': 2, 'level': 1}, {'start': 2, 'end': 3, 'level': 2},
                             {'start': 3, 'end': 4, 'level': 3}, {'start': 4, 'end': 5, 'level': 4},
                             {'start': 5, 'end': 6, 'level': 5}]),
    ("1-5,2-6,3-7,4-8", [{'start': 1, 'end': 5, 'level': 1}, {'start': 2, 'end': 6, 'level': 2},
                         {'start': 3, 'end': 7, 'level': 3}, {'start': 4, 'end': 8, 'level': 4}]),
    ("1-1,2-2,3-3", [{'start': 1, 'end': 1, 'level': 1}, {'start': 2, 'end': 2, 'level': 1},
                     {'start': 3, 'end': 3, 'level': 1}]),
    ("1-1,1-2,2-3", [{'start': 1, 'end': 1, 'level': 1}, {'start': 1, 'end': 2, 'level': 2},
                     {'start': 2, 'end': 3, 'level': 3}]),
])
def test_get_entries_with_levels(input_str: str, expected_output: List[Dict[str, int]]):
    allocator = LevelAllocator()
    assert allocator.get_entries_with_levels(input_str) == expected_output
