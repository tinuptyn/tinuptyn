"""CLI entry point for running the automated testing framework."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from framework import DEFAULT_CONFIG_PATH, FrameworkRunner, ReportManager, load_config


def apply_runtime(runtime_cfg):
    for key, value in runtime_cfg.env.items():
        os.environ[key] = value
    for path in runtime_cfg.pythonpath:
        abs_path = str((Path(path)).resolve())
        if abs_path not in sys.path:
            sys.path.insert(0, abs_path)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Automated testing framework runner")
    parser.add_argument("--config", default=str(DEFAULT_CONFIG_PATH), help="Path to framework YAML config")
    parser.add_argument("--type", choices=["unit", "integration", "performance", "all"], default="all",
                        help="Suite to execute")
    parser.add_argument("--no-console", action="store_true", help="Disable console reporter output")
    parser.add_argument("--no-json", action="store_true", help="Disable JSON artifact emission")
    parser.add_argument("--skip-services", action="store_true",
                        help="Skip integration service startup (useful for CI that pre-provisions deps)")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    config = load_config(args.config)
    apply_runtime(config.runtime)

    reporter = ReportManager(
        config.reporting,
        force_console=not args.no_console,
        force_json=not args.no_json,
    )

    runner = FrameworkRunner(config)
    success = runner.run(args.type, reporter, skip_services=args.skip_services)
    return 0 if success else 1


if __name__ == "__main__":
    raise SystemExit(main())
