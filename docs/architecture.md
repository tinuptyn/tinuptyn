# Automated Testing Framework Architecture

## Goals

- Offer a unified entry point for unit, integration, and performance testing.
- Keep framework configuration-driven so it can be dropped into any medium-sized service.
- Produce repeatable, machine-readable reports suitable for CI pipelines.
- Provide extension hooks for future capabilities (coverage, lint, contract tests, etc.).

## Key Components

### Configuration (`framework/config.py`)
- YAML-based (`configs/framework.yml`).
- Captures suite discovery paths, filename patterns, service dependencies, performance thresholds, and reporting targets.
- Runtime section applies environment variables and `PYTHONPATH` updates before executing tests.

### Executors (`framework/executors/*`)
- **Unit**: straightforward `unittest` discovery using configured pattern.
- **Integration**: wraps execution in a lightweight service manager so you can provision/teardown containers or remote fixtures.
- **Performance**: ships a `PerformanceTestCase` with `assertPerformance` helper that warms caches, captures stats, and enforces thresholds.

### Runner (`framework/runner.py`)
- Expands requested target (`unit`, `integration`, `performance`, or `all`).
- Calls executors sequentially and pushes `RunResult` objects into the reporter.
- Supports `--skip-services` to bypass dependency startup when infra is pre-baked (e.g., CI with shared databases).

### Reporter (`framework/reporters.py`)
- Streams concise status lines to stdout for humans.
- Emits a JSON artifact (`artifacts/test-report.json`) for machines.
- Normalizes result objects so additional reporters (JUnit XML, Slack, etc.) can be plugged in later.

### CLI (`run_tests.py`)
- Parses user intent, loads config, applies runtime, and triggers `FrameworkRunner`.
- Exposes switches to disable console/json output, choose suite types, and skip integration services.

## Extensibility Ideas

- Add coverage integration by wrapping unit executor with `coverage.py`.
- Implement async integration services that run `docker compose up` and watch health checks.
- Provide Prometheus-friendly metrics emission for performance runs.
- Support parallel execution using `concurrent.futures` for large suites.

## Development Workflow

1. Update or copy `configs/framework.yml` for your project.
2. Implement tests under `tests/unit|integration|performance`.
3. Run `python run_tests.py --type all` locally.
4. Wire `run-tests` CLI into CI (e.g., GitHub Actions) to keep stages consistent across environments.
