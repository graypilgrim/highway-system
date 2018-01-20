import random
import math
from Model import HighwaySystem


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

    def _init_(self, cities, K):
        solution_x = HighwaySystem(cities)  # random init state
        solution_x = solution_x.get_best_neighbour()
        while True:
            k = 1
            while True:
                solution_y = solution_x.get_neighbourhood(k)
                best_solution_y = solution_y.get_best_neighbour()
                k = k + 1
                if HighwaySystem.quality(best_solution_y) > HighwaySystem.quality(solution_x) or k > K:
                    break
                solution_x = best_solution_y
            self.result = solution_x
            break

    def get_result(self):
        return self.result

