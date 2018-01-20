#!/bin/python

import argparse
import matplotlib.pyplot as plt
import numpy as np

from Model import HighwaySystem
from Model import Point
from Model import Segment
from Metaheuristics import VNS
from Metaheuristics import SimulatedAnnealing

def plot_highway(highways, style):
    prev = highways[-1]
    for elem in highways:
        if elem.connection == False:
            prev = elem
            continue

        plt.plot([prev.point.x, elem.point.x], [prev.point.y, elem.point.y], style)
        prev = elem

parser = argparse.ArgumentParser(description='Program finding highway system for given cities with usage of metaheuristics')
parser.add_argument('-f', '--file', help='File with list of cities')
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
for city in cities:
    plt.plot(city.x, city.y, 'ro')


hs = HighwaySystem(cities)
hs.create_random_highway()

plot_highway(hs.highways, 'b-')

if args.algorithm == 'vns':
    vns = VNS(hs, 20)
    vns.run()
    print('result: ' + str(vns.highway_system.highways))
    plot_highway(vns.highway_system.highways, 'g-')

else:
    sa = SimulatedAnnealing(hs)
    sa.run()
    print('result: ' + str(sa.highway_system.highways))
    plot_highway(sa.highway_system.highways, 'g-')

plt.axis([-100, 100, -100, 100])
plt.show()
