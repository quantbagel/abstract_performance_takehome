"""Check organizer-owned paths against the immutable take-home starter (read-only)."""

import argparse
import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

PROTECTED_PATHS = (
    "agent-harness/",
    "baseline/",
    "benchmarks/",
    "tools/",
    "tests/",
    ".pi/",
    ".github/",
    ".gitignore",
    ".gitattributes",
    ".gitmodules",
    ".dockerignore",
    "pyproject.toml",
    "uv.lock",
    "budgets.toml",
)


@dataclass
class IntegrityResult:
    baseline_commit: str
    changed_paths: list[str]
    added_paths: list[str]

    @property
    def clean(self) -> bool:
        return not self.changed_paths and not self.added_paths


def _git(repo: Path, *args: str) -> bytes:
    result = subprocess.run(
        ["git", "--literal-pathspecs", "-C", str(repo), *args],
        capture_output=True,
        check=False,
    )
    if result.returncode:
        raise ValueError(result.stderr.decode(errors="replace").strip() or "Git command failed")
    return result.stdout


def _paths(output: bytes) -> set[str]:
    return {os.fsdecode(path) for path in output.split(b"\0") if path}


def _python_cache(path: str) -> bool:
    item = Path(path)
    return item.parent.name == "__pycache__" and item.suffix in {".pyc", ".pyo"}


def check_integrity(repo: Path, base: str = "takehome-start") -> IntegrityResult:
    if not base or base.startswith("-"):
        raise ValueError("Provide the organizer's starter ref or commit, not a Git option")
    root = Path(os.fsdecode(_git(repo, "rev-parse", "--show-toplevel")).strip())
    commit = _git(root, "rev-parse", "--verify", "--end-of-options", f"{base}^{{commit}}")
    baseline = commit.decode("ascii").strip()
    changed: set[str] = set()
    # Check each snapshot so restoring the worktree cannot hide a modified index/HEAD.
    for snapshot in ((baseline, "HEAD"), ("--cached", baseline), (baseline,)):
        changed.update(
            _paths(
                _git(
                    root,
                    "diff",
                    "--no-ext-diff",
                    "--no-textconv",
                    "--no-renames",
                    "--ignore-submodules=none",
                    "--name-only",
                    "-z",
                    *snapshot,
                    "--",
                    *PROTECTED_PATHS,
                )
            )
        )
    # Deliberately omit --exclude-standard: ignore rules must not hide new protected files.
    added = _paths(_git(root, "ls-files", "--others", "-z", "--", *PROTECTED_PATHS))
    added = {path for path in added if not _python_cache(path)}
    return IntegrityResult(baseline, sorted(changed), sorted(added))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", default="takehome-start", help="immutable organizer starter ref")
    parser.add_argument("--repo", type=Path, default=Path.cwd(), help="candidate Git checkout")
    args = parser.parse_args()
    try:
        result = check_integrity(args.repo, args.base)
    except (ValueError, OSError) as exc:
        print(f"ERROR: cannot verify starter/repository: {exc}", file=sys.stderr)
        return 2
    if result.clean:
        print(f"PASS: protected organizer files unchanged from {result.baseline_commit}")
        return 0
    print(f"WARNING: protected files differ from starter {result.baseline_commit}", file=sys.stderr)
    for path in result.changed_paths:
        print(f"  changed: {path!r}", file=sys.stderr)
    for path in result.added_paths:
        print(f"  added:   {path!r}", file=sys.stderr)
    print("Do not fix supplied tests/harnesses to make the task easier.", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
