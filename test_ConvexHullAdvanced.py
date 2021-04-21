from unittest import TestCase
from ConvexHull import ConvexHullJarvis, ConvexHullGraham
from ConvexHullAdvanced import ConvexHullDivideNConquer


class TestConvexHullDivideNConquer(TestCase):
    def test_convex_hull_simple_case(self):
        point_list = [(0, 3), (2, 2), (1, 1), (2, 1), (3, 0), (0, 0), (3, 3)]
        # Convex Hull Jarvis Algorithm
        mock_convex_hull_jarvis = ConvexHullJarvis(point_list)
        convex_hull_jarvis_output = mock_convex_hull_jarvis.convex_hull()

        # Convex Hull Divide and Conquer
        mock_convex_full_dnc = ConvexHullDivideNConquer(point_list)
        convex_hull_dnc_output = mock_convex_full_dnc.convex_hull()

        # Correct output: [Point(x=0, y=0), Point(x=3, y=0), Point(x=3, y=3), Point(x=0, y=3)]
        self.assertCountEqual(convex_hull_jarvis_output, convex_hull_dnc_output)

    def test_convex_hull_complicated_case1(self):
        point_list = [(0, 0), (1, 4), (3, 3), (3, 1), (5, 5), (5, 2), (7, 0), (9, 6)]
        # Convex Hull Jarvis Algorithm
        mock_convex_hull_jarvis = ConvexHullJarvis(point_list)
        convex_hull_jarvis_output = mock_convex_hull_jarvis.convex_hull()

        # Convex Hull Divide and Conquer
        mock_convex_full_dnc = ConvexHullDivideNConquer(point_list)
        convex_hull_dnc_output = mock_convex_full_dnc.convex_hull()

        # Correct output: [Point(x=0, y=0), Point(x=7, y=0), Point(x=9, y=6), Point(x=1, y=4)
        self.assertCountEqual(convex_hull_jarvis_output, convex_hull_dnc_output)

    def test_convex_hull_complicated_case2(self):
        point_list = [(0, 0), (1, -4), (-1, -5), (-5, -3), (-3, -1), (-1, -3), (-2, -2), (-1, -1), (-2, -1), (-1, 1)]
        # Convex Hull Jarvis Algorithm
        mock_convex_hull_jarvis = ConvexHullJarvis(point_list)
        convex_hull_jarvis_output = mock_convex_hull_jarvis.convex_hull()

        # Convex Hull Divide and Conquer
        mock_convex_full_dnc = ConvexHullDivideNConquer(point_list)
        convex_hull_dnc_output = mock_convex_full_dnc.convex_hull()

        # Correct output: [Point(x=0, y=0), Point(x=-1, y=1), Point(x=-5, y=-3), Point(x=-1, y=-5), Point(x=1, y=-4)
        self.assertCountEqual(convex_hull_jarvis_output, convex_hull_dnc_output)