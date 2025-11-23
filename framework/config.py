"""Configuration models and helpers for the testing framework."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional

import yaml

DEFAULT_CONFIG_PATH = Path("configs/framework.yml")


@dataclass
class SuiteConfig:
    """Base configuration shared by test suites."""

    enabled: bool = True
    path: str = "tests"
    pattern: str = "test_*.py"
    top_level_dir: Optional[str] = None

    def absolute_path(self, base: Optional[Path] = None) -> Path:
        base_path = base or Path.cwd()
        return (base_path / self.path).resolve()


@dataclass
class IntegrationConfig(SuiteConfig):
    """Integration-suite configuration, including external services."""

    services: List[Dict[str, str]] = field(default_factory=list)
    startup_timeout: float = 30.0


@dataclass
class PerformanceDefaults:
    repeats: int = 5
    warmup_iterations: int = 1
    threshold_ms: float = 150.0


@dataclass
class PerformanceConfig(SuiteConfig):
    defaults: PerformanceDefaults = field(default_factory=PerformanceDefaults)


@dataclass
class ReportingConfig:
    console: bool = True
    json: bool = True
    output_dir: str = "artifacts"


@dataclass
class RuntimeConfig:
    env: Dict[str, str] = field(default_factory=dict)
    pythonpath: List[str] = field(default_factory=list)


@dataclass
class FrameworkConfig:
    project_name: str
    unit: SuiteConfig
    integration: IntegrationConfig
    performance: PerformanceConfig
    reporting: ReportingConfig
    runtime: RuntimeConfig


def _suite_from_dict(data: Dict, *, default_path: str) -> SuiteConfig:
    return SuiteConfig(
        enabled=data.get("enabled", True),
        path=data.get("path", default_path),
        pattern=data.get("pattern", "test_*.py"),
        top_level_dir=data.get("top_level_dir"),
    )


def _integration_from_dict(data: Dict) -> IntegrationConfig:
    base = _suite_from_dict(data, default_path="tests/integration")
    return IntegrationConfig(
        enabled=base.enabled,
        path=base.path,
        pattern=base.pattern,
        top_level_dir=base.top_level_dir,
        services=data.get("services", []),
        startup_timeout=float(data.get("startup_timeout", 30.0)),
    )


def _performance_from_dict(data: Dict) -> PerformanceConfig:
    base = _suite_from_dict(data, default_path="tests/performance")
    defaults = data.get("defaults", {})
    perf_defaults = PerformanceDefaults(
        repeats=int(defaults.get("repeats", 5)),
        warmup_iterations=int(defaults.get("warmup_iterations", 1)),
        threshold_ms=float(defaults.get("threshold_ms", 150.0)),
    )
    return PerformanceConfig(
        enabled=base.enabled,
        path=base.path,
        pattern=base.pattern,
        top_level_dir=base.top_level_dir,
        defaults=perf_defaults,
    )


def _reporting_from_dict(data: Dict) -> ReportingConfig:
    return ReportingConfig(
        console=data.get("console", True),
        json=data.get("json", True),
        output_dir=data.get("output_dir", "artifacts"),
    )


def _runtime_from_dict(data: Dict) -> RuntimeConfig:
    return RuntimeConfig(
        env=data.get("env", {}),
        pythonpath=data.get("pythonpath", []),
    )


def load_config(path: Path | str) -> FrameworkConfig:
    """Load framework configuration from a YAML file."""

    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Configuration file not found: {path}")

    raw = yaml.safe_load(path.read_text()) or {}

    project_name = raw.get("project", {}).get("name", "unknown-project")
    unit_cfg = _suite_from_dict(raw.get("unit", {}), default_path="tests/unit")
    integration_cfg = _integration_from_dict(raw.get("integration", {}))
    performance_cfg = _performance_from_dict(raw.get("performance", {}))
    reporting_cfg = _reporting_from_dict(raw.get("reporting", {}))
    runtime_cfg = _runtime_from_dict(raw.get("runtime", {}))

    return FrameworkConfig(
        project_name=project_name,
        unit=unit_cfg,
        integration=integration_cfg,
        performance=performance_cfg,
        reporting=reporting_cfg,
        runtime=runtime_cfg,
    )
