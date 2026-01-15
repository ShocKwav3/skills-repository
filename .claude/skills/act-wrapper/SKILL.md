---
name: act-wrapper
description: Run GitHub Actions workflows locally using nektos/act with filtered output. Use when testing or debugging GitHub Actions workflows locally. Provides cleaner output by filtering ACT's infrastructure noise (docker operations, action cloning, internal commands) while preserving all actual workflow output. Language and ecosystem agnostic.
---

# Act Wrapper

Run GitHub Actions workflows locally with filtered output using nektos/act.

## Usage

Run the wrapper script with a workflow file path:

```bash
python3 .claude/skills/act-wrapper/scripts/run_act.py <workflow-file> [options]
```

### Options

- `--verbose, -v`: Show all output without filtering
- `--act-args ARGS`: Pass additional arguments to act (e.g., `--container-architecture linux/amd64`)

### Examples

```bash
# Run a workflow with filtered output
python3 .claude/skills/act-wrapper/scripts/run_act.py .github/workflows/ci.yml

# Run with full verbose output
python3 .claude/skills/act-wrapper/scripts/run_act.py .github/workflows/test.yml --verbose

# Pass additional act arguments
python3 .claude/skills/act-wrapper/scripts/run_act.py .github/workflows/build.yml --act-args "--container-architecture linux/amd64"
```

## What Gets Filtered

The wrapper removes ACT's internal infrastructure noise while preserving all actual workflow output:

**Filtered (hidden):**
- Docker operations (pull, create, run, exec, cp)
- Action cloning messages
- GitHub Actions internal commands (set-env, set-output, add-path)
- Container chown operations
- Problem matcher additions
- Container cleanup messages

**Always shown:**
- Step start markers (Run...)
- Step results (Success/Failure)
- Matrix configuration
- Job completion status
- All actual command output from workflow steps
- Error messages

## Exit Codes

- `0`: All jobs succeeded
- `1`: One or more jobs failed
- `130`: Interrupted by user (Ctrl+C)

## Progressive Development

Filter patterns are in `scripts/patterns.py` (separate from the main script to minimize context).

When you encounter verbose output that should be filtered:

1. Read only `scripts/patterns.py`
2. Add a new regex to `HIDE_PATTERNS`
3. Keep patterns generic when possible
4. Add a comment explaining what it matches

Example - for noisy lines like `| Fetching crate metadata...`:
```python
r"\|\s+Fetching crate metadata",  # Cargo fetch progress
```

Do NOT read `run_act.py` unless you need to modify the core logic.

## Requirements

- nektos/act must be installed: `brew install act` (macOS)
- Docker must be running
