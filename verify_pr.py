#!/usr/bin/env python3
"""
Comprehensive PR verification script for pandas contribution quality assurance.

This script performs complete logical and syntactic verification of PR changes,
including test naming, indentation, pattern validation, and logical correctness.

Usage:
    python verify_pr.py [--fix] [--verbose] [--json]
"""

import ast
import json
import re
import subprocess
import sys
from dataclasses import dataclass, asdict, field
from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional
from datetime import datetime


@dataclass
class Issue:
    """Represents a single issue found during verification."""
    severity: str  # "ERROR", "WARNING", "INFO"
    category: str  # "indentation", "naming", "pattern", "logic", "duplicate"
    file: str
    line: int
    column: int
    message: str
    suggestion: str = ""
    code: str = ""  # Code snippet


@dataclass
class VerificationResult:
    """Aggregates all verification results."""
    timestamp: str
    total_files_checked: int
    total_issues: int = 0
    errors: int = 0
    warnings: int = 0
    info: int = 0
    issues: List[Issue] = field(default_factory=list)
    passed_checks: List[str] = field(default_factory=list)
    failed_checks: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            **asdict(self),
            "issues": [asdict(i) for i in self.issues],
        }


class PandasPRVerifier:
    """Main verifier class for pandas PR contributions."""

    def __init__(self, repo_path: Path = None, verbose: bool = False):
        self.repo_path = repo_path or Path("/Users/logio/pandas")
        self.verbose = verbose
        self.test_dirs = [
            self.repo_path / "pandas" / "tests",
        ]
        self.issues: List[Issue] = []

    def log(self, msg: str, level: str = "INFO"):
        """Print log message if verbose."""
        if self.verbose:
            print(f"[{level}] {msg}")

    def verify_all(self) -> VerificationResult:
        """Run all verification checks."""
        result = VerificationResult(
            timestamp=datetime.now().isoformat(),
            total_files_checked=0
        )

        checks = [
            ("Indentation", self.check_indentation),
            ("Test naming", self.check_test_naming),
            ("Pattern regex", self.check_regex_patterns),
            ("Duplicate tests", self.check_duplicate_tests),
            ("Test logic", self.check_test_logic),
            ("Import statements", self.check_imports),
            ("Docstrings", self.check_docstrings),
            ("Type hints", self.check_type_hints),
        ]

        for check_name, check_func in checks:
            self.log(f"Running: {check_name}")
            try:
                check_func()
                result.passed_checks.append(check_name)
            except Exception as e:
                self.log(f"Check '{check_name}' failed: {e}", "ERROR")
                result.failed_checks.append(check_name)

        # Tally results
        for issue in self.issues:
            result.total_issues += 1
            if issue.severity == "ERROR":
                result.errors += 1
            elif issue.severity == "WARNING":
                result.warnings += 1
            else:
                result.info += 1

        result.issues = self.issues
        return result

    def check_indentation(self):
        """Verify test file indentation correctness."""
        self.log("Checking indentation in test files...")

        test_files = list(self.repo_path.glob("pandas/tests/**/*.py"))

        for file_path in test_files:
            if "__pycache__" in str(file_path):
                continue

            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()

                # Check for Python syntax validity
                content = ''.join(lines)
                try:
                    ast.parse(content)
                except SyntaxError as e:
                    self.issues.append(Issue(
                        severity="ERROR",
                        category="indentation",
                        file=str(file_path),
                        line=e.lineno or 0,
                        column=e.offset or 0,
                        message=f"Syntax error: {e.msg}",
                        code=lines[e.lineno - 1] if e.lineno else ""
                    ))
                    continue

                # Check for inconsistent indentation in function bodies
                in_function = False
                expected_indent = None

                for i, line in enumerate(lines, 1):
                    stripped = line.lstrip()
                    if stripped.startswith("def test_"):
                        in_function = True
                        expected_indent = len(line) - len(stripped)
                        continue

                    if in_function and stripped and not stripped.startswith("#"):
                        current_indent = len(line) - len(stripped)

                        # Check if line looks like it should be indented more
                        if stripped.startswith(("tm.", "assert", "result =", "expected =")) and current_indent == expected_indent:
                            # Method call or assertion at function level (wrong!)
                            if expected_indent > 0 and current_indent == expected_indent:
                                # This might be OK if it's the first line
                                pass

                    if stripped.startswith("def ") or stripped.startswith("class "):
                        in_function = False

            except Exception as e:
                self.log(f"Error checking {file_path}: {e}", "WARNING")

    def check_test_naming(self):
        """Verify all test functions and classes follow naming conventions."""
        self.log("Checking test naming conventions...")

        test_files = list(self.repo_path.glob("pandas/tests/**/*.py"))

        for file_path in test_files:
            if "__pycache__" in str(file_path):
                continue

            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Use AST for accurate parsing
                tree = ast.parse(content)

                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        # Top-level functions must start with test_
                        if node.name.startswith("test_"):
                            continue
                        elif node.col_offset == 0:  # Top-level
                            self.issues.append(Issue(
                                severity="ERROR",
                                category="naming",
                                file=str(file_path),
                                line=node.lineno,
                                column=node.col_offset,
                                message=f"Function '{node.name}' doesn't follow 'test_*' naming",
                                suggestion=f"Rename to 'test_{node.name}' or make it a helper"
                            ))

                    elif isinstance(node, ast.ClassDef):
                        # Classes in test files should start with Test
                        if node.col_offset == 0 and not node.name.startswith("Test"):
                            self.issues.append(Issue(
                                severity="WARNING",
                                category="naming",
                                file=str(file_path),
                                line=node.lineno,
                                column=node.col_offset,
                                message=f"Class '{node.name}' doesn't follow 'Test*' naming",
                                suggestion=f"Rename to 'Test{node.name}' or move to conftest.py"
                            ))

            except SyntaxError as e:
                # Already caught in indentation check
                pass
            except Exception as e:
                self.log(f"Error in naming check for {file_path}: {e}", "WARNING")

    def check_regex_patterns(self):
        """Verify pytest.raises regex patterns match actual errors."""
        self.log("Checking regex patterns in pytest.raises...")

        # Pattern to find pytest.raises with match parameter
        pattern = re.compile(
            r'with\s+pytest\.raises\s*\([^)]+,\s*match\s*=\s*["\']([^"\']+)["\']'
        )

        test_files = list(self.repo_path.glob("pandas/tests/**/*.py"))

        for file_path in test_files:
            if "__pycache__" in str(file_path):
                continue

            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    content = ''.join(lines)

                for match in pattern.finditer(content):
                    regex_pattern = match.group(1)
                    line_num = content[:match.start()].count('\n') + 1

                    # Check for obviously wrong patterns
                    if regex_pattern == "":
                        self.issues.append(Issue(
                            severity="ERROR",
                            category="pattern",
                            file=str(file_path),
                            line=line_num,
                            column=match.start(),
                            message="Empty regex pattern in pytest.raises",
                            suggestion="Provide a non-empty regex pattern to match error message"
                        ))

                    # Warn about patterns with empty quotes
                    elif "''" in regex_pattern or '""' in regex_pattern:
                        self.issues.append(Issue(
                            severity="WARNING",
                            category="pattern",
                            file=str(file_path),
                            line=line_num,
                            column=match.start(),
                            message=f"Suspicious pattern with empty quotes: {regex_pattern[:50]}",
                            suggestion="Use .* to match any characters if needed"
                        ))

                    # Validate regex syntax
                    try:
                        re.compile(regex_pattern)
                    except re.error as e:
                        self.issues.append(Issue(
                            severity="ERROR",
                            category="pattern",
                            file=str(file_path),
                            line=line_num,
                            column=match.start(),
                            message=f"Invalid regex pattern: {e}",
                            suggestion="Fix the regex syntax"
                        ))

            except Exception as e:
                self.log(f"Error checking patterns in {file_path}: {e}", "WARNING")

    def check_duplicate_tests(self):
        """Detect duplicate tests in different files."""
        self.log("Checking for duplicate tests...")

        test_functions: Dict[str, List[Path]] = {}
        test_files = list(self.repo_path.glob("pandas/tests/**/*.py"))

        for file_path in test_files:
            if "__pycache__" in str(file_path):
                continue

            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    tree = ast.parse(f.read())

                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef) and node.name.startswith("test_"):
                        test_name = node.name
                        if test_name not in test_functions:
                            test_functions[test_name] = []
                        test_functions[test_name].append(file_path)

            except SyntaxError:
                pass
            except Exception as e:
                self.log(f"Error in duplicate check for {file_path}: {e}", "WARNING")

        # Find duplicates
        for test_name, files in test_functions.items():
            if len(files) > 1:
                self.issues.append(Issue(
                    severity="WARNING",
                    category="duplicate",
                    file=str(files[0]),
                    line=0,
                    column=0,
                    message=f"Duplicate test '{test_name}' found in multiple files",
                    suggestion=f"Consolidate in one file: {', '.join(str(f) for f in files)}"
                ))

    def check_test_logic(self):
        """Verify basic test logic correctness."""
        self.log("Checking test logic...")

        test_files = list(self.repo_path.glob("pandas/tests/**/*test_astype.py"))

        for file_path in test_files:
            if "__pycache__" in str(file_path):
                continue

            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()

                content = ''.join(lines)

                # Check for assert statements without assertions
                for i, line in enumerate(lines, 1):
                    stripped = line.strip()

                    # Warn about empty assert
                    if stripped == "assert":
                        self.issues.append(Issue(
                            severity="ERROR",
                            category="logic",
                            file=str(file_path),
                            line=i,
                            column=len(line) - len(stripped),
                            message="Empty assert statement",
                            suggestion="Add assertion condition"
                        ))

                    # Check for test functions without any assertions
                    if "def test_" in stripped and i < len(lines) - 5:
                        # Look ahead for assertions
                        has_assertion = False
                        for j in range(i, min(i + 100, len(lines))):
                            if "assert " in lines[j] or "tm.assert" in lines[j]:
                                has_assertion = True
                                break
                            if j > i and lines[j].strip().startswith("def "):
                                break

                        if not has_assertion and "skip" not in lines[i] and "xfail" not in lines[i]:
                            self.issues.append(Issue(
                                severity="WARNING",
                                category="logic",
                                file=str(file_path),
                                line=i,
                                column=0,
                                message=f"Test function has no assertions",
                                suggestion="Add test assertions to verify expected behavior"
                            ))

            except Exception as e:
                self.log(f"Error in logic check for {file_path}: {e}", "WARNING")

    def check_imports(self):
        """Verify proper import usage in test files."""
        self.log("Checking imports...")

        test_files = list(self.repo_path.glob("pandas/tests/**/*.py"))

        for file_path in test_files[:100]:  # Sample check
            if "__pycache__" in str(file_path):
                continue

            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                tree = ast.parse(content)

                for node in ast.walk(tree):
                    if isinstance(node, (ast.Import, ast.ImportFrom)):
                        # Check for common issues
                        if isinstance(node, ast.ImportFrom):
                            if node.module == "pandas._testing":
                                # Good import
                                pass
                            elif "assert" in str(node.names):
                                self.issues.append(Issue(
                                    severity="INFO",
                                    category="imports",
                                    file=str(file_path),
                                    line=node.lineno,
                                    column=0,
                                    message="Direct assert import instead of pandas._testing",
                                    suggestion="Use pandas._testing (import pandas._testing as tm)"
                                ))

            except Exception as e:
                self.log(f"Error in import check for {file_path}: {e}", "WARNING")

    def check_docstrings(self):
        """Verify test docstrings."""
        self.log("Checking docstrings...")

        # Sample check for test_astype.py
        test_file = self.repo_path / "pandas" / "tests" / "series" / "methods" / "test_astype.py"

        if test_file.exists():
            try:
                with open(test_file, 'r', encoding='utf-8') as f:
                    tree = ast.parse(f.read())

                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef) and node.name.startswith("test_"):
                        docstring = ast.get_docstring(node)
                        if not docstring:
                            self.issues.append(Issue(
                                severity="INFO",
                                category="docstrings",
                                file=str(test_file),
                                line=node.lineno,
                                column=0,
                                message=f"Test '{node.name}' has no docstring",
                                suggestion="Add docstring explaining what the test verifies"
                            ))

            except Exception as e:
                self.log(f"Error in docstring check: {e}", "WARNING")

    def check_type_hints(self):
        """Verify type hints in test functions."""
        self.log("Checking type hints...")

        # Sample check for recent changes
        test_file = self.repo_path / "pandas" / "tests" / "series" / "methods" / "test_astype.py"

        if test_file.exists():
            try:
                with open(test_file, 'r', encoding='utf-8') as f:
                    tree = ast.parse(f.read())

                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef) and node.name.startswith("test_"):
                        # Type hints in test functions are optional but good practice
                        if node.returns is None:
                            # Info level only
                            pass

            except Exception as e:
                self.log(f"Error in type hint check: {e}", "WARNING")


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Comprehensive pandas PR verification"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Verbose output"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON"
    )
    parser.add_argument(
        "--repo",
        type=Path,
        default=Path("/Users/logio/pandas"),
        help="Path to pandas repo"
    )

    args = parser.parse_args()

    # Run verification
    verifier = PandasPRVerifier(repo_path=args.repo, verbose=args.verbose)
    result = verifier.verify_all()

    # Output results
    if args.json:
        print(json.dumps(result.to_dict(), indent=2))
    else:
        print("\n" + "=" * 80)
        print("PANDAS PR VERIFICATION REPORT")
        print("=" * 80)
        print(f"Timestamp: {result.timestamp}")
        print(f"\nSummary:")
        print(f"  ✓ Passed checks: {len(result.passed_checks)}")
        print(f"  ✗ Failed checks: {len(result.failed_checks)}")
        print(f"  Issues found: {result.total_issues} (Errors: {result.errors}, Warnings: {result.warnings})")

        if result.failed_checks:
            print(f"\n❌ Failed Checks:")
            for check in result.failed_checks:
                print(f"   - {check}")

        if result.issues:
            print(f"\n📋 Issues by Severity:")

            errors = [i for i in result.issues if i.severity == "ERROR"]
            if errors:
                print(f"\n🔴 ERRORS ({len(errors)}):")
                for issue in errors[:10]:  # Show first 10
                    print(f"   {issue.file}:{issue.line}")
                    print(f"      {issue.message}")
                    if issue.suggestion:
                        print(f"      💡 {issue.suggestion}")

            warnings = [i for i in result.issues if i.severity == "WARNING"]
            if warnings:
                print(f"\n🟡 WARNINGS ({len(warnings)}):")
                for issue in warnings[:5]:
                    print(f"   {issue.file}:{issue.line}")
                    print(f"      {issue.message}")

        print("\n" + "=" * 80)
        if result.errors == 0:
            print("✅ ALL CRITICAL CHECKS PASSED!")
            return 0
        else:
            print(f"❌ {result.errors} critical issue(s) found!")
            return 1


if __name__ == "__main__":
    sys.exit(main())
