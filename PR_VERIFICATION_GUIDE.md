# Pandas PR Verification & Quality Assurance Guide

**Version**: 1.0
**Created**: 2026-03-09
**Updated**: 2026-03-09

---

## 📋 Table of Contents

1. [Quick Start](#quick-start)
2. [Common Issues & Solutions](#common-issues--solutions)
3. [Test File Best Practices](#test-file-best-practices)
4. [Verification Checklist](#verification-checklist)
5. [Automated Tools](#automated-tools)
6. [Troubleshooting](#troubleshooting)

---

## Quick Start

### Run All Verifications

```bash
# 1. Quick syntax check
python verify_pr.py --verbose

# 2. Full verification with pre-commit
pre-commit run --all-files

# 3. Run affected tests
pytest pandas/tests/arrays/test_array.py -v

# 4. Type checking (optional, slower)
mypy pandas/tests/arrays/test_array.py --strict
```

### For Your Current PR (GH#57702)

```bash
# Verify the specific files changed
python verify_pr.py --verbose --json > pr_report.json

# Run tests
pytest pandas/tests/arrays/test_array.py::test_array_str_dtype_preserves_na -xvs
pytest pandas/tests/arrays/test_array.py::test_array_str_dtype_consistent_with_series -xvs
pytest pandas/tests/series/methods/test_astype.py::TestAstype::test_astype_int_na_string -xvs
```

---

## Common Issues & Solutions

### 1. ❌ Indentation Errors

**Problem**: Test assertion not indented inside function body

```python
# WRONG ❌
def test_my_function(self):
    result = function_call()
expected = result_value
tm.assert_series_equal(result, expected)  # NOT indented!

# CORRECT ✅
def test_my_function(self):
    result = function_call()
    expected = result_value
    tm.assert_series_equal(result, expected)  # Properly indented
```

**Detection**: Run `python verify_pr.py` → Check "Indentation" errors

**Fix**: Add 4 spaces or 1 tab per indentation level

---

### 2. ❌ Test Naming

**Problem**: Functions don't start with `test_` or classes don't start with `Test`

```python
# WRONG ❌
def verify_behavior():  # Doesn't start with test_
    assert something

class Helper:  # Doesn't start with Test
    def test_helper(self):
        pass

# CORRECT ✅
def test_behavior():  # Starts with test_
    assert something

class TestHelper:  # Starts with Test
    def test_something(self):
        pass
```

**Detection**: Run `python verify_pr.py` → Check "Test naming" errors

**Fix**: Rename functions/classes to follow convention

---

### 3. ❌ Regex Pattern Issues

**Problem**: `pytest.raises(match=...)` pattern doesn't match actual error

```python
# WRONG ❌
msg = "dtype '' not understood"  # Empty quotes don't match anything!
with pytest.raises(TypeError, match=msg):
    ser.astype(datetime)
# Actual error: "dtype '<class 'datetime.datetime'>' not understood"
# Pattern won't match! ❌

# CORRECT ✅
msg = "dtype .* not understood"  # .* matches any characters
with pytest.raises(TypeError, match=msg):
    ser.astype(datetime)
# Now pattern matches! ✅
```

**Detection**: Run `python verify_pr.py` → Check "Pattern regex" errors

**Fix**: Use `.*` to match variable parts, test pattern with:
```python
import re
pattern = "dtype .* not understood"
message = "dtype '<class 'datetime.datetime'>' not understood"
assert re.search(pattern, message), "Pattern doesn't match!"
```

---

### 4. ❌ Duplicate Tests

**Problem**: Same test logic in multiple files

```python
# File 1: pandas/tests/arrays/test_array.py
def test_array_str_dtype_consistent_with_series():
    result_array = pd.array([1, None], dtype=str)
    result_series = pd.Series([1, None], dtype=str).array
    tm.assert_extension_array_equal(result_array, result_series)

# File 2: pandas/tests/arrays/numpy_/test_numpy.py
def test_array_str_dtype_with_none():  # SAME LOGIC!
    arr_result = pd.array([1, None], dtype=str)
    series_result = pd.Series([1, None], dtype=str).array
    tm.assert_extension_array_equal(arr_result, series_result)
```

**Detection**: Run `python verify_pr.py` → Check "Duplicate tests" warnings

**Fix**: Consolidate into one file, preferring broader test directory

---

### 5. ❌ No Assertions

**Problem**: Test function has no assertions

```python
# WRONG ❌
def test_conversion():
    ser = Series([1, 2, 3])
    result = ser.astype(float)
    # No assertion! What are we testing?

# CORRECT ✅
def test_conversion():
    ser = Series([1, 2, 3])
    result = ser.astype(float)
    assert result.dtype == float  # Assert expected behavior
    tm.assert_series_equal(result, Series([1.0, 2.0, 3.0], dtype=float))
```

**Detection**: Run `python verify_pr.py` → Check "Test logic" warnings

**Fix**: Add assertions to verify expected behavior

---

### 6. ❌ Wrong Import of Assertions

**Problem**: Using plain assert instead of pandas testing utilities

```python
# SUBOPTIMAL ❌
import pandas._testing as tm
ser1 = Series([1, 2])
ser2 = Series([1, 2])
assert ser1.equals(ser2)  # Basic comparison

# BETTER ✅
import pandas._testing as tm
ser1 = Series([1, 2])
ser2 = Series([1, 2])
tm.assert_series_equal(ser1, ser2)  # Detailed comparison with better error messages
```

**Detection**: Linting tools and code review

**Fix**: Use `pandas._testing` utilities for better error messages

---

## Test File Best Practices

### Structure

```python
"""
Module docstring explaining what tests are in this file.
"""

import numpy as np
import pytest

import pandas as pd
import pandas._testing as tm
from pandas import Series, DataFrame


class TestSeriesAstype:
    """Tests for Series.astype() method."""

    def test_astype_to_string(self):
        """Test astype conversion to string dtype."""
        # Setup
        ser = Series([1, 2, 3])

        # Execute
        result = ser.astype(str)

        # Assert
        expected = Series(["1", "2", "3"], dtype=object)
        tm.assert_series_equal(result, expected)

    @pytest.mark.parametrize("na_value", [None, np.nan, pd.NA])
    def test_astype_with_na_values(self, na_value):
        """Test astype handling of NA values."""
        ser = Series([1, na_value])
        result = ser.astype(str)

        # Verify NA is preserved
        assert pd.isna(result[1])
```

### Decorator Patterns

```python
# Skip test if dependency missing
@td.skip_if_no("pyarrow")
def test_pyarrow_operation(self):
    result = pd.Series([1, 2], dtype="int64[pyarrow]")
    assert result.dtype.name == "int64[pyarrow]"

# Skip test if dependency present
@td.skip_if_installed("pyarrow")
def test_fallback_behavior(self):
    # Test behavior when pyarrow not available
    pass

# Parametrize test
@pytest.mark.parametrize("dtype", ["int64", "float64", "object"])
def test_multiple_dtypes(self, dtype):
    ser = Series([1, 2, 3], dtype=dtype)
    assert ser.dtype == dtype

# Expected failure
@pytest.mark.xfail(reason="Known limitation")
def test_future_feature(self):
    # Test for feature not yet implemented
    pass

# Mark as slow
@pytest.mark.slow
def test_large_dataset(self):
    # Test with large dataset
    pass
```

### Assertion Patterns

```python
import pandas._testing as tm

# Series comparison
tm.assert_series_equal(result, expected)

# DataFrame comparison
tm.assert_frame_equal(result, expected)

# Index comparison
tm.assert_index_equal(result.index, expected.index)

# NumPy array comparison
tm.assert_numpy_array_equal(result, expected)

# Category comparison
tm.assert_categorical_equal(result, expected)

# Extension array comparison
tm.assert_extension_array_equal(result, expected)

# Warning context
with tm.assert_produces_warning(FutureWarning):
    result = function_with_warning()

# No warning
with tm.assert_produces_warning(None):
    result = function_without_warning()
```

---

## Verification Checklist

Use this before pushing your PR:

### Syntax & Format
- [ ] `python verify_pr.py --verbose` passes all checks
- [ ] `pre-commit run --all-files` passes all hooks
- [ ] `python -m py_compile` passes for all changed files
- [ ] No trailing whitespace
- [ ] Proper indentation (4 spaces or 1 tab)

### Test Naming & Structure
- [ ] All test functions start with `test_`
- [ ] All test classes start with `Test`
- [ ] Test methods use clear, descriptive names
- [ ] Test docstrings explain what is being tested
- [ ] Test has at least one assertion

### Test Logic
- [ ] Assertions use `pandas._testing` utilities (tm.*)
- [ ] Regex patterns in `pytest.raises(match=...)` are valid and match actual errors
- [ ] No duplicate tests across files
- [ ] Test is not skipped unnecessarily (`@pytest.mark.skip`)
- [ ] Setup, execution, assertion are clearly separated

### Issue-Specific
- [ ] References correct GitHub issue (#XXXXX)
- [ ] Commit message explains the fix
- [ ] No merge conflicts
- [ ] All affected test files checked

### Documentation
- [ ] Docstrings added/updated if needed
- [ ] whatsnew entry added (if user-facing change)
- [ ] Type hints added (if applicable)

### Pre-submission
- [ ] Tests pass locally: `pytest pandas/tests/arrays/test_array.py -v`
- [ ] No new warnings from mypy
- [ ] All hooks pass: `pre-commit run --all-files`
- [ ] JSON report generated: `python verify_pr.py --json > report.json`

---

## Automated Tools

### 1. **verify_pr.py** - Main Verification Script

```bash
# Check current directory
python verify_pr.py

# Verbose output
python verify_pr.py --verbose

# JSON output for CI
python verify_pr.py --json > pr_report.json

# Custom repo path
python verify_pr.py --repo /path/to/pandas --verbose
```

**Checks performed**:
- ✅ Indentation correctness
- ✅ Test naming conventions
- ✅ Regex pattern validation
- ✅ Duplicate test detection
- ✅ Test logic verification
- ✅ Import statement analysis
- ✅ Docstring coverage
- ✅ Type hint suggestions

### 2. **pre-commit hooks** - Automatic checks before commit

```bash
# Install hooks
pre-commit install

# Run all hooks
pre-commit run --all-files

# Run specific hook
pre-commit run pandas-test-verify --all-files
```

### 3. **pytest** - Test execution

```bash
# Run specific test
pytest pandas/tests/arrays/test_array.py::test_array_str_dtype_preserves_na -xvs

# Run test file
pytest pandas/tests/arrays/test_array.py -v

# Run with coverage
pytest pandas/tests/arrays/test_array.py --cov=pandas --cov-report=html
```

### 4. **mypy** - Type checking

```bash
# Check specific file
mypy pandas/tests/arrays/test_array.py --strict

# Check all tests
mypy pandas/tests --strict
```

---

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'pandas._libs.pandas_parser'"

**Cause**: Pandas C extensions not compiled

**Solution**:
```bash
cd /Users/logio/pandas
python -m pip install -e . --no-build-isolation -q
```

### Issue: Pre-commit hook failing

**Solution**:
```bash
# Check hook output
pre-commit run --all-files --verbose

# Update dependencies
pre-commit autoupdate

# Reinstall hooks
pre-commit install --install-hooks
```

### Issue: Test passes locally but fails in CI

**Cause**: Environment difference or missing test dependency

**Solution**:
1. Check test for `@td.skip_if_no(...)` decorators
2. Run test in isolated environment: `pytest pandas/tests/arrays/test_array.py --tb=short`
3. Check for hardcoded paths or OS-specific logic

### Issue: Regex pattern validation fails

**Solution**: Test pattern manually:
```python
import re
pattern = "dtype .* not understood"
message = "dtype '<class 'datetime.datetime'>' not understood"
match = re.search(pattern, message)
print(f"Match: {match is not None}")  # Should be True
```

---

## For Your PR #64424

### Summary of Fixes Applied

| Issue | File | Fix |
|-------|------|-----|
| Missing indentation | `test_astype.py:686` | Added 8 spaces indentation |
| Duplicate test | `test_numpy.py:414-425` | Removed (exists in `test_array.py`) |
| Invalid regex | `test_astype.py:700` | Changed `"dtype '' not understood"` → `"dtype .* not understood"` |

### Verification Commands

```bash
# Verify all fixes
python verify_pr.py --verbose

# Test the specific functions
pytest pandas/tests/arrays/test_array.py::test_array_str_dtype_preserves_na -xvs
pytest pandas/tests/arrays/test_array.py::test_array_str_dtype_consistent_with_series -xvs
pytest pandas/tests/series/methods/test_astype.py::TestAstype::test_astype_int_na_string -xvs
pytest pandas/tests/series/methods/test_astype.py::TestAstype::test_dt_to_pydatetime_returns_object_dtype -xvs
pytest pandas/tests/series/methods/test_astype.py::TestAstype::test_astype_datetime_raises_typeerror -xvs

# Generate final report
python verify_pr.py --json > final_report.json
```

---

## Resources

- **Pandas Contributing**: https://pandas.pydata.org/docs/development/contributing.html
- **Testing Best Practices**: https://pandas.pydata.org/docs/development/testing.html
- **Pytest Documentation**: https://docs.pytest.org/
- **Pre-commit Framework**: https://pre-commit.com/

---

**Last Updated**: 2026-03-09
**Maintainer**: logio (Claude AI Assistant)
