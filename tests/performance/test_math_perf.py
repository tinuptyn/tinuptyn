from framework.executors.performance import PerformanceTestCase
from app import math_utils


class TestMathPerformance(PerformanceTestCase):
    def test_prime_sieve_is_within_threshold(self):
        self.assertPerformance(math_utils.compute_primes, 10_000, threshold_ms=200, repeats=5, warmup_iterations=1,
                               label="prime-sieve-10k")

    def test_fibonacci_cache_keeps_calls_fast(self):
        # warm cache first
        math_utils.fibonacci(30)
        self.assertPerformance(math_utils.fibonacci, 30, threshold_ms=5, repeats=10, warmup_iterations=0,
                               label="fibonacci-30-cached")
