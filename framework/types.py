"""Shared data structures used across the framework."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class RunResult:
    suite: str
    kind: str
    total: int
    passed: int
    failed: int
    errors: int
    skipped: int
    duration: float
    details: List[Dict[str, Any]] = field(default_factory=list)
    logs: str = ""

    @property
    def success(self) -> bool:
        return self.failed == 0 and self.errors == 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "suite": self.suite,
            "kind": self.kind,
            "total": self.total,
            "passed": self.passed,
            "failed": self.failed,
            "errors": self.errors,
            "skipped": self.skipped,
            "duration": self.duration,
            "success": self.success,
            "details": self.details,
            "logs": self.logs,
        }
