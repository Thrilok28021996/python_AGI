# Test-Driven Development (TDD) Guide

## Overview

The multi-agent system now includes **automated testing** and **test-driven development (TDD)** workflows. When enabled, the system automatically:

1. ✅ Runs tests after each development iteration
2. 🔍 Detects test failures
3. 📝 Provides structured feedback to developers
4. 🔧 Triggers automatic fix iterations
5. ♻️ Re-runs tests to verify fixes
6. 📊 Tracks test history throughout the project

This creates a **true TDD workflow** where:
- QA Testers write tests
- Developers write code
- **Tests automatically validate the code**
- **Developers automatically fix bugs based on test failures**
- The cycle continues until all tests pass

---

## Table of Contents

1. [How It Works](#how-it-works)
2. [Supported Test Frameworks](#supported-test-frameworks)
3. [Usage Examples](#usage-examples)
4. [Test Execution Flow](#test-execution-flow)
5. [Developer Feedback Loop](#developer-feedback-loop)
6. [CLI Options](#cli-options)
7. [Configuration](#configuration)
8. [Best Practices](#best-practices)
9. [Troubleshooting](#troubleshooting)

---

## How It Works

### Architecture

```
Iteration Loop:
├── 1. Agents create/update code
├── 2. ✅ Auto-run tests (if enabled)
├── 3. 🔍 Parse test results
├── 4. ❌ If tests fail:
│   ├── Generate structured feedback
│   ├── Send to developer agents
│   ├── Developers fix bugs
│   └── Re-run tests
└── 5. Continue to next iteration
```

### Key Components

1. **TestExecutor** (`test_executor.py`)
   - Detects test frameworks automatically
   - Runs tests and parses results
   - Formats feedback for developers
   - Tracks test history

2. **File-Aware Agent** (`file_aware_agent.py`)
   - Integrated testing into workflow
   - Triggers test execution after iterations
   - Provides test feedback to developers
   - Manages test-fix cycles

3. **Build Tool** (`build_project.py`)
   - CLI flags for testing control
   - Display test results in summary
   - Custom test command support

---

## Supported Test Frameworks

### Automatic Detection

The system automatically detects and runs the appropriate test framework:

| Language | Frameworks | Detection Method |
|----------|-----------|------------------|
| **Python** | pytest, unittest | `pytest.ini`, `setup.py`, `test_*.py` files |
| **JavaScript/TypeScript** | Jest, Mocha, npm test | `package.json` with test scripts |
| **Go** | go test | `*_test.go` files |
| **Rust** | cargo test | `Cargo.toml` |
| **Java** | JUnit (Maven/Gradle) | `pom.xml`, `build.gradle` |

### Manual Override

You can specify a custom test command:

```bash
python build_project.py "Create API" --test-command "pytest -v --cov"
```

---

## Usage Examples

### Example 1: Basic TDD Workflow (Python with pytest)

```bash
# Create a project with testing enabled (default)
python build_project.py "Create a calculator library with add, subtract, multiply, divide functions. Include comprehensive tests."

# The system will:
# 1. QA Tester creates test files (test_calculator.py)
# 2. Backend Developer creates implementation (calculator.py)
# 3. Auto-run tests after iteration 1
# 4. If tests fail, developer receives feedback:
#    "Test test_divide failed: ZeroDivisionError"
# 5. Developer fixes the bug
# 6. Re-run tests to verify fix
# 7. Continue until all tests pass
```

### Example 2: JavaScript TDD with Jest

```bash
python build_project.py "Build a React component library with tests" \
    --agents frontend_developer qa_tester \
    --test-command "npm test"
```

### Example 3: Disable Testing

```bash
# Skip testing (useful for prototyping)
python build_project.py "Quick prototype" --no-testing
```

### Example 4: TDD with Specific Iterations

```bash
# Run exactly 5 iterations with testing
python build_project.py "Create REST API" \
    --iterations 5 \
    --no-auto-stop \
    --test-command "pytest -v"
```

---

## Test Execution Flow

### Timeline of Events

```
Iteration 0:
  QA Tester → Creates test files (test_calculator.py)
  Backend Developer → Creates implementation (calculator.py)
  ✅ SKIP TESTS (no implementation yet)

Iteration 1:
  Backend Developer → Implements functions
  QA Tester → Reviews and adds more tests
  🧪 RUN TESTS: pytest -v
  📊 RESULT: 3 passed, 2 failed

  ❌ Test Failures Detected:
    - test_divide: ZeroDivisionError when divisor is 0
    - test_multiply: Returns incorrect result for negative numbers

  🔧 FIX ITERATION (automatic):
    Backend Developer receives feedback:
      "⚠️ TEST RESULTS: TESTS FAILING - CODE NEEDS FIXES

       Failed Tests:
       1. Test: test_divide
          Error: ZeroDivisionError: division by zero

       2. Test: test_multiply
          Error: AssertionError: expected -6, got 6

       REQUIRED ACTIONS:
       - Fix the bugs causing test failures
       - Provide fixed code"

    Backend Developer → Fixes divide (add zero check)
    Backend Developer → Fixes multiply (handle negative numbers)

  ♻️ RE-RUN TESTS: pytest -v
  📊 RESULT: 5 passed, 0 failed
  ✅ ALL TESTS PASSING!

Iteration 2:
  (All tests passing, continue refinement...)
```

---

## Developer Feedback Loop

### What Developers Receive

When tests fail, developers get **structured, actionable feedback**:

```
⚠️ TEST RESULTS: TESTS FAILING - CODE NEEDS FIXES

❌ 2/5 tests failed
✅ 3/5 tests passed
Framework: pytest -v

CRITICAL: You MUST fix the failing tests before proceeding.

Failed Tests:

1. Test: test_calculator.py::test_divide_by_zero
   Error:
   def test_divide_by_zero():
       calculator = Calculator()
   >   result = calculator.divide(10, 0)
   E   ZeroDivisionError: division by zero

2. Test: test_calculator.py::test_multiply_negative
   Error:
   AssertionError: assert 6 == -6
    +  where 6 = <bound method Calculator.multiply of ...>(2, -3)

REQUIRED ACTIONS:
1. Read the test file to understand what's expected
2. Review the code that's being tested
3. Fix the bugs causing test failures
4. Provide the fixed code in ```update: filename format
5. Explain what was wrong and how you fixed it

DO NOT PROCEED until tests pass.
```

### Developer Response

```python
# Developer analyzes the feedback and fixes:

# Fix 1: Add zero division check
```update: calculator.py
class Calculator:
    def divide(self, a, b):
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b
```

# Fix 2: Fix multiply logic for negative numbers
```update: calculator.py
    def multiply(self, a, b):
        # Was: return abs(a * b)  # BUG: always positive
        return a * b  # FIXED: preserve sign
```

Analysis:
1. divide() was missing zero check - added ValueError
2. multiply() was using abs() incorrectly - removed it
```

---

## CLI Options

### Testing Flags

```bash
# Enable testing (default)
python build_project.py "Create API"

# Disable testing
python build_project.py "Create API" --no-testing

# Custom test command
python build_project.py "Create API" --test-command "pytest -v --cov"

# Custom test command with arguments
python build_project.py "Create API" --test-command "npm run test:unit"
```

### Complete Example

```bash
python build_project.py \
    "Create a REST API for blog posts with full CRUD operations" \
    --name blog_api \
    --agents backend_developer qa_tester devops \
    --iterations 5 \
    --test-command "pytest -v --cov=src" \
    --min-iterations 2 \
    --output ./my_projects
```

---

## Configuration

### Enable/Disable Testing in Code

```python
from file_aware_agent import create_project_workflow

result = create_project_workflow(
    project_name="my_project",
    task="Create a calculator",
    agents=[
        {"type": "backend_developer", "name": "Alice"},
        {"type": "qa_tester", "name": "Bob"}
    ],
    enable_testing=True,  # Enable testing
    test_command="pytest -v"  # Optional: custom command
)

# Check test results
if result['final_test_results']:
    if result['final_test_results']['success']:
        print("✅ All tests passing!")
    else:
        print(f"❌ {result['final_test_results']['failed']} tests failed")

# View test history
for i, test_run in enumerate(result['test_history'], 1):
    print(f"Run {i}: {test_run['passed']}/{test_run['total_tests']} passed")
```

### Custom Test Executor

```python
from test_executor import TestExecutor

# Create executor
executor = TestExecutor("./my_project")

# Auto-detect and run tests
results = executor.run_tests()

# Or use custom command
results = executor.run_tests("pytest -v --cov")

# Format feedback
feedback = executor.format_feedback_for_developer(results)
print(feedback)

# Get history
history = executor.get_test_history_summary()
print(history)
```

---

## Best Practices

### 1. Include QA Tester in Team

✅ **DO:**
```bash
python build_project.py "Create API" \
    --agents backend_developer qa_tester
```

❌ **DON'T:**
```bash
python build_project.py "Create API" \
    --agents backend_developer  # No QA = no tests!
```

**Why:** QA Tester creates comprehensive test files. Without them, there are no tests to run.

### 2. Write Testable Requirements

✅ **DO:**
```bash
"Create a calculator library with add, subtract, multiply, divide functions.
 Include tests for:
 - Basic operations
 - Edge cases (zero, negative numbers)
 - Error handling (division by zero)"
```

❌ **DON'T:**
```bash
"Make a calculator"  # Too vague
```

### 3. Let Tests Run Before Completion

✅ **DO:**
```bash
python build_project.py "Create API" --min-iterations 2
```

**Why:** First iteration creates tests & code, second iteration runs tests. Auto-stop after min iterations ensures tests have run.

### 4. Use Auto-Stop with Testing

✅ **DO:**
```bash
# Default: auto-stop when agents agree AND tests pass
python build_project.py "Create API"
```

**Why:** System will continue iterating if tests are failing, even if agents think it's done.

### 5. Review Test Output

```bash
python build_project.py "Create API" > build.log 2>&1
```

**Why:** Full test output is logged. Review to understand what failed.

---

## Troubleshooting

### Issue: "No test framework detected"

**Solution 1:** Ensure QA Tester is in the team:
```bash
--agents backend_developer qa_tester
```

**Solution 2:** Specify test command manually:
```bash
--test-command "pytest"
```

**Solution 3:** Check test files exist:
```bash
ls generated_projects/my_project/test_*.py
```

---

### Issue: Tests timeout after 5 minutes

**Cause:** Tests are taking too long to run.

**Solution 1:** Reduce test scope in requirements:
```bash
"Create API with basic tests (not integration tests)"
```

**Solution 2:** Disable slow tests:
```bash
--test-command "pytest -v -m 'not slow'"
```

---

### Issue: Tests fail but developers don't fix them

**Cause:** Developer agent is not receiving feedback properly.

**Debug:**
```python
# Check if developer agents exist
result = create_project_workflow(...)
developer_agents = [a for a in file_agents if "developer" in a.role.lower()]
print(f"Found {len(developer_agents)} developers")
```

**Solution:** Ensure at least one developer agent is in the team.

---

### Issue: Tests pass locally but fail in agent system

**Cause:** Different environment or dependencies.

**Solution:** Install dependencies first:
```bash
# Have DevOps agent create requirements.txt
--agents backend_developer qa_tester devops
```

Then the DevOps agent will:
1. Create requirements.txt
2. Create setup.py
3. Include installation instructions

---

### Issue: Want to run tests manually after build

**Solution:**
```bash
# Build project
python build_project.py "Create API" --output ./projects

# Run tests manually
cd projects/my_api
pytest -v
```

Or disable auto-testing and run tests yourself:
```bash
python build_project.py "Create API" --no-testing
```

---

## Advanced: Test-Driven Development Workflow

### Real TDD (Tests First)

Update your task description to enforce TDD:

```bash
python build_project.py "
Create a calculator library using Test-Driven Development:

WORKFLOW:
1. QA Tester: Write failing tests FIRST
2. Backend Developer: Write minimal code to pass tests
3. Backend Developer: Refactor for quality
4. Repeat

REQUIREMENTS:
- Tests should be created BEFORE implementation
- All tests must pass
- Code coverage > 80%
" --iterations 5
```

The system will naturally follow TDD because:
1. Iteration 0: QA creates tests (which fail - no code yet)
2. Iteration 1: Developer writes code to pass tests
3. Iteration 2+: Refactor and improve

---

## Test History Tracking

### View Test History in Results

```python
result = create_project_workflow(...)

print("\n📊 Test History:")
for i, test_run in enumerate(result['test_history'], 1):
    status = "✅" if test_run['success'] else "❌"
    print(f"{status} Run {i}: {test_run['passed']}/{test_run['total_tests']} passed")
    if test_run['failures']:
        for failure in test_run['failures'][:2]:  # Show first 2
            print(f"   - {failure['test']}: {failure['error'][:50]}...")
```

**Example Output:**
```
📊 Test History:
❌ Run 1: 3/5 passed
   - test_divide: ZeroDivisionError...
   - test_multiply: AssertionError...
✅ Run 2: 5/5 passed
✅ Run 3: 5/5 passed
```

---

## Summary

### What Changed

1. ✅ **New Module:** `test_executor.py` - Automatic test execution
2. ✅ **Updated:** `file_aware_agent.py` - Integrated testing into workflow
3. ✅ **Updated:** `build_project.py` - CLI flags for testing
4. ✅ **New Feature:** Auto-detect test frameworks (pytest, jest, etc.)
5. ✅ **New Feature:** Structured feedback to developers on test failures
6. ✅ **New Feature:** Automatic fix iterations when tests fail
7. ✅ **New Feature:** Test history tracking

### Testing is Now Default

- **Before:** No automated testing, manual verification only
- **After:** Tests run automatically, bugs fixed automatically

### Benefits

1. 🎯 **Higher Code Quality:** Bugs caught immediately
2. ⚡ **Faster Development:** No manual testing needed
3. 🔄 **True TDD:** Write tests, write code, verify, repeat
4. 📊 **Visibility:** See test results in real-time
5. 🤖 **Automation:** Developers fix bugs based on test failures automatically

---

## Examples in Action

### Example Project: REST API with TDD

```bash
python build_project.py \
    "Create a REST API for a todo list with FastAPI.

     Requirements:
     - CRUD operations (Create, Read, Update, Delete)
     - Input validation
     - Error handling
     - Comprehensive tests using pytest

     QA Tester: Write tests for all endpoints and edge cases
     Backend Developer: Implement the API to pass all tests" \
    --agents backend_developer qa_tester \
    --iterations 4 \
    --test-command "pytest -v"
```

**What Happens:**
1. **Iteration 0:** QA creates `test_api.py` with 20 tests, Developer creates `main.py`
2. **Iteration 1:** Auto-run tests → 12 passed, 8 failed (validation errors)
3. **Fix Iteration:** Developer adds validation → Re-run → 18 passed, 2 failed
4. **Iteration 2:** Developer fixes last 2 bugs → All tests passing ✅
5. **Auto-stop:** Project complete!

---

## Comparison: Before vs After

### Before (Without Automated Testing)

```
Iteration 1: Create code
Iteration 2: Review code manually
Iteration 3: Fix obvious issues
Done (but untested!)
```

**Problems:**
- No verification
- Bugs in production
- Manual testing required

### After (With Automated Testing)

```
Iteration 1: Create code + tests
Run tests → 3 failed
Auto-fix → Re-run tests → All pass ✅

Iteration 2: Add features
Run tests → All pass ✅
Done with confidence!
```

**Benefits:**
- Automatic verification
- Bugs caught immediately
- No manual work needed

---

## Next Steps

1. **Try It:** Run `python build_project.py "Create a calculator with tests"`
2. **Review:** Check the test output in console
3. **Inspect:** Look at `generated_projects/*/test_*.py` files
4. **Customize:** Use `--test-command` for your framework
5. **Iterate:** Use `--iterations 5` for more thorough testing

Happy Test-Driven Development! 🧪✅
