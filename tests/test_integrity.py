"""CPU-only integrity-check regressions; each test owns a temporary Git repository."""

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from tools.check_integrity import PROTECTED_PATHS, check_integrity

ROOT = Path(__file__).resolve().parents[1]


class IntegrityTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(self.temp.name)
        self.git("init", "-q")
        self.git("config", "user.email", "integrity-test@example.invalid")
        self.git("config", "user.name", "Integrity Test")
        for namespace in PROTECTED_PATHS:
            path = self.repo / namespace
            if namespace.endswith("/"):
                path = path / "reference.txt"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("reference\n")
        (self.repo / ".gitignore").write_text("*.ignored\n__pycache__/\n")
        self.git("add", ".")
        self.git("commit", "-qm", "starter")
        self.git("tag", "takehome-start")

    def git(self, *args):
        return subprocess.check_output(["git", "-C", str(self.repo), *args], stderr=subprocess.PIPE)

    def write(self, path, text="changed\n"):
        target = self.repo / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text)

    def cli(self, base="takehome-start"):
        return subprocess.run(
            [
                sys.executable,
                "-B",
                "-m",
                "tools.check_integrity",
                "--repo",
                str(self.repo),
                "--base",
                base,
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

    def test_clean_and_cli_pass(self):
        self.assertTrue(check_integrity(self.repo).clean)
        result = self.cli()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("PASS", result.stdout)

    def test_every_protected_namespace_is_checked(self):
        for namespace in PROTECTED_PATHS:
            with self.subTest(namespace=namespace):
                path = namespace + "reference.txt" if namespace.endswith("/") else namespace
                original = (self.repo / path).read_text()
                self.write(path)
                self.assertIn(path, check_integrity(self.repo).changed_paths)
                self.write(path, original)

    def test_unstaged_change_and_cli_warning(self):
        self.write("tests/reference.txt")
        result = self.cli()
        self.assertEqual(result.returncode, 1)
        self.assertIn("WARNING", result.stderr)
        self.assertIn("tests/reference.txt", result.stderr)

    def test_staged_change_hidden_by_restored_worktree(self):
        self.write("benchmarks/reference.txt")
        self.git("add", "benchmarks/reference.txt")
        self.write("benchmarks/reference.txt", "reference\n")
        self.assertIn("benchmarks/reference.txt", check_integrity(self.repo).changed_paths)

    def test_committed_change(self):
        self.write("agent-harness/reference.txt")
        self.git("add", "agent-harness/reference.txt")
        self.git("commit", "-qm", "changed supplied harness")
        self.assertIn("agent-harness/reference.txt", check_integrity(self.repo).changed_paths)

    def test_deletion(self):
        (self.repo / "baseline/reference.txt").unlink()
        self.assertIn("baseline/reference.txt", check_integrity(self.repo).changed_paths)

    def test_rename_outside_protected_root(self):
        self.git("mv", "tests/reference.txt", "candidate.txt")
        self.assertIn("tests/reference.txt", check_integrity(self.repo).changed_paths)

    def test_added_protected_file(self):
        self.write("tests/new_fixture.json")
        self.assertIn("tests/new_fixture.json", check_integrity(self.repo).added_paths)

    def test_ignored_addition_is_not_hidden(self):
        self.write("tests/hidden.ignored")
        self.assertIn("tests/hidden.ignored", check_integrity(self.repo).added_paths)

    def test_only_generated_python_cache_is_exempt(self):
        self.write("tools/__pycache__/check_integrity.cpython-311.pyc")
        self.assertTrue(check_integrity(self.repo).clean)
        self.write("tools/__pycache__/injected.py")
        self.assertIn("tools/__pycache__/injected.py", check_integrity(self.repo).added_paths)

    def test_candidate_benchmark_tests_and_harness_are_editable(self):
        self.write("tasks/benchmark-design/suite/tests/test_candidate.py")
        self.write("tasks/harness-design/harness/run.py")
        self.write("tasks/harness-design/harness/program.md")
        self.assertTrue(check_integrity(self.repo).clean)
        self.git("add", "tasks")
        self.git("commit", "-qm", "candidate solution")
        self.assertTrue(check_integrity(self.repo).clean)

    def test_full_starter_hash_and_subdirectory(self):
        baseline = self.git("rev-parse", "takehome-start").decode().strip()
        result = check_integrity(self.repo / "tests", baseline)
        self.assertTrue(result.clean)
        self.assertEqual(result.baseline_commit, baseline)

    def test_missing_starter_fails_closed(self):
        result = self.cli("missing-starter")
        self.assertEqual(result.returncode, 2)
        self.assertIn("cannot verify", result.stderr)

    def test_option_like_baseline_is_rejected(self):
        with self.assertRaises(ValueError):
            check_integrity(self.repo, "--help")

    def test_non_repository_fails_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            result = subprocess.run(
                [sys.executable, "-B", "-m", "tools.check_integrity", "--repo", directory],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
                env={**os.environ, "GIT_CEILING_DIRECTORIES": directory},
            )
            self.assertEqual(result.returncode, 2)


if __name__ == "__main__":
    unittest.main()
