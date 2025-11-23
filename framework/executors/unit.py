"""Unit test executor."""

from __future__ import annotations

from pathlib import Path

from ..config import SuiteConfig
from .base import discover_suite, run_suite


def run_unit_tests(config: SuiteConfig):
    if not config.enabled:
        return None

    suite = discover_suite(Path(config.path).resolve(), config.pattern, config.top_level_dir)
    return run_suite("unit", "unit", suite)
