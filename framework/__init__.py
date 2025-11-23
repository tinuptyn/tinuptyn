"""Public interface for the automated testing framework."""

from .config import (
    DEFAULT_CONFIG_PATH,
    FrameworkConfig,
    IntegrationConfig,
    PerformanceConfig,
    ReportingConfig,
    RuntimeConfig,
    SuiteConfig,
    load_config,
)
from .reporters import ReportManager
from .runner import FrameworkRunner
from .types import RunResult

__all__ = [
    "DEFAULT_CONFIG_PATH",
    "FrameworkConfig",
    "SuiteConfig",
    "IntegrationConfig",
    "PerformanceConfig",
    "ReportingConfig",
    "RuntimeConfig",
    "ReportManager",
    "FrameworkRunner",
    "RunResult",
    "load_config",
]
