# -*- coding: utf-8 -*-
"""
Created on Fri Apr 16 2021

@author: Michael Lin
"""
# Jarvis' Algorithm
from LineIntersectionChecker import Point, orientation


class ConvexHullJarvis:
    def __init__(self, point_list):
        self.point_list = []
        for val in point_list:
            new_point = Point(val[0], val[1])
            self.point_list.append(new_point)

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

    def convex_hull(self):
        """
        Implementation of Convex Hull Jarvis' Algorithm
        :return: List of convex hull nodes
        """
        # if there are less than three nodes, then return
        if len(self.point_list) < 3:
            return None

        convex_hull_list = []
        left_most_idx = self.left_most_point()
        curr_idx = left_most_idx

        # Keep doing the search and replace operation until we loop around
        # curr_idx is the one we have confirmed
        # next_idx is the one we are searching
        # i is the search through all points, aiming to replace next_idx
        while True:
            # Append the confirmed point
            convex_hull_list.append(self.point_list[curr_idx])

            next_idx = (curr_idx + 1) % len(self.point_list)
            for i in range(len(self.point_list)):
                # If the selected point is again more counterclockwise than before, replace the point
                if orientation(self.point_list[curr_idx], self.point_list[next_idx], self.point_list[i]) == 2:
                    next_idx = i

            # After finding the most counterclockwise node, move forward
            curr_idx = next_idx

            # Stop when we reach original point
            if curr_idx == left_most_idx:
                break

        return convex_hull_list


def main():
    point_list = [(0, 3), (2, 2), (1, 1), (2, 1), (3, 0), (0, 0), (3, 3)]
    convex_hull_test = ConvexHullJarvis(point_list)
    print(convex_hull_test.convex_hull())


if __name__ == '__main__':
    main()


