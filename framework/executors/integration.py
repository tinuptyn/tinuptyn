"""Integration test executor with basic service hooks."""

from __future__ import annotations

import contextlib
import time
from pathlib import Path
from typing import Dict, Iterable

from ..config import IntegrationConfig
from ..types import RunResult
from .base import discover_suite, run_suite


class IntegrationServiceManager(contextlib.AbstractContextManager):
    """Lightweight stub that represents lifecycle hooks for external services."""

    def __init__(self, services: Iterable[Dict[str, str]], startup_timeout: float):
        self.services = list(services)
        self.startup_timeout = startup_timeout

    def __enter__(self):
        for svc in self.services:
            name = svc.get("name", "service")
            print(f"[integration] prepared '{name}' (command={svc.get('start_cmd', 'n/a')})")
            time.sleep(0.01)  # simulate a short setup delay without real side effects
        return self

    def __exit__(self, exc_type, exc, tb):
        for svc in reversed(self.services):
            name = svc.get("name", "service")
            print(f"[integration] tore down '{name}'")
        return False


def run_integration_tests(config: IntegrationConfig, *, skip_services: bool = False) -> RunResult | None:
    if not config.enabled:
        return None

    suite = discover_suite(Path(config.path).resolve(), config.pattern, config.top_level_dir)

    if skip_services or not config.services:
        return run_suite("integration", "integration", suite)

    with IntegrationServiceManager(config.services, config.startup_timeout):
        return run_suite("integration", "integration", suite)
