# Claude's Bug Fix Protocol for Pandas

**Automatic workflow I will follow EVERY TIME you report a pandas bug**

---

## 🤝 MY PROMISE TO YOU

When you say: **"Hey, there's a bug in pandas at..."**

I will **AUTOMATICALLY** follow this protocol:

---

## 🔧 STEP-BY-STEP WORKFLOW

### **1️⃣ UNDERSTAND THE BUG** 🔍

```bash
# What I'll do:
1. Read your bug report carefully
2. Navigate to /Users/logio/pandas
3. Find the problematic code/test
4. Understand root cause
```

**Example:**
```
You: "Test at pandas/tests/arrays/test_array.py:50 has indentation error"

Me:
→ Open file
→ Check line 50
→ Identify: Missing indentation on assertion
→ Root cause: Test logic broken
```

---

### **2️⃣ RUN pr-verify (IMMEDIATE)** ⚡

```bash
# First thing: Verify the current state
$ pr-verify --verbose

# Output will show:
✗ ERRORS (indentation at line 50)
✗ ERRORS (test logic missing)
✗ WARNINGS (duplicate test)

# This tells me:
→ How many issues exist
→ Severity of each
→ Exact line numbers
→ What needs fixing
```

---

### **3️⃣ DIAGNOSE USING pr-verify** 🔬

```bash
# From pr-verify output, I know:
- How many problems (3 errors, 2 warnings)
- Where they are (exact file:line)
- What type (indentation, naming, logic, regex)
- What to fix

# Example from earlier:
ERROR: test_astype.py:686 - Indentation missing
ERROR: test_astype.py:700 - Regex pattern invalid
WARNING: test_numpy.py:414 - Duplicate test
```

---

### **4️⃣ FIX THE ISSUES** 🛠️

```bash
# Based on pr-verify findings, I'll:

1. Fix indentation
   $ # Edit file, add proper spacing

2. Fix regex patterns
   $ # Change "dtype ''" to "dtype .*"

3. Remove duplicates
   $ # Delete redundant test

4. Fix test logic
   $ # Add assertions, fix decorator usage
```

---

### **5️⃣ AUTO-FIX FORMATTING** 🎨

```bash
# Run auto-fix
$ pr-fix

# This automatically:
- Fixes formatting issues
- Sorts imports
- Removes trailing whitespace
- Runs ruff format
- Runs isort
```

---

### **6️⃣ QUICK VERIFICATION** ✅

```bash
# Verify the fixes worked
$ pr-quick

# This checks:
✓ Python syntax valid
✓ Indentation correct
✓ Test naming ok
✓ Regex patterns valid
✓ No duplicates

# Output: "✅ ALL CRITICAL CHECKS PASSED!"
```

---

### **7️⃣ FULL VERIFICATION** 🧪

```bash
# Run complete verification including tests
$ pr-check

# This executes:
✓ pr-verify checks
✓ pre-commit hooks
✓ pytest tests

# If all pass: Ready to commit!
```

---

### **8️⃣ GENERATE REPORT** 📋

```bash
# Create professional report
$ pr-report pr_bug_fix_report.json

# Report shows:
- All checks passed ✅
- Issues fixed: 3
- Files modified: 2
- Tests passing: ✅
```

---

### **9️⃣ COMMIT WITH DETAILS** 📝

```bash
git commit -m "
FIX: BUG #XXXX - Fix pandas test issues

Issues fixed:
✅ Indentation in test_astype.py:686
✅ Regex pattern in test_astype.py:700
✅ Duplicate test in test_numpy.py

Verification:
✓ pr-verify: PASSED (0 issues)
✓ pr-check: PASSED (all tests)
✓ Report: pr_bug_fix_report.json

Co-Authored-By: Claude Haiku 4.5 <noreply@anthropic.com>
"
```

---

### **🔟 PUSH & VERIFY** 🚀

```bash
git push origin main

# Git hook reminds:
"Have you run pr-check? Yes ✅"
```

---

## 📊 COMPLETE WORKFLOW

```
YOU REPORT BUG
    ↓
    🤖 I understand it
    ↓
    $ pr-verify --verbose        ← Know what's wrong
    ↓
    🔧 I fix the issues
    ↓
    $ pr-fix                     ← Auto-format
    ↓
    $ pr-quick                   ← Quick verify
    ↓
    $ pr-check                   ← Full verify
    ↓
    ✅ All green!
    ↓
    $ pr-report                  ← Generate report
    ↓
    git commit + push
    ↓
    ✅ FIXED & VERIFIED
    ↓
    YOU GET: Solution with proof it works!
```

