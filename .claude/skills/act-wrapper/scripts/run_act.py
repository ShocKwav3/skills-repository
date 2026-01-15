#!/usr/bin/env python3
"""
act-wrapper: Run GitHub Actions workflows locally with filtered output.

Filters ACT's verbose infrastructure noise while preserving workflow output.
See patterns.py for filter configuration.
"""

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Iterator

# Import patterns from separate file (handle import from any directory)
sys.path.insert(0, str(Path(__file__).parent))
from patterns import HIDE_PATTERNS, KEEP_PATTERNS

# Compile patterns for performance
KEEP_REGEX = [re.compile(p, re.IGNORECASE) for p in KEEP_PATTERNS]
HIDE_REGEX = [re.compile(p, re.IGNORECASE) for p in HIDE_PATTERNS]

# ANSI color codes
class Colors:
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    RED = "\033[31m"
    RESET = "\033[0m"
    BOLD = "\033[1m"

# Check if colors should be used (tty and not disabled)
USE_COLORS = sys.stdout.isatty() and os.environ.get("NO_COLOR") is None


def colorize(line: str) -> str:
    """Apply color to line based on content."""
    if not USE_COLORS:
        return line

    # Success indicators (green)
    if "✅" in line or "Job succeeded" in line or "PASSED" in line:
        return f"{Colors.GREEN}{line}{Colors.RESET}"

    # Hard failures (red) - actual workflow/job failures
    if "❌" in line or "Job failed" in line or "FAILED" in line or "Error:" in line:
        return f"{Colors.RED}{line}{Colors.RESET}"

    # Warnings and lint summaries (yellow) - needs attention but not broken
    if (
        "level=warning" in line
        or "⚠" in line
        or "warning:" in line.lower()
        or re.search(r"Found \d+ errors?", line)  # Lint error summaries
    ):
        return f"{Colors.YELLOW}{line}{Colors.RESET}"

    return line


def should_show_line(line: str, verbose: bool = False) -> bool:
    """Determine if a line should be shown in output."""
    if verbose:
        return True

    if not line.strip():
        return False

    # KEEP patterns have priority (ensures errors always show)
    for pattern in KEEP_REGEX:
        if pattern.search(line):
            return True

    # HIDE patterns filter noise
    for pattern in HIDE_REGEX:
        if pattern.search(line):
            return False

    # Default: show the line
    return True


def filter_output(lines: Iterator[str], verbose: bool = False) -> Iterator[str]:
    """Filter act output lines."""
    for line in lines:
        if should_show_line(line, verbose):
            yield line


def run_act(workflow_file: str, verbose: bool = False, act_args: str = "") -> int:
    """Run act with filtered output."""
    cmd = ["act", "-W", workflow_file]
    if act_args:
        cmd.extend(act_args.split())

    print(f"Running: {' '.join(cmd)}")
    print("=" * 60)

    try:
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
        )

        job_failed = False
        for line in filter_output(iter(process.stdout.readline, ""), verbose):
            print(colorize(line), end="")
            if "Job failed" in line or "❌" in line:
                job_failed = True

        process.wait()
        print("=" * 60)

        if process.returncode != 0 or job_failed:
            print(f"{Colors.RED}Result: FAILED{Colors.RESET}" if USE_COLORS else "Result: FAILED")
            return 1
        print(f"{Colors.GREEN}Result: PASSED{Colors.RESET}" if USE_COLORS else "Result: PASSED")
        return 0

    except FileNotFoundError:
        print("Error: 'act' not found. Install: brew install act")
        return 1
    except KeyboardInterrupt:
        print("\nInterrupted")
        return 130


def main():
    parser = argparse.ArgumentParser(
        description="Run GitHub Actions workflows locally with filtered output"
    )
    parser.add_argument("workflow", help="Path to workflow file")
    parser.add_argument("-v", "--verbose", action="store_true", help="Show all output")
    parser.add_argument("--act-args", default="", help="Additional act arguments")

    args = parser.parse_args()
    sys.exit(run_act(args.workflow, args.verbose, args.act_args))


if __name__ == "__main__":
    main()
