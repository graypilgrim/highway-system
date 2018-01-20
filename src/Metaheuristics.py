from Model import HighwaySystem

import random
import math
import sys


class SimulatedAnnealing:
    def __init__(self, highway_system):
        self.highway_system = highway_system
        self.temperature = 1.0
        self.coefficient = 0.995


    def run(self):
        while self.temperature > 0.001:
            quality = self.highway_system.quality()
            temp_highway_system = self.highway_system.get_random_neighbour()
            temp_quality = temp_highway_system.quality()
            tolerance = self.tolerance(quality, temp_quality, self.temperature)

            print('current: ' + str(quality))
            print('best neighbour: ' + str(temp_quality))

            if temp_quality < quality or random.random() < tolerance:
                self.highway_system = temp_highway_system

            self.temperature = self.coefficient*self.temperature
            print('temp: ' + str(self.temperature))

    def get_result(self):
        return self.result

    @staticmethod
    def tolerance(solution_x_quality, solution_y_quality, temperature):
        if temperature == 0:
            return 0
        else:
            return math.exp(-math.fabs(solution_y_quality - solution_x_quality) / temperature)

class VNS:
    def __init__(self, highway_system, max_neighbourhood_radius):
        self.highway_system = highway_system
        self.max_neighbourhood_radius = max_neighbourhood_radius

    def run(self):
        print ('begin quality: ' + str(self.highway_system.quality()))

        while(True):
            for radius in range(1, self.max_neighbourhood_radius + 1):
                neighbours = self.highway_system.get_neighbourhood(radius)
                best_neighbour = self.choose_best_neighbour(neighbours)

                print('current: ' + str(self.highway_system.quality()))
                print('best neighbour: ' + str(best_neighbour.quality()))
                print('radius: ' + str(radius))

                if best_neighbour.quality() < self.highway_system.quality():
                    self.highway_system = best_neighbour
                    break;

            if radius == self.max_neighbourhood_radius:
                return

        print ('end quality: ' + str(self.highway_system.quality()))

    def choose_best_neighbour(self, neighbours):
        best_result = sys.maxsize
        best_result_index = -1

        for i in range(len(neighbours)):
            quality = neighbours[i].quality()
            if quality < best_result:
                best_result = quality
                best_result_index = i

        return neighbours[best_result_index]

    def get_result(self):
        return self.result
