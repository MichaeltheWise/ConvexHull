from unittest import TestCase
from LineIntersectionChecker import IntersectionChecker


class TestIntersectionChecker(TestCase):
    def test_intersection_check_parallel_case(self):
        mock_checker = IntersectionChecker()
        mock_checker[1] = [(1, 1), (10, 1)]
        mock_checker[2] = [(1, 2), (10, 2)]
        self.assertEqual(False, mock_checker.intersection_check(1, 2))

    def test_intersection_check_intersect_case(self):
        mock_checker = IntersectionChecker()
        mock_checker[1] = [(10, 0), (0, 10)]
        mock_checker[2] = [(0, 0), (10, 10)]
        self.assertEqual(True, mock_checker.intersection_check(1, 2))

    def test_intersection_check_collinear_not_intersect_case(self):
        mock_checker = IntersectionChecker()
        mock_checker[1] = [(-5, -5), (0, 0)]
        mock_checker[2] = [(1, 1), (10, 10)]
        self.assertEqual(False, mock_checker.intersection_check(1, 2))

    def test_intersection_check_collinear_intersect_case(self):
        mock_checker = IntersectionChecker()
        mock_checker[1] = [(-5, -5), (0, 0)]
        mock_checker[2] = [(0, 0), (10, 10)]
        self.assertEqual(True, mock_checker.intersection_check(1, 2))

    def test_intersection_keyerror_case(self):
        mock_checker = IntersectionChecker()
        mock_checker[1] = [(-5, -5), (0, 0)]
        mock_checker[2] = [(0, 0), (10, 10)]
        with self.assertRaises(Exception):
            mock_checker.intersection_check(1, 3)

    def test_multiple_lines_intersection_check(self):
        mock_checker = IntersectionChecker()
        mock_checker[1] = [(-5, -5), (0, 0)]
        mock_checker[2] = [(1, 1), (10, 10)]
        mock_checker[3] = [(0, 0), (0, 10)]
        self.assertEqual(False, mock_checker.intersection_check(1, 2))
        self.assertEqual(True, mock_checker.intersection_check(1, 3))
        self.assertEqual(False, mock_checker.intersection_check(2, 3))
