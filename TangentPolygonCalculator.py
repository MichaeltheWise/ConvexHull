# -*- coding: utf-8 -*-
"""
Created on Tue Apr 20 2021

@author: Michael Lin
"""
# Following the guidance by Amritya Vagmi on GeeksForGeeks.org
from collections import defaultdict
from LineIntersectionChecker import Point, orientation


class Polygon:
    def __init__(self, point_list=None):
        super(Polygon, self).__init__()
        self.midpoint = None
        self.point_list = []
        if point_list:
            for point in point_list:
                if isinstance(point, Point):
                    self.point_list.append(point)
                else:
                    self.point_list.append(Point(point[0], point[1]))

    def __str__(self):
        return "Polygon with points: {}".format(self.point_list)

    def __len__(self):
        return len(self.point_list)

    def add(self, value):
        """
        Add in point to polygons
        :param value: have to be a set in the format of (x,y)
        :return: None
        """
        if isinstance(value, Point):
            self.point_list.append(value)
        else:
            print("Only accept format is Point")
            raise AttributeError

    def set_midpoint(self):
        """
        Set centroid positions
        :return: None
        """
        x_sum, y_sum = 0, 0
        for point in self.point_list:
            x_sum += point.x
            y_sum += point.y
        n = len(self.point_list)
        self.midpoint = Point(x_sum / n, y_sum / n)

    def maximum_point(self):
        """
        Find the max point of the given point list in terms of x
        :return: Index of the maximum point
        """
        x_max_val = float('-inf')
        x_max_index = 0
        for index, point in enumerate(self.point_list):
            if point.x > x_max_val:
                x_max_val = point.x
                x_max_index = index
        return x_max_index

    def minimum_point(self):
        """
        Find the min point of the given point list in terms of x
        :return: Index of the minimum point
        """
        x_min_val = float('inf')
        x_min_index = 0
        for index, point in enumerate(self.point_list):
            if point.x < x_min_val:
                x_min_val = point.x
                x_min_index = index
        return x_min_index

    def lowest_point(self):
        """
        Find the lowest point of the given point list
        :return: Index of the lowest point
        """
        y_min_val = float('inf')
        y_min_index = 0
        for index, point in enumerate(self.point_list):
            if point.y < y_min_val:
                # If y value of the point is lower than the current minimum val, then replace
                y_min_val = point.y
                y_min_index = index
            elif point.y == y_min_val:
                # If y values are identical, compare x coordinates
                if point.x < self.point_list[y_min_index].x:
                    y_min_index = index
        return y_min_index

    def sort_by_positions(self, point):
        """
        Sorting functionality
        :param point: point
        :return: Sorting functionality
        """
        x, y = point.x, point.y

        # Find the difference between points and the centroid
        p = Point(x - self.midpoint.x, y - self.midpoint.y)

        # Find slope
        if x - self.midpoint.x == 0:
            slope = float('inf')
        else:
            slope = (y - self.midpoint.y) / (x - self.midpoint.x)

        return quadrant(p), slope

    def sort(self):
        """
        Sort polygons counter clock order
        :return: None
        """
        self.set_midpoint()
        self.point_list = sorted(self.point_list, key=lambda p: self.sort_by_positions(p))


