import random


def kth_element(array, k):
    """
    Return `sorted(array)[k]`
    """
    # Choose random index i
    if len(array) == 1:
        return array[0]

    i = random.randint(0, len(array) - 1)

    # Partition array in two parts such that
    # elements in the first part are < array[i],
    # elements in the second part are > array[i],
    # and the element in beween is array[i].
    #
    # Get new index p of array[i]
    p = partition(array, i)

    # If array[i] was kth element, return it.
    if k == p:
        return array[p]

    # Search for kth element in one of the parts
    if k < p:
        return kth_element(array[:p], k)
    return kth_element(array[p+1:], k - p - 1)


def partition(array, i):
    """
    Partition array in two parts such that
    elements in the first part are < array[i],
    elements in the second part are > array[i],
    and the element in beween is array[i].

    Return new index of element array[i].
    """
    x = array[i]
    n = len(array)
    array[i], array[n-1] = array[n-1], array[i]
    p = 0
    for j in range(len(array)):
        if array[j] < x:
            array[p], array[j] = array[j], array[p]
            p += 1
    array[p], array[n-1] = array[n-1], array[p]

    return p
