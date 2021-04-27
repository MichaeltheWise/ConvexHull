# -*- coding: utf-8 -*-
"""
Created on Tue Apr 27 2021

@author: Michael Lin
"""
import multiprocessing
import time

from TwoLinesIntersectionCheck.ConvexHullAdvanced import ConvexHullDivideNConquer


class Process(multiprocessing.Process):
    def __init__(self, id_num, point_list=[]):
        super(Process, self).__init__()
        self.id = id_num
        self.point_list = point_list

    @property
    def point_list(self):
        return self._point_list

    @point_list.setter
    def point_list(self, val):
        if isinstance(val, list):
            self._point_list = val
        else:
            raise AttributeError("Need to be a list")

    def run(self):
        print("Process {0} started as {1}".format(self.id, multiprocessing.current_process))
        # To simulate a much more complicated process
        time.sleep(1)
        if self.point_list is None:
            print("Process {} is not calculated".format(self.id))
            return
        # Run convex hull
        convex_hull = ConvexHullDivideNConquer(self.point_list)
        res = convex_hull.convex_hull()
        if res:
            print("Result {}".format(res))
            print("Process {} is done".format(self.id))


def main():
    processes = Process(0), Process(1), Process(2)
    point_list_dict = {
        0: [(0, 3), (2, 2), (1, 1), (2, 1), (3, 0), (0, 0), (3, 3)],
        1: [(0, 0), (1, 4), (3, 3), (3, 1), (5, 5), (5, 2), (7, 0), (9, 6)],
        2: [(0, 0), (1, -4), (-1, -5), (-5, -3), (-3, -1), (-1, -3), (-2, -2), (-1, -1), (-2, -1), (-1, 1)],
    }
    for p in processes:
        if p.id in point_list_dict:
            p.point_list = point_list_dict[p.id]
            p.start()


if __name__ == "__main__":
    main()
