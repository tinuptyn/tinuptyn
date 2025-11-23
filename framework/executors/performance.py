"""Performance test executor and helper base classes."""

from __future__ import annotations

import statistics
import time
import unittest
from pathlib import Path
from typing import Any, Dict, List, Optional

from ..config import PerformanceConfig
from ..types import RunResult
from .base import discover_suite, run_suite


class PerformanceTestCase(unittest.TestCase):
    """TestCase with helpers for measuring runtime characteristics."""

    performance_defaults = {
        "repeats": 5,
        "warmup_iterations": 1,
        "threshold_ms": 150.0,
    }

    def setUp(self):  # type: ignore[override]
        self._performance_samples: List[Dict[str, Any]] = []
        return super().setUp()

    # Using snake_case for clarity even though unittest prefers camelCase.
    def assertPerformance(self, func, *args, threshold_ms: Optional[float] = None, repeats: Optional[int] = None,
                          warmup_iterations: Optional[int] = None, label: Optional[str] = None, **kwargs):
        repeats = repeats or self.performance_defaults.get("repeats", 5)
        warmup_iterations = warmup_iterations or self.performance_defaults.get("warmup_iterations", 1)
        threshold_ms = threshold_ms or self.performance_defaults.get("threshold_ms", 150.0)

        for _ in range(warmup_iterations):
            func(*args, **kwargs)

        samples: List[float] = []
        for _ in range(repeats):
            start = time.perf_counter()
            func(*args, **kwargs)
            samples.append((time.perf_counter() - start) * 1000)

        avg = statistics.fmean(samples)
        sorted_samples = sorted(samples)
        p95_index = max(int(0.95 * (len(sorted_samples) - 1)), 0)
        p95 = sorted_samples[p95_index]
        entry = {
            "label": label or func.__name__,
            "samples": samples,
            "average_ms": avg,
            "max_ms": max(samples),
            "p95_ms": p95,
            "threshold_ms": threshold_ms,
        }
        self._performance_samples.append(entry)
        self.assertLessEqual(avg, threshold_ms,
                             msg=f"Average {avg:.2f}ms exceeded threshold {threshold_ms:.2f}ms for {entry['label']}")

    def get_performance_samples(self):
        return getattr(self, "_performance_samples", [])


def _apply_performance_defaults(suite: unittest.TestSuite, defaults: dict[str, float | int]):
    for test in suite:
        if isinstance(test, unittest.TestSuite):
            _apply_performance_defaults(test, defaults)
        elif isinstance(test, PerformanceTestCase):
            test.performance_defaults = defaults


def run_performance_tests(config: PerformanceConfig) -> RunResult | None:
    if not config.enabled:
        return None

    suite = discover_suite(Path(config.path).resolve(), config.pattern, config.top_level_dir)
    defaults = {
        "repeats": config.defaults.repeats,
        "warmup_iterations": config.defaults.warmup_iterations,
        "threshold_ms": config.defaults.threshold_ms,
    }
    _apply_performance_defaults(suite, defaults)
    return run_suite("performance", "performance", suite)
