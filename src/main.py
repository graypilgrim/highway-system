#!/bin/python

import argparse
from Model import HighwaySystem
from Model import Point
from Model import Segment

parser = argparse.ArgumentParser(description='Program finding highway system for given cities with usage of metaheuristics')
parser.add_argument('-f', '--file', help='File with list of cities')
parser.add_argument('-g', '--graphical', action='store_true', help='Show calculations with graphical indicators.')
parser.add_argument('-a', '--algorithm', choices=['vns', 'simulated_annealing'], help='Choose metaheuristics from provided: "vns" or "simulated_annealing"')

args = parser.parse_args()
data_file = open(args.file, 'r')

cities = []
for line in data_file:
    (x, y) = line.split()
    p = Point(x=int(x), y=int(y))
    cities.append(p)

data_file.close()
print(cities)

hs = HighwaySystem(cities)
print(hs.highways)

length = hs.calculate_highways_len()
print('final length: ' + str(length))

slip_roads = hs.calculate_slip_roads_len()
print('slip_roads: ' + str([i for i in slip_roads]))

hs.is_valid()
