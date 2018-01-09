import random
from math import sqrt
from typing import NamedTuple

class Point(NamedTuple):
    x: int
    y: int

class Segment(NamedTuple):
    a: Point
    b: Point

class Vertex(NamedTuple):
    point: Point
    connection: bool

class HighwaySystem:
    def __init__(self, cities):
        self.cities = cities
        self.highways = [Vertex(Point(x=random.randint(-100, 100), y=random.randint(-100, 100)), bool(random.getrandbits(1))) for i in range(len(cities))]

    def calculate_highways_len(self):
        res = 0.0
        prev = self.highways[-1]
        for elem in self.highways:
            if elem.connection == False:
                prev = elem
                continue

            length = self.point_to_point_distance(elem.point, prev.point)
            res += length
            prev = elem

        return res

    def calculate_slip_roads_len(self):
        prev = self.highways[-1]
        for city in self.cities:
            res = float('inf')
            prev = self.highways[-1]
            for elem in self.highways:
                if elem.connection == False:
                    prev = elem
                    continue

                distance = self.point_to_segment_distance(Segment(prev.point, elem.point), city)
                res = min(distance, res)

            yield res

    def point_to_point_distance(self, point_a, point_b):
        return sqrt((point_a.x - point_b.x)**2 + (point_a.y - point_b.y)**2)

    def between(self, segment, point):
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

    def point_to_segment_distance(self, segment, point):
        if not self.between(segment, point):
            distance_a = self.point_to_point_distance(segment.a, point)
            distance_b = self.point_to_point_distance(segment.b, point)
            return distance_a if distance_a < distance_b else distance_b

        # TODO: case when 0 in denominators

        segment_coefficient_a = (segment.b.y - segment.a.y) / (segment.b.x - segment.a.x)
        segment_coefficient_b = (segment.b.x*segment.a.y - segment.a.x*segment.b.y)/(segment.b.x - segment.a.x)

        coefficient_a = -1/(segment_coefficient_a)
        coefficient_b = point.y - coefficient_a*point.x

        point_image_x = (coefficient_b - segment_coefficient_b) / (segment_coefficient_a - coefficient_a)
        point_image_y = segment_coefficient_a * point_image_x + segment_coefficient_b

        return self.point_to_point_distance(Point(point_image_x, point_image_y), point)
