import pytest
import random


from kth_element import kth_element


def kth_element_reference_implementation(array, k):
    return sorted(array)[k]


def test_random():
    random.seed(17)
    for _ in range(1000):
        n = random.randint(1, 10)
        array = list(range(n))
        random.shuffle(array)
        k = random.randint(0, len(array) - 1)
        expected_kth = kth_element_reference_implementation(array, k)
        kth = kth_element(array, k)
        assert kth == expected_kth