class TangentPolygonCalculator:
    def __init__(self):
        super(TangentPolygonCalculator, self).__init__()
        self.polygon_list = defaultdict(Polygon)

    def __setitem__(self, key, value):
        if isinstance(value, Polygon):
            self.polygon_list[key] = value
        else:
            print("Input has to be a polygon")
            raise AttributeError

    def __getitem__(self, key):
        if key in self.polygon_list:
            return self.polygon_list[key]
        else:
            print("Polygon {} doesn't exist".format(key))
            raise KeyError

    def summary(self, a, b):
        """
        Summary of Upper and Lower Tangents
        :param a: polygon A
        :param b: polygon B
        :return: Print out the upper and lower tangents
        """
        print("\nUpper Tangent: {}".format(self.upper_tangent(a, b)))
        print("Lower Tangent: {}".format(self.lower_tangent(a, b)))

    def upper_tangent(self, a, b, idx=False):
        """
        Output the Upper Tangent
        :param a: polygon A
        :param b: polygon B
        :param idx: output index, default as false
        :return: Return the upper tangent points or index
        """
        poly_a, poly_b = self._prepare_polygon(a, b)
        index_a, index_b = self._upper_tangent(poly_a, poly_b)
        if idx:
            return index_a, index_b
        return [poly_a.point_list[index_a], poly_b.point_list[index_b]]

    def lower_tangent(self, a, b, idx=False):
        """
        Output the Lower Tangent
        :param a: polygon A
        :param b: polygon B
        :param idx: output index, default as false
        :return: Return the lower tangent points or index
        """
        poly_a, poly_b = self._prepare_polygon(a, b)
        index_a, index_b = self._lower_tangent(poly_a, poly_b)
        if idx:
            return index_a, index_b
        return [poly_a.point_list[index_a], poly_b.point_list[index_b]]

    def _prepare_polygon(self, a, b):
        if len(self.polygon_list) < 2:
            print("Need at least two polygons")
            return
        elif len(self.polygon_list) > 2:
            if a is None or b is None:
                print("Please specify which two polygons for operation")
                return

        # Polygons are assigned and sorted
        poly_a = self.polygon_list[a]
        poly_a.sort()
        max_a_index = poly_a.maximum_point()
        poly_b = self.polygon_list[b]
        poly_b.sort()
        min_b_index = poly_b.minimum_point()

        # Swap if b is on a's left side
        if (poly_a.point_list[max_a_index]).x > (poly_b.point_list[min_b_index]).x:
            poly_a, poly_b = poly_b, poly_a

        return poly_a, poly_b

    def _upper_tangent(self, poly_a, poly_b):
        """
        Implementation of Upper Tangent Search
        :param poly_a: polygon 1
        :param poly_b: polygon 2
        :return: Tangent points index in their respective lists
        """
        max_a_index = poly_a.maximum_point()
        min_b_index = poly_b.minimum_point()

        poly_a_point_list = poly_a.point_list
        poly_b_point_list = poly_b.point_list

        # Upper tangent implementation
        done = 0
        while not done:
            done = 1
            # If the line crosses a, we move to the next counterclockwise a point
            # If the line crosses b, we move to the next clockwise b point
            while orientation(poly_b_point_list[min_b_index], poly_a_point_list[max_a_index],
                              poly_a_point_list[(max_a_index + 1) % len(poly_a)]) == 1:
                # Rotate counterclockwise to find next a location
                max_a_index = (max_a_index + 1) % len(poly_a)
            while orientation(poly_a_point_list[max_a_index], poly_b_point_list[min_b_index],
                              poly_b_point_list[(len(poly_b) + min_b_index - 1) % len(poly_b)]) == 2:
                # Rotate clockwise to find next b location
                min_b_index = (len(poly_b) + min_b_index - 1) % len(poly_b)
                done = 0
        return max_a_index, min_b_index

    def _lower_tangent(self, poly_a, poly_b):
        """
        Implementation of Upper Tangent Search
        :param poly_a: polygon 1
        :param poly_b: polygon 2
        :return: Tangent points index in their respective lists
        """
        max_a_index = poly_a.maximum_point()
        min_b_index = poly_b.minimum_point()

        poly_a_point_list = poly_a.point_list
        poly_b_point_list = poly_b.point_list

        # Upper tangent implementation
        done = 0
        while not done:
            done = 1
            # If the line crosses a, we move to the next clockwise a point
            # If the line crosses b, we move to the next counterclockwise b point
            while orientation(poly_b_point_list[min_b_index], poly_a_point_list[max_a_index],
                              poly_a_point_list[(len(poly_a) + max_a_index - 1) % len(poly_a)]) == 2:
                # Rotate clockwise to find next a location
                max_a_index = (len(poly_a) + max_a_index - 1) % len(poly_a)
            while orientation(poly_a_point_list[max_a_index], poly_b_point_list[min_b_index],
                              poly_b_point_list[(min_b_index + 1) % len(poly_b)]) == 1:
                # Rotate counterclockwise to find next b location
                min_b_index = (min_b_index + 1) % len(poly_b)
                done = 0
        return max_a_index, min_b_index


# Function to check quadrant
def quadrant(point):
    """
    Check quadrant of a point
    :param point: point
    :return: Return quadrant of a point
    """
    x, y = point.x, point.y
    if x >= 0 and y >= 0:
        return 1
    elif x <= 0 <= y:
        return 2
    elif x <= 0 and y <= 0:
        return 3
    else:
        return 4


def main():
    point_list = [(2, 2), (3, 1), (3, 3), (5, 2)]
    mock_polygon_a = Polygon(point_list)
    mock_polygon_a.add(Point(4, 0))
    mock_polygon_a.sort()
    print(mock_polygon_a)

    point_list_a = [(2, 2), (3, 1), (3, 3), (5, 2), (4, 0)]
    polygon_a = Polygon(point_list_a)
    point_list_b = [(0, 1), (1, 0), (0, -2), (-1, 0)]
    polygon_b = Polygon(point_list_b)
    tangent_calculator_test = TangentPolygonCalculator()
    tangent_calculator_test['a'] = polygon_a
    tangent_calculator_test['b'] = polygon_b
    tangent_calculator_test.summary('a', 'b')


if __name__ == '__main__':
    main()
