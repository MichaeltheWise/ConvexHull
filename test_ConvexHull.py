from unittest import TestCase
from LineIntersectionChecker import Point
from ConvexHull import sort_by_angle_and_distance, ConvexHullJarvis, ConvexHullGraham


class TestSort(TestCase):
    def test_sort_by_angle_and_distance(self):
        mock_point_list = [Point(0, 0), Point(2, 2), Point(1, 1), Point(2, 1), Point(3, 0), Point(0, 3), Point(3, 3)]
        mock_point_list[1:] = sorted(mock_point_list[1:],
                                     key=lambda p: sort_by_angle_and_distance(mock_point_list[0], p))
        expected = [Point(0, 0), Point(3, 0), Point(2, 1), Point(1, 1), Point(2, 2), Point(3, 3), Point(0, 3)]
        self.assertEqual(expected, mock_point_list)

    def test_convex_hull_algos_output_simple_case(self):
        point_list = [(0, 3), (2, 2), (1, 1), (2, 1), (3, 0), (0, 0), (3, 3)]
        # Convex Hull Jarvis Algorithm
        mock_convex_hull_jarvis = ConvexHullJarvis(point_list)
        convex_hull_jarvis_output = mock_convex_hull_jarvis.convex_hull()

        # Convex Hull Graham Scan
        mock_convex_full_graham = ConvexHullGraham(point_list)
        convex_hull_graham_output = mock_convex_full_graham.convex_hull()

        # Correct output: [Point(x=0, y=0), Point(x=3, y=0), Point(x=3, y=3), Point(x=0, y=3)]
        self.assertCountEqual(convex_hull_jarvis_output, convex_hull_graham_output)

    def test_convex_hull_algos_output_complicated_case(self):
        point_list = [(0, 0), (1, 4), (3, 3), (3, 1), (5, 5), (5, 2), (7, 0), (9, 6)]
        # Convex Hull Jarvis Algorithm
        mock_convex_hull_jarvis = ConvexHullJarvis(point_list)
        convex_hull_jarvis_output = mock_convex_hull_jarvis.convex_hull()

        # Convex Hull Graham Scan
        mock_convex_hull_graham = ConvexHullGraham(point_list)
        convex_hull_graham_output = mock_convex_hull_graham.convex_hull()

        # Correct output: [Point(x=0, y=0), Point(x=7, y=0), Point(x=9, y=6), Point(x=1, y=4)
        self.assertCountEqual(convex_hull_jarvis_output, convex_hull_graham_output)


class TestConvexHullJarvis(TestCase):
    def test_convex_hull_jarvis_simple_case(self):
        point_list = [(0, 3), (2, 2), (1, 1), (2, 1), (3, 0), (0, 0), (3, 3)]
        # Convex Hull Jarvis Algorithm
        mock_convex_hull_jarvis = ConvexHullJarvis(point_list)
        convex_hull_jarvis_output = mock_convex_hull_jarvis.convex_hull()
        expected = [Point(0, 0), Point(0, 3), Point(3, 3), Point(3, 0)]
        self.assertCountEqual(expected, convex_hull_jarvis_output)

    def test_convex_hull_jarvis_complicated_case(self):
        point_list = [(0, 0), (1, 4), (3, 3), (3, 1), (5, 5), (5, 2), (7, 0), (9, 6)]
        # Convex Hull Jarvis Algorithm
        mock_convex_hull_jarvis = ConvexHullJarvis(point_list)
        convex_hull_jarvis_output = mock_convex_hull_jarvis.convex_hull()
        expected = [Point(0, 0), Point(7, 0), Point(9, 6), Point(1, 4)]
        self.assertCountEqual(expected, convex_hull_jarvis_output)


class TestConvexHullGraham(TestCase):
    def test_convex_hull_jarvis_simple_case(self):
        point_list = [(0, 3), (2, 2), (1, 1), (2, 1), (3, 0), (0, 0), (3, 3)]
        # Convex Hull Graham Scan
        mock_convex_hull_graham = ConvexHullGraham(point_list)
        convex_hull_graham_output = mock_convex_hull_graham.convex_hull()
        expected = [Point(0, 0), Point(0, 3), Point(3, 3), Point(3, 0)]
        self.assertCountEqual(expected, convex_hull_graham_output)

    def test_convex_hull_jarvis_complicated_case(self):
        point_list = [(0, 0), (1, 4), (3, 3), (3, 1), (5, 5), (5, 2), (7, 0), (9, 6)]
        # Convex Hull Graham Scan
        mock_convex_hull_graham = ConvexHullGraham(point_list)
        convex_hull_graham_output = mock_convex_hull_graham.convex_hull()
        expected = [Point(0, 0), Point(7, 0), Point(9, 6), Point(1, 4)]
        self.assertCountEqual(expected, convex_hull_graham_output)