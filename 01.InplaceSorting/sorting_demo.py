#!/usr/bin/env -S python3
"""
Sorting demo with performance measurements
"""

import random
from counting_container import CountingList, CountingOrdered
import sortings


def run_sort(name, sort_func, raw_data):
    """
    Run a sorting algorithm and display stats

    :param name: Name of the algorithm
    :param sort_func: Sorting function
    :param raw_data: Input data (list of ints)
    """

    # Wrap data
    data = CountingList([CountingOrdered(e) for e in raw_data])

    # Reset counters
    CountingList.reset_stats()
    CountingOrdered.reset_stats()

    # Run sorting
    sort_func(data)

    # Display results
    print(f"{name}:")
    print(f"  Comparisons: {CountingOrdered.comparisons()}")
    print(f"  Assignments: {CountingList.assignments()}")
    print(f"  Estimated swaps: {CountingList.likely_swaps()}")
    print("-" * 40)


if __name__ == "__main__":
    # Generate data
    raw_data = list(range(1000))
    random.shuffle(raw_data)

    # Run all algorithms
    run_sort("Builtin Sort", sortings.builtin_sort, raw_data)
    print()
    run_sort("Bubble Sort (O(N^2))", sortings.bubble_sort, raw_data)
    print()
    run_sort("Merge Sort (O(N log N))", sortings.merge_sort, raw_data)
