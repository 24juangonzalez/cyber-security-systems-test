"""Beginner launcher: python development.py (macOS, Linux, or Windows)."""

import argparse
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Start the local demo using the locked project environment."
    )
    parser.add_argument(
        "--check", action="store_true", help="Run lint, formatting checks, and tests."
    )
    args = parser.parse_args()
    uv = shutil.which("uv")
    if uv is None:
        print(
            "Setup needed: uv was not found. Install it using the instructions at\n"
            "https://docs.astral.sh/uv/getting-started/installation/\n"
            "Then reopen your terminal and run this command again."
        )
        return 1

    if args.check:
        commands = [
            ["ruff", "check", "."],
            ["ruff", "format", "--check", "."],
            ["pytest"],
        ]
        print(
            "Checking code style and running the tests. Files will not be formatted.",
            flush=True,
        )
    else:
        commands = [
            [
                "streamlit",
                "run",
                "streamlit_app.py",
                "--server.address",
                "127.0.0.1",
            ]
        ]
        print(
            "Starting the local demo. First run may download Python and dependencies.\n"
            "Open the local URL printed by Streamlit. Stop with Ctrl+C.\n"
            "In the app, choose Bundled demo, then Run analysis.\n"
            "Use synthetic examples only; customer data is not supported.",
            flush=True,
        )
    try:
        for command in commands:
            completed = subprocess.run(
                [uv, "run", "--locked", "--group", "dev", "--extra", "ui", *command],
                cwd=ROOT,
                check=False,
            )
            if completed.returncode:
                print("The command did not finish successfully. See the error above.")
                return completed.returncode
    except KeyboardInterrupt:
        print("\nStopped. You can restart with the same command.")
        return 130
    except OSError:
        print(
            "Could not start uv. Check its installation and your terminal permissions."
        )
        return 1
    if args.check:
        print("All development checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
