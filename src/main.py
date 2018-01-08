#!/bin/python

import argparse

parser = argparse.ArgumentParser(description='Program finding highway system for given cities with usage of metaheuristics')
parser.add_argument('-f', '--file', help='File with list of cities')
parser.add_argument('-g', '--graphical', action='store_true', help='Show calculations with graphical indicators.')
parser.add_argument('-a', '--algorithm', choices=['vns', 'simulated_annealing'], help='Choose metaheuristics from provided: "vns" or "simulated_annealing"')

args = parser.parse_args()

print(args)
