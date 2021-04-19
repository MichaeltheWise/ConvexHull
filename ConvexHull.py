# -*- coding: utf-8 -*-
"""
Created on Fri Apr 16 2021

@author: Michael Lin
"""
from LineIntersectionChecker import Point, orientation
import numpy as np
import copy
# Jarvis Algorithm


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
                if curr_idx == i:
                    continue
                # If the selected point is again more clockwise than before, replace the point
                # Or if collinear, if distance larger, also replace
                # For example, using the complicated example
                # it goes from o((0,0), (1,4), point[i])
                # all the way to o((0,0), (7,0), point[i]) which yields the most clockwise
                # Can also be counterclockwise but the orientation calculation below needs to be changed
                o = orientation(self.point_list[curr_idx], self.point_list[next_idx], self.point_list[i])
                if o == 1 or (o == 0 and distance(self.point_list[i], self.point_list[next_idx]) > distance(
                        self.point_list[next_idx], self.point_list[curr_idx])):
                    next_idx = i

            # After finding the most counterclockwise node, move forward
            curr_idx = next_idx

            # Stop when we reach original point
            if curr_idx == left_most_idx:
                break

        return convex_hull_list

# Graham Scan


class ConvexHullGraham:
    def __init__(self, point_list):
        self.point_list = []
        for val in point_list:
            new_point = Point(val[0], val[1])
            self.point_list.append(new_point)

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

    def update_point_list(self, point_list):
        """
        Remove points with the same angle and only leave the ones that are the farthest away
        :param point_list: point list that has been sorted by angle and distance
        :return: Updated point list
        """
        start_point = point_list[0]
        remove_idx = []
        prev_slope, prev_dist = sort_by_angle_and_distance(start_point, point_list[1])
        for idx, point in enumerate(point_list[2:]):
            curr_slope, curr_dist = sort_by_angle_and_distance(start_point, point)
            if curr_slope == prev_slope:
                # Taking the previous index if the slopes are identical
                # Since we are indexing from point_list[2:], need to shift the index by 2 at the end
                remove_idx.append(idx-1+2)
            prev_slope, prev_dist = curr_slope, curr_dist
        return [val for idx, val in enumerate(point_list) if idx not in remove_idx]

    def convex_hull(self):
        """
        Implementation of Convex Hull Graham's Scan
        :return: List of convex hull nodes
        """
        # Swap the lowest possible point with the first point
        idx = self.lowest_point()
        point_list = copy.deepcopy(self.point_list)
        point_list[0], point_list[idx] = point_list[idx], point_list[0]

        # Sort the rest of the point list based on angle and distance
        starting_point = point_list[0]
        point_list[1:] = sorted(point_list[1:], key=lambda p: sort_by_angle_and_distance(starting_point, p))

        # After sorted, update point list to remove points that are close and have the same angle
        updated_point_list = self.update_point_list(point_list)
        # If less than 3 points
        if len(updated_point_list) < 3:
            return None

        # Traversal the path and remove concave points
        stack = [updated_point_list[0], updated_point_list[1], updated_point_list[2]]
        stack_size = 3
        for i in range(2, len(updated_point_list)-1):
            while True:
                o = orientation(stack[stack_size - 2], stack[stack_size - 1], updated_point_list[i+1])
                if o == 2:
                    # If counterclockwise, add in that element
                    break
                else:
                    # If not counterclockwise
                    stack.pop()
                    stack_size -= 1
            stack.append(updated_point_list[i+1])
            stack_size += 1
        return stack


def sort_by_angle_and_distance(point1, point2):
    """
    Self created function prioritizing slope, then distance
    :return: Sorting function
    """
    x1, y1 = point1.x, point1.y
    x2, y2 = point2.x, point2.y
    if x2 - x1 == 0:
        slope = float('inf')
    else:
        slope = (y2 - y1) / (x2 - x1)
    dist = distance(point1, point2)
    return slope, dist


def distance(point1, point2):
    """
    Distance between point 1 and point 2
    :param point1: point 1
    :param point2: point 2
    :return: Distance between point 1 and point 2
    """
    x1, y1 = point1.x, point1.y
    x2, y2 = point2.x, point2.y
    return np.sqrt((y2 - y1) * (y2 - y1) + (x2 - x1) * (x2 - x1))


def main():
    point_list = [(0, 3), (2, 2), (1, 1), (2, 1), (3, 0), (0, 0), (3, 3)]
    convex_hull_test = ConvexHullJarvis(point_list)
    print(convex_hull_test.convex_hull())

    convex_hull_test = ConvexHullGraham(point_list)
    print(convex_hull_test.convex_hull())


if __name__ == '__main__':
    main()


