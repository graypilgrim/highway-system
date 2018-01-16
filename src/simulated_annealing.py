import random
import math
from Model import HighwaySystem


class SimulatedAnnealing:
    def __init__(self, cities, temperature, iterations):
        self.temperature = temperature
        self.iterations = iterations

        solution_x = HighwaySystem(cities)  # random init state
        iteration = 0
        while iteration < iterations:
            solution_y = solution_x.get_neighbour()
            solution_x_quality = HighwaySystem.quality(solution_x)
            solution_y_quality = HighwaySystem.quality(solution_y)
            tolerance = self.tolerance(solution_x_quality, solution_y_quality, temperature)
            if solution_y_quality < solution_x_quality or random.random() < tolerance:
                solution_x = solution_y
            iteration += 1
        self.result = solution_x

    def get_result(self):
        return self.result

    @staticmethod
    def tolerance(solution_x_quality, solution_y_quality, temperature):
        if temperature == 0:
            return 0
        else:
            return math.exp(-math.fabs(solution_y_quality - solution_x_quality) / temperature)
