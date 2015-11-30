#!/usr/bin/env python

import argparse
import numpy as np
import itertools
import random
import json
from point import Point
from circle import Circle

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
        distances[key] = round(d, 4)
    return distances

def get_centroid(points):
    """ Points is a list of points
    """
    return sum(points, Point(0, 0))/len(points)


def initial_trilateration(p0, p1, distance_matrix):
    points = [p0, p1]
    for target_number in range(2, distance_matrix.shape[0]):
        d0t = distance_matrix[0][target_number]
        c0t = Circle(p0, d0t)
        d1t = distance_matrix[1][target_number]
        c1t = Circle(p1, d1t)
        points.append(c0t.positive_intersection_with(c1t))
    return points

def trilateration_phase(points_in, distance_matrix):
    points_out = [points_in[0]]  # force point 0 to stay at origin
    for target_idx in range(1, len(points_in)):
        approximations = []  # points which are approximate 'target' 
        # we want pairs of circles which intersect at target. Will have circle A and circle B.
        for source_a_idx, source_b_idx in itertools.combinations(range(0, len(points_in)), 2):
            # ensure the centre of the circle isn't target. 
            # It must be defined by another point and target
            if (source_a_idx != target_idx) and (source_b_idx != target_idx):
                a_center = points_in[source_a_idx]
                a_rad = distance_matrix[source_a_idx][target_idx]
                a = Circle(a_center, a_rad)
                b_center = points_in[source_b_idx]
                b_rad = distance_matrix[source_b_idx][target_idx]
                b = Circle(b_center, b_rad)
                intersections = a.intersection_with(b)
                approximations.append(points_in[target_idx].get_closest(intersections))
        approximation = get_centroid(approximations)
        points_out.append(approximation)
    return points_out

def build_distance_matrix_from_distances(n, distances):
    """ n = number of elements.
    distances like: {'d01': 1.23, 'd02': 2.34, ..., 'd34': 5.76}
    val should be -1 if measurement not taken
    """
    distance_matrix = np.zeros((n, n))
    pairs = itertools.combinations(range(0, n), 2)
    for pair in pairs:
        el0 = pair[0]
        el1 = pair[1]
        key = 'd{n}{m}'.format(n = el0, m = el1)
        distance = distances[key]
        distance_matrix[el0][el1] = distance
        distance_matrix[el1][el0] = distance
    return distance_matrix

def calculate_cost(distances0, distances1):
    assert(distances0.shape == distances1.shape)
    cost = 0
    for n, m in itertools.combinations(range(0, distances0.shape[0]), 2):
        c = 100*abs(1-(distances1[n][m]/distances0[n][m]))  # get percentage error squared
        cost += np.square(c)
    return cost

def print_cost(distances0, distances1):
    assert(distances0.shape == distances1.shape)
    cost = 0
    for n, m in itertools.combinations(range(0, distances0.shape[0]), 2):
        c = 100*abs(1-(distances1[n][m]/distances0[n][m]))  # get percentage error squared
        print("{n} -> {m}: expected: {e:.3f}, found: {f:.3f}, error: {c:.3f}%".format(
            n = n, m = m, e = distances0[n][m], f = distances1[n][m], c = c))
        cost += np.square(c)
    print(cost)
    return cost

def build_distance_matrix_from_points(points):
    distance_matrix = np.ndarray((len(points), len(points)))
    for n in range(0, len(points)):
        for m in range(0, len(points)):
            distance_matrix[n][m] = points[n].distance_to_other(points[m])
    return distance_matrix

def run(n, **kwargs):
    distance_matrix_target = build_distance_matrix_from_distances(n, kwargs)
    p0 = Point(0, 0)
    p1 = Point(distance_matrix_target[0][1], 0)
    points = initial_trilateration(p0, p1, distance_matrix_target)
    best_points = points
    distance_matrix_calculated = build_distance_matrix_from_points(points)
    best_cost = calculate_cost(distance_matrix_target, distance_matrix_calculated)
    best_distance_matrix = distance_matrix_calculated
    for phase in range(30):
        points = trilateration_phase(points, distance_matrix_target)
        distance_matrix_calculated = build_distance_matrix_from_points(points)
        cost = calculate_cost(distance_matrix_target, distance_matrix_calculated)
        if cost <= best_cost:
            #print("-------------------------------------")
            #print("Phase: {p}".format(p = phase))
            best_cost = cost
            best_points = points
            best_distance_matrix = distance_matrix_calculated
            #print(points)
            #print(cost)
    #print("----------------BEST-----------------")
    #print_cost(distance_matrix_target, best_distance_matrix)
    #print(best_points)
    return best_points

def remove_origin_offset(points):
    centroid = get_centroid(points)
    return [point - centroid for point in points]

def noisify(v):
    #return v * (1 + random.gauss(0, 0.03))
    return round(v,1)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = "Calculate coordinates from side lengths")
    parser.add_argument('-n', default = 4, type = int, help = "Number of array elements")
    args = parser.parse_args()
    #distances = { 'd01': noisify(4.0), 
    #              'd02': noisify(5.0), 
    #              'd03': noisify(5.09901951359), 
    #              'd12': noisify(4.12310562562),
    #              'd13': noisify(5.83095189485),
    #              'd23': noisify(2.2360679775)}
    distances = { 'd01': noisify(1.41), 
                  'd02': noisify(2), 
                  'd03': noisify(1.41), 
                  'd12': noisify(1.41),
                  'd13': noisify(2),
                  'd23': noisify(1.41)}
    distances = get_measurements_from_user(args.n)
    print(distances)
    target_matrix = build_distance_matrix_from_distances(args.n, distances)
    points = run(args.n, **distances)
    result_matrix = build_distance_matrix_from_points(points)
    print_cost(target_matrix, result_matrix)
    points = remove_origin_offset(points)
    array = []
    for idx, point in enumerate(points):
        print("Point {idx} : ({p.x:.4f}, {p.y:.4f})".format(idx = idx, p = point))
        array.append({'x':point.x, 'y':point.y})
    array_json = json.dumps(array, indent=2)
    with open('array_geometry.json', 'w') as f:
        f.write(array_json)
