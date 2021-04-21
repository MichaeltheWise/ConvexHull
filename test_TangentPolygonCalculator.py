from unittest import TestCase
from LineIntersectionChecker import Point
from TangentPolygonCalculator import Polygon, TangentPolygonCalculator


class TestTangentPolygonCalculator(TestCase):
    def test_upper_tangent_case1(self):
        point_list_a = [(2, 2), (3, 1), (3, 3), (5, 2), (4, 0)]
        polygon_a = Polygon(point_list_a)
        point_list_b = [(0, 1), (1, 0), (0, -2), (-1, 0)]
        polygon_b = Polygon(point_list_b)

        # After polygons are created
        mock_tangent_polygon_calculator = TangentPolygonCalculator()
        mock_tangent_polygon_calculator['a'] = polygon_a
        mock_tangent_polygon_calculator['b'] = polygon_b

        expected = [Point(0, 1), Point(3, 3)]
        self.assertCountEqual(expected, mock_tangent_polygon_calculator.upper_tangent('a', 'b'))

    def test_upper_tangent_case2(self):
        point_list_a = [(3, 1), (4, 2), (3, 3), (2, 2)]
        polygon_a = Polygon(point_list_a)
        point_list_b = [(0, 1), (0, 2), (-1, 1), (-1, 2)]
        polygon_b = Polygon(point_list_b)

        # After polygons are created
        mock_tangent_polygon_calculator = TangentPolygonCalculator()
        mock_tangent_polygon_calculator['a'] = polygon_a
        mock_tangent_polygon_calculator['b'] = polygon_b

        expected = [Point(-1, 2), Point(3, 3)]
        self.assertCountEqual(expected, mock_tangent_polygon_calculator.upper_tangent('a', 'b'))

    def test_upper_tangent_case3(self):
        point_list_a = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        polygon_a = Polygon(point_list_a)
        point_list_b = [(4, 1), (3, 3), (5, 2), (4, 4)]
        polygon_b = Polygon(point_list_b)

        # After polygons are created
        mock_tangent_polygon_calculator = TangentPolygonCalculator()
        mock_tangent_polygon_calculator['a'] = polygon_a
        mock_tangent_polygon_calculator['b'] = polygon_b

        expected = [Point(0, 1), Point(4, 4)]
        self.assertCountEqual(expected, mock_tangent_polygon_calculator.upper_tangent('a', 'b'))

    def test_lower_tangent_case1(self):
        point_list_a = [(2, 2), (3, 1), (3, 3), (5, 2), (4, 0)]
        polygon_a = Polygon(point_list_a)
        point_list_b = [(0, 1), (1, 0), (0, -2), (-1, 0)]
        polygon_b = Polygon(point_list_b)

        # After polygons are created
        mock_tangent_polygon_calculator = TangentPolygonCalculator()
        mock_tangent_polygon_calculator['a'] = polygon_a
        mock_tangent_polygon_calculator['b'] = polygon_b

        expected = [Point(0, -2), Point(4, 0)]
        self.assertCountEqual(expected, mock_tangent_polygon_calculator.lower_tangent('a', 'b'))

    def test_lower_tangent_case2(self):
        point_list_a = [(3, 1), (4, 2), (3, 3), (2, 2)]
        polygon_a = Polygon(point_list_a)
        point_list_b = [(0, 1), (0, 2), (-1, 1), (-1, 2)]
        polygon_b = Polygon(point_list_b)

        # After polygons are created
        mock_tangent_polygon_calculator = TangentPolygonCalculator()
        mock_tangent_polygon_calculator['a'] = polygon_a
        mock_tangent_polygon_calculator['b'] = polygon_b

        expected = [Point(0, 1), Point(3, 1)]
        self.assertCountEqual(expected, mock_tangent_polygon_calculator.lower_tangent('a', 'b'))

    def test_lower_tangent_case3(self):
        point_list_a = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        polygon_a = Polygon(point_list_a)
        point_list_b = [(4, 1), (3, 3), (5, 2), (4, 4)]
        polygon_b = Polygon(point_list_b)

        # After polygons are created
        mock_tangent_polygon_calculator = TangentPolygonCalculator()
        mock_tangent_polygon_calculator['a'] = polygon_a
        mock_tangent_polygon_calculator['b'] = polygon_b

        expected = [Point(0, -1), Point(4, 1)]
        self.assertCountEqual(expected, mock_tangent_polygon_calculator.lower_tangent('a', 'b'))
