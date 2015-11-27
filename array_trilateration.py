#!/usr/bin/env python

import argparse
import numpy as np
import itertools

def get_measurements_from_user(n):
    """ n: number of elements. 
    Prompts for input and returns a hash like: 
    {'d01': 1.23, 'd02': 2.34, ..., 'd34': 5.76}
    """
    distances = {}
    pairs = itertools.combinations(range(0, n), 2)
    for pair in pairs:
        el0 = pair[0]
        el1 = pair[1]
        while True:    # keep trying to get valid input
            try:
                d = raw_input("Distance from elelemt {el0} to element {el1}:  ".format(el0 = el0, el1 = el1))
                d = np.float64(d)   # here is where an exception could be thrown
                assert((d > 0) or (d == -1))
                break
            except (TypeError, AssertionError):
                print("Invalid input! Enter -1 for no reading taken. Re-try.")
        key = 'd{n}{m}'.format(n = el0, m = el1)
        distances[key] = d
    print distances
    return distances

def initial_trilateration(p0, p1, distance_matrix):
    for target_number in range(2, distance_matrix.shape[0]):
        d0t = distance_matrix[0][target_number]
        c0t = Circle(p0, d0t)
        d1t = distance_matrix[1][target_number]
        c1t = Circle(p1, d1t)

def build_distance_matrix(n, **kwargs):
    """ n = number of elements.
    kwargs like: {'d01': 1.23, 'd02': 2.34, ..., 'd34': 5.76}
    val should be -1 if measurement not taken
    """
    distance_matrix = np.zeros((n, n))
    pairs = itertools.combinations(range(0, n), 2)
    for pair in pairs:
        el0 = pair[0]
        el1 = pair[1]
        key = 'd{n}{m}'.format(n = el0, m = el1)
        distance = kwargs[key]
        distance_matrix[el0][el1] = distance
        distance_matrix[el1][el0] = distance
    return distance_matrix

def run(n, **kwargs):
    distance_matrix = np.zeros((n, n))
    points = []
    return []

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = "Calculate coordinates from side lengths")
    parser.add_argument('-n', default = 4, type = int, help = "Number of array elements")
    args = parser.parse_args()
    get_measurements_from_user(args.n)
