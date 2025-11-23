## Automated Testing Framework

This repository contains a complete, batteries-included automated testing framework designed for medium-sized Python projects. The framework unifies unit, integration, and performance testing under a single configuration-driven workflow, making it easy to standardize quality gates without wiring together bespoke scripts per project.

### Highlights

- Single entry point via `run_tests.py` or the `run-tests` console script.
- Configuration as code (`configs/framework.yml`) to control discovery paths, naming conventions, runtime env vars, test selection, and performance thresholds.
- Structured reporting with console and machine-readable JSON summaries (ready for CI artifacts).
- Extensible executors for unit, integration, and performance suites, each with pluggable hooks.
- Sample application & tests that illustrate recommended project layout and how to author each test flavor.

### Repository Layout

- `app/`: Sample production code under test.
- `framework/`: Core testing framework modules (config parsing, runners, reporters, executors).
- `tests/`: Three suites (`unit`, `integration`, `performance`) showcasing framework capabilities.
- `configs/framework.yml`: Centralized knobs for discovery, reporting, env, and perf thresholds.
- `docs/architecture.md`: Deep dive into design decisions, extension points, and roadmap ideas.

### Quick Start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
python run_tests.py --type all
```

The command above runs unit, integration, and performance suites, emits console summaries, and writes structured reports to `artifacts/test-report.json`.

Head over to `docs/architecture.md` for a detailed walkthrough of the framework internals and guidance on adapting it to your own services.
