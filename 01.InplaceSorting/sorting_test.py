"""
Unit tests for sorting algorithms
"""

import random
from itertools import pairwise
import pytest
import sortings


@pytest.fixture(scope="function")
def fatal_array():
    r = random.Random()
    r.seed(123456)

    data = list(range(1000))
    r.shuffle(data)
    return data


def is_sorted(data):
    return all(x <= y for x, y in pairwise(data))


# -------------------------
# Tests principaux
# -------------------------

def test_builtin_sort_array(fatal_array):
    sortings.builtin_sort(fatal_array)
    assert is_sorted(fatal_array)


def test_bubble_sort_array(fatal_array):
    sortings.bubble_sort(fatal_array)
    assert is_sorted(fatal_array)


def test_merge_sort_array(fatal_array):
    sortings.merge_sort(fatal_array)
    assert is_sorted(fatal_array)


# -------------------------
# Edge cases
# -------------------------

def test_empty_array():
    data = []
    sortings.bubble_sort(data)
    assert data == []


def test_single_element():
    data = [42]
    sortings.merge_sort(data)
    assert data == [42]


def test_reversed_array():
    data = [i for i in range(100,0,-1)]
    sortings.bubble_sort(data)
    assert is_sorted(data)