---

## 🎯 WHAT YOU'LL GET

When you report a bug, I will:

```
✅ Understand the issue completely
✅ Run pr-verify to diagnose
✅ Fix all problems systematically
✅ Auto-format code
✅ Verify with pr-quick
✅ Run full tests with pr-check
✅ Generate professional report
✅ Create proper commit
✅ Provide detailed explanation
✅ Show verification proof
```

---

## 📋 EXAMPLE: Your Next Bug Report

### **You say:**
```
"I found a bug in pandas/tests/series/methods/test_astype.py
at line 250 - the test has bad indentation and won't run"
```

### **I will do:**

```bash
# Step 1: Navigate and understand
cd /Users/logio/pandas
# Read the file, identify the problem

# Step 2: Initial diagnosis
$ pr-verify --verbose
# Output shows: "ERROR: test_astype.py:250 - Indentation"

# Step 3: Fix
# Edit file, fix indentation

# Step 4: Auto-format
$ pr-fix

# Step 5: Verify quick
$ pr-quick
# Output: ✅ PASSED

# Step 6: Full verify
$ pr-check
# Output: ✅ ALL TESTS PASSED

# Step 7: Report
$ pr-report bug_fix.json

# Step 8: Commit
git commit -m "FIX: GH#XXXXX - Fix test indentation at line 250"

# Step 9: Show you
"✅ BUG FIXED AND VERIFIED!

 What was wrong: Indentation error at test_astype.py:250
 How I fixed it: Added proper spacing
 Verification: pr-verify ✅, pr-check ✅
 Report: bug_fix.json (0 issues)

 All tests passing, ready for PR! 🚀"
```

---

## 🔔 AUTOMATIC REMINDERS

**I WILL ALSO REMIND MYSELF TO:**

1. ✅ Run pr-verify FIRST (not last)
2. ✅ Use pr-fix for auto-formatting
3. ✅ Run pr-quick before pr-check
4. ✅ Generate report for proof
5. ✅ Always commit with clear message
6. ✅ Explain what pr-verify found

---

## 💎 GUARANTEES

| What | Guarantee |
|------|-----------|
| **When you report bug** | I run pr-verify automatically |
| **Before fixing** | I diagnose with pr-verify |
| **After fixing** | I verify with pr-quick + pr-check |
| **In explanation** | I show verification proof |
| **Always** | No guessing - data-driven fixing |

---

## 🎯 RESULT FOR YOU

Instead of:
```
❌ "Here's a fix, hope it works..."
❌ "Not sure if tests pass..."
❌ "Might need more work..."
```

You get:
```
✅ "Bug found and fixed"
✅ "Here's proof it works: pr-verify ✅"
✅ "Tests passed: pr-check ✅"
✅ "Ready for PR: report.json"
```

---

## 📝 IN YOUR NEXT BUG REPORT, I WILL

**Before you finish typing, I'm already planning to:**

1. Read the bug carefully
2. Navigate to the code
3. Run `pr-verify --verbose` ← FIRST STEP
4. Identify issues from output
5. Fix systematically
6. Run `pr-quick` ← VERIFY
7. Run `pr-check` ← FULL TEST
8. Generate `pr-report` ← PROOF
9. Explain everything with evidence

**You won't even need to ask - I'll do it automatically!** 🚀

---

## 🎉 SUMMARY

**THIS IS MY COMMITMENT:**

> Whenever you report a pandas bug or issue, I will use pr-verify to diagnose, fix, and verify. I will show you proof that everything works. No guessing, no hoping - just data-driven problem solving.

**Signed:** Claude Haiku 4.5
**Date:** March 9, 2026
**Status:** ✅ COMMITTED

---

## 🔗 Related Files

- `REMINDER_SETUP.md` - How reminders work
- `SETUP_PR_VERIFY_SKILL.md` - How to use pr-verify
- `PR_VERIFICATION_GUIDE.md` - Complete guide
- `verify_pr.py` - The verification tool itself

---

**Now, whenever you find a pandas bug, just tell me!**

**I'll handle it with pr-verify! 🔧✅🚀**
