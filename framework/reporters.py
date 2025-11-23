"""Reporting utilities for framework runs."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable, List

from .config import ReportingConfig
from .types import RunResult


class ReportManager:
    """Accumulates run results and emits console + JSON reports."""

    def __init__(self, config: ReportingConfig, *, force_console: bool | None = None, force_json: bool | None = None):
        self.console_enabled = config.console if force_console is None else force_console
        self.json_enabled = config.json if force_json is None else force_json
        self.output_dir = Path(config.output_dir)
        self.results: List[RunResult] = []

    def add_result(self, result: RunResult | None):
        if result is None:
            return
        self.results.append(result)
        if self.console_enabled:
            status = "PASS" if result.success else "FAIL"
            print(f"[{status}] {result.suite} :: total={result.total} pass={result.passed} fail={result.failed} "
                  f"errors={result.errors} skipped={result.skipped} duration={result.duration:.2f}s")

    def finalize(self):
        if self.json_enabled and self.results:
            self.output_dir.mkdir(parents=True, exist_ok=True)
            payload = {
                "results": [r.to_dict() for r in self.results],
                "success": self.all_passed,
            }
            (self.output_dir / "test-report.json").write_text(json.dumps(payload, indent=2))

    @property
    def all_passed(self) -> bool:
        return all(result.success for result in self.results)

    def extend(self, results: Iterable[RunResult | None]):
        for result in results:
            self.add_result(result)
