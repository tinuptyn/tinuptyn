"""Common discovery and execution helpers for all suites."""

from __future__ import annotations

import io
import time
import unittest
from pathlib import Path
from typing import Dict, Optional

from ..types import RunResult


class CapturingTestResult(unittest.TextTestResult):
    """Custom TestResult that keeps structured per-test metadata."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.case_details = []
        self._case_lookup: Dict[str, Dict] = {}

    def _record(self, test: unittest.case.TestCase, status: str, message: Optional[str] = None):
        detail = {
            "test": self.getDescription(test),
            "status": status,
        }
        if message:
            detail["message"] = message
        self.case_details.append(detail)
        self._case_lookup[str(test)] = detail

    def addSuccess(self, test):  # type: ignore[override]
        super().addSuccess(test)
        self._record(test, "passed")

    def addFailure(self, test, err):  # type: ignore[override]
        super().addFailure(test, err)
        self._record(test, "failed", self._exc_info_to_string(err, test))

    def addError(self, test, err):  # type: ignore[override]
        super().addError(test, err)
        self._record(test, "error", self._exc_info_to_string(err, test))

    def addSkip(self, test, reason):  # type: ignore[override]
        super().addSkip(test, reason)
        self._record(test, "skipped", reason)

    def stopTest(self, test):  # type: ignore[override]
        detail = self._case_lookup.get(str(test))
        if detail and hasattr(test, "get_performance_samples"):
            samples = test.get_performance_samples()
            if samples:
                detail["performance"] = samples
        super().stopTest(test)


def discover_suite(path: Path, pattern: str, top_level: Optional[str]):
    loader = unittest.TestLoader()
    start_dir = str(path)
    top_level_dir = str(Path(top_level).resolve()) if top_level else None
    return loader.discover(start_dir=start_dir, pattern=pattern, top_level_dir=top_level_dir)


def run_suite(name: str, kind: str, suite: unittest.TestSuite) -> RunResult:
    buffer = io.StringIO()
    runner = unittest.TextTestRunner(
        stream=buffer,
        verbosity=2,
        failfast=False,
        resultclass=CapturingTestResult,
    )
    start = time.perf_counter()
    result: CapturingTestResult = runner.run(suite)
    elapsed = time.perf_counter() - start
    failures = len(result.failures)
    errors = len(result.errors)
    skipped = len(result.skipped)
    passed = result.testsRun - failures - errors - skipped

    return RunResult(
        suite=name,
        kind=kind,
        total=result.testsRun,
        passed=passed,
        failed=failures,
        errors=errors,
        skipped=skipped,
        duration=elapsed,
        details=result.case_details,
        logs=buffer.getvalue(),
    )
