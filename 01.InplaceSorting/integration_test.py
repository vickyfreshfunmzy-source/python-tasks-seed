#!/usr/bin/env python3
"""
Integration test: run all algorithms on arrays of different sizes
"""

import random
import sortings


def is_sorted(data):
    return all(data[i] <= data[i + 1] for i in range(len(data) - 1))


def run_test(sort_func, size):
    data = list(range(size))
    random.shuffle(data)

    sort_func(data)

    assert is_sorted(data), f"{sort_func.__name__} failed for size {size}"


def main():
    sizes = [0, 1, 2, 10, 100, 1000]

    algorithms = [
        sortings.builtin_sort,
        sortings.bubble_sort,
        sortings.merge_sort,
    ]

    for algo in algorithms:
        print(f"Testing {algo.__name__}")
        for size in sizes:
            run_test(algo, size)

    print("All integration tests passed ")


if __name__ == "__main__":
    main()
