"""High-level orchestration for running configured suites."""

from __future__ import annotations

from dataclasses import replace
from typing import List

from .config import FrameworkConfig, IntegrationConfig
from .reporters import ReportManager
from .types import RunResult
from .executors import run_integration_tests, run_performance_tests, run_unit_tests


class FrameworkRunner:
    """Coordinate suite execution according to config and CLI selection."""

    def __init__(self, config: FrameworkConfig):
        self.config = config

    def run(self, target: str, reporter: ReportManager, *, skip_services: bool = False) -> bool:
        targets = self._expand_target(target)
        results: List[RunResult | None] = []

        if "unit" in targets:
            results.append(run_unit_tests(self.config.unit))

        if "integration" in targets:
            integration_cfg: IntegrationConfig = self.config.integration
            if skip_services and integration_cfg.services:
                integration_cfg = replace(integration_cfg, services=[])
            results.append(run_integration_tests(integration_cfg, skip_services=skip_services))

        if "performance" in targets:
            results.append(run_performance_tests(self.config.performance))

        reporter.extend(results)
        reporter.finalize()
        return reporter.all_passed

    @staticmethod
    def _expand_target(target: str) -> List[str]:
        if target == "all":
            return ["unit", "integration", "performance"]
        return [target]
