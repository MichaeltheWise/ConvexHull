# -*- coding: utf-8 -*-
"""
Created on Wed Apr 21 2021

@author: Michael Lin
"""
from LineIntersectionChecker import Point, orientation
from ConvexHull import ConvexHullJarvis
from TangentPolygonCalculator import Polygon, TangentPolygonCalculator


class ConvexHullDivideNConquer:
    def __init__(self, point_list):
        super(ConvexHullDivideNConquer, self).__init__()
        self.point_list = []
        self.midpoint = None
        for val in point_list:
            new_point = Point(val[0], val[1])
            self.point_list.append(new_point)

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

    def convex_hull(self):
        # Find midpoint
        self.set_midpoint()
        left = [point for point in self.point_list if point.x <= self.midpoint.x]
        right = [point for point in self.point_list if point.x > self.midpoint.x]

        # Divide and conquer
        # Left and right convex hull can be recursively found
        # Here Jarvis Algorithm is directly applied
        left_convex_hull = ConvexHullJarvis(left).convex_hull()
        right_convex_hull = ConvexHullJarvis(right).convex_hull()

        # Find tangents by using tangent polygon calculator
        left_polygon = Polygon(left_convex_hull)
        right_polygon = Polygon(right_convex_hull)
        tangent_finder = TangentPolygonCalculator()
        tangent_finder[1] = left_polygon
        tangent_finder[2] = right_polygon
        left_upper_idx, right_upper_idx = tangent_finder.upper_tangent(1, 2, idx=True)
        left_lower_idx, right_lower_idx = tangent_finder.lower_tangent(1, 2, idx=True)

        # Need to do a collinear check else the convex hull will have extra collinear points
        left_upper_idx, right_upper_idx, left_lower_idx, right_lower_idx = self.collinear_check(left_polygon,
                                                                                                right_polygon,
                                                                                                left_upper_idx,
                                                                                                right_upper_idx,
                                                                                                left_lower_idx,
                                                                                                right_lower_idx)

        # Merge
        res = []
        left_idx = left_upper_idx
        # Turn counterclockwise to include the left outer convex hull points until the lower index is reached
        while left_idx != left_lower_idx:
            res.append(left_polygon.point_list[left_idx])
            left_idx = (left_idx + 1) % len(left_polygon)
        res.append(left_polygon.point_list[left_idx])

        right_idx = right_upper_idx
        # Turn clockwise to include the right outer convex hull points until the lower index is reached
        while right_idx != right_lower_idx:
            res.append(right_polygon.point_list[right_idx])
            right_idx = (len(right_polygon) + right_idx - 1) % len(right_polygon)
        res.append(right_polygon.point_list[right_idx])

        # Use polygon to sort
        sort_poly = Polygon(res)
        sort_poly.sort()
        return sort_poly.point_list

    def left_most_point(self):
        """
        Find the left most point possible
        :return: The index of the left most point
        """
        minimum_index = 0
        if self.point_list:
            for i in range(1, len(self.point_list)):
                if self.point_list[i].x < self.point_list[minimum_index].x:
                    minimum_index = i
                elif self.point_list[i].x == self.point_list[minimum_index].x:
                    if self.point_list[i].y > self.point_list[minimum_index].y:
                        minimum_index = i
        return minimum_index

    def collinear_check(self, left_polygon, right_polygon, left_upper_idx, right_upper_idx, left_lower_idx,
                        right_lower_idx):
        """
        Collinear Check on Upper and Lower Tangents to Ensure No Extra Point
        :param left_polygon: left polygon
        :param right_polygon: right polygon
        :param left_upper_idx: left polygon upper tangent point
        :param right_upper_idx: right polygon upper tangent point
        :param left_lower_idx: left polygon lower tangent point
        :param right_lower_idx: right polygon lower tangent point
        :return: Updated indexes
        """
        left_up, left_down, right_up, right_down = left_upper_idx, left_lower_idx, right_upper_idx, right_lower_idx
        left_upper_next_idx = (left_upper_idx + 1) % len(left_polygon)
        right_lower_next_idx = (right_lower_idx + 1) % len(right_polygon)
        left_lower_next_idx = (len(left_polygon) + left_lower_idx - 1) % len(left_polygon)
        right_upper_next_idx = (len(right_polygon) + right_upper_idx - 1) % len(right_polygon)

        # If collinear, then replace
        if orientation(right_polygon.point_list[right_upper_idx], left_polygon.point_list[left_upper_idx],
                       left_polygon.point_list[left_upper_next_idx]) == 0:
            left_up = left_upper_next_idx
        if orientation(left_polygon.point_list[left_lower_idx], right_polygon.point_list[right_lower_idx],
                       right_polygon.point_list[right_lower_next_idx]) == 0:
            right_down = right_lower_next_idx
        if orientation(right_polygon.point_list[right_lower_idx], left_polygon.point_list[left_lower_idx],
                       left_polygon.point_list[left_lower_next_idx]) == 0:
            left_down = left_lower_next_idx
        if orientation(left_polygon.point_list[left_upper_idx], right_polygon.point_list[right_upper_idx],
                       right_polygon.point_list[right_upper_next_idx]) == 0:
            right_up = right_upper_next_idx

        return left_up, right_up, left_down, right_down


def main():
    # point_list = [(0, 3), (2, 2), (1, 1), (2, 1), (3, 0), (0, 0), (3, 3)]
    point_list = [(0, 0), (1, -4), (-1, -5), (-5, -3), (-3, -1), (-1, -3), (-2, -2), (-1, -1), (-2, -1), (-1, 1)]
    convex_hull_test = ConvexHullDivideNConquer(point_list)
    print(convex_hull_test.convex_hull())
    # convex_hull_jarvis = ConvexHullJarvis(point_list)
    # print(convex_hull_jarvis.convex_hull())


if __name__ == '__main__':
    main()
