# -*- coding: utf-8 -*-
"""
Created on Fri Apr 16 2021

@author: Michael Lin
"""


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "x coordinate: {}, y coordinate: {}".format(self.x, self.y)

    def __repr__(self):
        return "Point(x={}, y={})".format(self.x, self.y)


class Line:
    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2
        self.point_list = {1: point1, 2: point2}

    def __getitem__(self, key):
        try:
            return self.point_list[key]
        except KeyError:
            print("Please enter either 1 or 2 for point 1 or point 2")
            return -1

    def __str__(self):
        return "Line with point 1: {} and point 2: {}".format(str(self.point1), str(self.point2))

    def __repr__(self):
        return "Line(point1={}, point2={})".format(self.point1.__repr__(), self.point2.__repr__())


class IntersectionChecker:
    def __init__(self):
        self.line_list = {}

        # For calculation
        self.point1 = None
        self.point2 = None
        self.point3 = None
        self.point4 = None
        self.orientation_mapping = None

    def __setitem__(self, key, value):
        if isinstance(value, list) and len(value) == 2:
            point_list = []
            for point in value:
                new_point = Point(point[0], point[1])
                point_list.append(new_point)
            new_line = Line(point_list[0], point_list[1])
            self.line_list[key] = new_line
        else:
            print("Please input the line in the following format: [(p1, q1), (p2, q2)]")

    def __getitem__(self, key):
        try:
            return self.line_list[key]
        except KeyError:
            print("Line {} not inputted".format(key))
            return -1

    def set_orientation_mapping(self):
        """
        Set attribute orientation mapping
        :return: None
        """
        self.orientation_mapping = {
            0: [self.point1, self.point2, self.point3],
            1: [self.point1, self.point2, self.point4],
            2: [self.point3, self.point4, self.point1],
            3: [self.point3, self.point4, self.point2],
        }

    def intersection_check(self, key1, key2):
        """
        Check whether two lines intersect
        :param key1: 1st line
        :param key2: 2nd line
        :return: Boolean True/False
        """
        self.point1, self.point2, self.point3, self.point4 = None, None, None, None
        if key1 in self.line_list and key2 in self.line_list:
            line1 = self.line_list[key1]
            line2 = self.line_list[key2]
        else:
            # Raise exception if line doesn't exist
            print("\nPlease check whether lines exist")
            raise KeyError
            return

        self.point1 = line1[1]
        self.point2 = line1[2]
        self.point3 = line2[1]
        self.point4 = line2[2]
        self.set_orientation_mapping()

        # Calculate orientation
        o_list = [0] * 4
        for i in range(4):
            mapping = self.orientation_mapping[i]
            o_list[i] = orientation(mapping[0], mapping[1], mapping[2])

        if o_list[0] != o_list[1] and o_list[2] != o_list[3]:
            return True

        # Check collinear situation
        collinear_list = [idx for idx, x in enumerate(o_list) if x == 0]
        if collinear_list:
            for idx in collinear_list:
                mapping = self.orientation_mapping[idx]
                if collinear_check(mapping[0], mapping[1], mapping[2]):
                    return True
        return False


def orientation(point1, point2, point3):
    """
    Use the difference in slope to figure out which ways are the point 3 orients with respect to point 1 and point 2
    :param point1: point 1
    :param point2: point 2
    :param point3: point 3
    :return: 1 for clockwise, 2 for counterclockwise, 0 for collinear
    """
    x1, y1 = point1.x, point1.y
    x2, y2 = point2.x, point2.y
    x3, y3 = point3.x, point3.y
    res = (y3 - y2) * (x2 - x1) - (y2 - y1) * (x3 - x2)

    if res > 0:
        return 1
    # Instead of assigning to -1, to reduce memory usage, assign to 2 instead
    elif res < 0:
        return 2
    else:
        return res


def collinear_check(point1, point2, point3):
    """
    Check whether point 3 is on line point1-point2
    :param point1: point 1
    :param point2: point 2
    :param point3: point 3
    :return: Boolean True/False
    """
    x1, y1 = point1.x, point1.y
    x2, y2 = point2.x, point2.y
    x3, y3 = point3.x, point3.y
    # Check whether point 3 x and y coordinates are in between point 1 and point 2
    if min(x1, x2) <= x3 <= max(x1, x2) and min(y1, y2) <= y3 <= max(y1, y2):
        return True
    return False


def main():
    intersection_checker = IntersectionChecker()
    # Add line number 1
    intersection_checker[1] = [(1, 1), (10, 1)]
    # Print line 1
    print(intersection_checker[1])
    print(intersection_checker[1].__repr__())
    # Print point 1
    print(intersection_checker[1][1])
    print(intersection_checker[1][1].__repr__())
    # Print point 2
    print(intersection_checker[1][2])
    print(intersection_checker[1][2].__repr__())
    # Add line number 2
    intersection_checker[2] = [(1, 2), (10, 2)]
    print(intersection_checker[2])
    print("\nCHECK WHETHER THE TWO LINES INTERSECT: ")
    print(intersection_checker.intersection_check(1, 2))
    # print(intersection_checker.intersection_check(1, 3))
    # print(intersection_checker[1])
    # print(intersection_checker[1][3])


if __name__ == '__main__':
    main()
