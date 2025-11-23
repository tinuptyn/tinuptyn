import unittest

from app import math_utils


class TestMathUtils(unittest.TestCase):
    def test_safe_divide(self):
        self.assertAlmostEqual(math_utils.safe_divide(10, 2), 5)
        with self.assertRaises(ValueError):
            math_utils.safe_divide(1, 0)

    def test_running_total(self):
        self.assertEqual(math_utils.running_total([1, 2, 3]), [1, 3, 6])

    def test_fibonacci(self):
        self.assertEqual(math_utils.fibonacci(10), 55)

    def test_compute_primes(self):
        primes = math_utils.compute_primes(30)
        self.assertIn(29, primes)
        self.assertEqual(primes[:5], [2, 3, 5, 7, 11])


if __name__ == "__main__":
    unittest.main()
