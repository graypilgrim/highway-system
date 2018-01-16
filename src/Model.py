import random
from math import sqrt
from typing import NamedTuple
import sys


class Point(NamedTuple):
    x: int
    y: int


class Segment(NamedTuple):
    a: Point
    b: Point


class Vertex(NamedTuple):
    point: Point
    connection: bool


class BoundingRectangle:
    def __init__(self):
        self.top_right = [-sys.maxsize-1, -sys.maxsize-1]
        self.bottom_left = [sys.maxsize, sys.maxsize]

    def is_in(self, segment):
        if segment.a.x > self.top_right[0] or segment.a.x < self.bottom_left[0] and segment.b.x > self.top_right[0] or segment.b.x < self.bottom_left[0]:
            return False

        if segment.a.y > self.top_right[1] or segment.a.y < self.bottom_left[1] and segment.b.y > self.top_right[1] or segment.b.y < self.bottom_left[1]:
            return False

        return True

    def add(self, segment):
        self.top_right[0] = max(self.top_right[0], segment.a.x)
        self.top_right[0] = max(self.top_right[0], segment.b.x)
        self.top_right[1] = max(self.top_right[1], segment.a.x)
        self.top_right[1] = max(self.top_right[1], segment.b.x)

        self.bottom_left[0] = min(self.bottom_left[0], segment.a.x)
        self.bottom_left[0] = min(self.bottom_left[0], segment.b.x)
        self.bottom_left[1] = min(self.bottom_left[1], segment.a.x)
        self.bottom_left[1] = min(self.bottom_left[1], segment.b.x)


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

        if segment.b.x == segment.a.x:
            return abs(segment.a.x - point.x)

        segment_coefficient_a = (segment.b.y - segment.a.y) / (segment.b.x - segment.a.x)
        segment_coefficient_b = (segment.b.x*segment.a.y - segment.a.x*segment.b.y)/(segment.b.x - segment.a.x)

        coefficient_a = -1/(segment_coefficient_a)
        coefficient_b = point.y - coefficient_a*point.x

        point_image_x = (coefficient_b - segment_coefficient_b) / (segment_coefficient_a - coefficient_a)
        point_image_y = segment_coefficient_a * point_image_x + segment_coefficient_b

        return self.point_to_point_distance(Point(point_image_x, point_image_y), point)

    def is_valid(self):
        rect = BoundingRectangle()
        prev = self.highways[-1]
        segments = set()
        for elem in self.highways:
            if elem.connection == False:
                prev = elem
                continue

            segment = Segment(Point(prev.point.x, prev.point.y), Point(elem.point.x, elem.point.y))

            if not rect.is_in(segment):
                return False

            if not self.is_intersection(segments, segment):
                return False

            segments.add(segment)
            rect.add(segment)

        return True

    def is_intersection(self, segments, segment):
        for seg in segments:

            if seg.a.x == seg.b.x:
                if segment.a.x <= seg.a.x and segment.b.x >= seg.a.x or segment.a.x > seg.a.x and segment.b.x < seg.a.x:
                    return True

            coefficient_a = (seg.b.y - seg.a.y) / (seg.b.x - seg.a.x)
            coefficient_b = (seg.b.x*seg.a.y - seg.a.x*seg.b.y)/(seg.b.x - seg.a.x)

            val_a = coefficient_a*segment.a.x + coefficient_b
            val_b = coefficient_a*segment.b.x + coefficient_b

            if segment.a.y > val_a and segment.b.y < val_b:
                return True

            if segment.a.y < val_a and segment.b.y > val_b:
                return True

        return False

    def quality(self, calculate_highways_len, calculate_slip_roads_len):
        result = calculate_highways_len + 2^calculate_slip_roads_len - 1
        return result