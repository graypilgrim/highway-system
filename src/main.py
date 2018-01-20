#!/bin/python

import argparse
import matplotlib.pyplot as plt
import numpy as np

from Model import HighwaySystem
from Model import Point
from Model import Segment
from Metaheuristics import VNS

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
hs.create_random_highway()

prev = hs.highways[-1]
for elem in hs.highways:
    if elem.connection == False:
        prev = elem
        continue

    plt.plot([prev.point.x, elem.point.x], [prev.point.y, elem.point.y], 'b-')
    prev = elem

vns = VNS(hs, 5)
vns.run()
print('result: ' + str(vns.highway_system.highways))

for city in cities:
    plt.plot(city.x, city.y, 'ro')

prev = vns.highway_system.highways[-1]
for elem in vns.highway_system.highways:
    if elem.connection == False:
        prev = elem
        continue

    plt.plot([prev.point.x, elem.point.x], [prev.point.y, elem.point.y], 'g-')
    prev = elem

plt.axis([-100, 100, -100, 100])
plt.show()
