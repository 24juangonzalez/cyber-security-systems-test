"""Offline synthetic prototype entry point."""

import argparse
import json
import sys
from pathlib import Path

from cyber_security_systems.analysis.engine import analyze, compare
from cyber_security_systems.ingestion.fixtures import FixtureError, load_fixture
from cyber_security_systems.normalization.inventory import inventory_issues
from cyber_security_systems.reporting.reports import write_reports


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Analyze declared synthetic industrial fixtures locally."
    )
    commands = parser.add_subparsers(dest="command", required=True)
    validate = commands.add_parser("validate")
    validate.add_argument("fixture", type=Path)
    analysis = commands.add_parser("analyze")
    analysis.add_argument("fixture", type=Path)
    analysis.add_argument("--output", required=True, type=Path)
    comparison = commands.add_parser("compare")
    comparison.add_argument("before", type=Path)
    comparison.add_argument("after", type=Path)
    comparison.add_argument("--output", required=True, type=Path)
    args = parser.parse_args(argv)
    try:
        if args.command == "validate":
            snapshot = load_fixture(args.fixture)
            issues = inventory_issues(snapshot)
            print(
                json.dumps(
                    {
                        "valid": True,
                        "status": "incomplete_analysis" if issues else "complete",
                        "issues": issues,
                    }
                )
            )
            return 3 if issues else 0
        if args.command == "analyze":
            result = analyze(load_fixture(args.fixture))
        else:
            result = compare(load_fixture(args.before), load_fixture(args.after))
        write_reports(result, args.output)
        status = result.get("comparison_status", result["status"])
        print(json.dumps({"status": status, "findings": len(result["findings"])}))
        return 3 if status == "incomplete_analysis" else 0
    except FixtureError as error:
        print("Invalid fixture: " + str(error), file=sys.stderr)
        return 2
    except OSError:
        print(
            (
                "Cannot write reports; use a new directory under an existing "
                "writable parent. A failed write may leave partial output."
            ),
            file=sys.stderr,
        )
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
