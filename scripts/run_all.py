from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run(step: str, cmd: list[str]) -> None:
    print(f"\n=== {step} ===")
    subprocess.run(cmd, cwd=ROOT, check=True)


def main() -> None:
    run("Validate framework", [sys.executable, "scripts/validate_framework.py"])
    run("Run Part 1 experiments", [sys.executable, "scripts/run_part1.py"])
    run("Run Part 2 experiments", [sys.executable, "scripts/run_part2.py"])
    run("Generate requirement coverage report", [sys.executable, "scripts/generate_requirement_coverage.py"])
    run("Build notebooks", [sys.executable, "scripts/build_notebooks.py"])
    print("\nAll steps completed.")


if __name__ == "__main__":
    main()
