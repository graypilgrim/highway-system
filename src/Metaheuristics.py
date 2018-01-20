from Model import HighwaySystem

import random
import math
import sys


class SimulatedAnnealing:
    def __init__(self, cities):
        solution_x = HighwaySystem(cities)  # random init state
        temperature = 1.0
        k = 0.995

        while temperature > 0.001:
            solution_y = solution_x.get_random_neighbour()
            solution_x_quality = HighwaySystem.quality(solution_x)
            solution_y_quality =  HighwaySystem.quality(solution_y)
            tolerance = self.tolerance(solution_x_quality, solution_y_quality, temperature)

            if solution_y_quality < solution_x_quality or random.random() < tolerance:
                solution_x = solution_y
            temperature = k*temperature

        self.result = solution_x

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

                # print('current: ' + str(self.highway_system.highways))
                print('current: ' + str(self.highway_system.quality()))
                print('best neighbour: ' + str(best_neighbour.quality()))
                # print('best neighbour: ' + str(best_neighbour.highways))
                print('radius: ' + str(radius))
                # print('')

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
