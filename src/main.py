#!/bin/python

import argparse
import random
from math import sqrt
from typing import NamedTuple

class Point(NamedTuple):
    x: int
    y: int

class Segment(NamedTuple):
    a: Point
    b: Point

def calculate_polyline_len(polyline):
    res = 0.0
    prev = polyline[-1]
    for point in polyline:
        if point[1] == False:
            prev = point
            continue

        length = sqrt((point[0].x - prev[0].x)**2 + (point[0].y - prev[0].y)**2)
        print('length: ' + str(length))
        res += length
        prev = point

    return res

def between(segment, point):
    if segment.a.x < segment.b.x:
        if segment.a.x < point.x < segment.b.x:
            return True
    else:
        if segment.b.x < point.x < segment.a.x:
            return True

    if segment.a.y < segment.b.y:
        if segment.a.y < point.y < segment.b.y:
            return True
    else:
        if segment.b.y < point.y < segment.a.y:
            return True

    return False

def distance(segment, point):
    if not between(segment, point):
        distance_a = sqrt((segment.a.x - point.x)**2 + (segment.a.y - point.y)**2)
        distance_b = sqrt((segment.b.x - point.x)**2 + (segment.b.y - point.y)**2)
        return distance_a if distance_a < distance_b else distance_b

    segment_coefficient_a = (segment.b.y - segment.a.y) / (segment.b.x - segment.a.x)
    segment_coefficient_b = (segment.b.x*segment.a.y - segment.a.x*segment.b.y)/(segment.b.x - segment.a.x)

    coefficient_a = -1/(segment_coefficient_a)
    coefficient_b = point.y - coefficient_a*point.x

    print('coefficient_a: ' + str(coefficient_a))
    print('coefficient_b: ' + str(coefficient_b))


parser = argparse.ArgumentParser(description='Program finding highway system for given cities with usage of metaheuristics')
parser.add_argument('-f', '--file', help='File with list of cities')
parser.add_argument('-g', '--graphical', action='store_true', help='Show calculations with graphical indicators.')
parser.add_argument('-a', '--algorithm', choices=['vns', 'simulated_annealing'], help='Choose metaheuristics from provided: "vns" or "simulated_annealing"')

args = parser.parse_args()
data_file = open(args.file, 'r')

cities = []
max_x = 0
min_x = 0
max_y = 0
min_y = 0
for line in data_file:
    (x, y) = line.split()
    p = Point(x=int(x), y=int(y))
    cities.append(p)
    max_x = max(max_x, int(x))
    min_x = min(min_x, int(x))
    max_y = max(max_y, int(y))
    min_y = min(min_y, int(y))

data_file.close()
print(cities)

highways = [(Point(x=random.randint(min_x, max_x), y=random.randint(min_y, max_y)), bool(random.getrandbits(1))) for i in range(len(cities))]
print(highways)

length = calculate_polyline_len(highways)
print('final length: ' + str(length))

d = distance(Segment(Point(1, 1), Point(4, 2)), Point(2, 3))
print('d: ' + str(d))
