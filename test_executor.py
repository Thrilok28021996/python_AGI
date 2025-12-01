"""
Test Execution System
Automatically runs tests and provides feedback to developers for code fixes
Implements Test-Driven Development (TDD) workflow in multi-agent systems
"""

import os
import subprocess
import json
import re
from typing import Dict, List, Optional, Tuple
from pathlib import Path
import colorama

colorama.init(autoreset=True)


class TestExecutor:
    """
    Executes tests and provides structured feedback for developers
    Supports multiple test frameworks: pytest, unittest, jest, etc.
    """

    def __init__(self, project_path: str):
        """
        Initialize test executor

        Args:
            project_path: Path to the project being tested
        """
        self.project_path = Path(project_path)
        self.test_history = []  # Track all test runs
        self.supported_frameworks = {
            "python": ["pytest", "unittest", "python -m pytest"],
            "javascript": ["npm test", "jest", "mocha"],
            "typescript": ["npm test", "jest"],
            "java": ["mvn test", "gradle test"],
            "go": ["go test ./..."],
            "rust": ["cargo test"]
        }

    def detect_test_framework(self) -> Optional[str]:
        """
        Auto-detect which test framework to use based on project files

        Returns:
            Command to run tests, or None if no framework detected
        """
        # Check for Python test frameworks
        if (self.project_path / "pytest.ini").exists() or \
           (self.project_path / "setup.py").exists() or \
           list(self.project_path.glob("test_*.py")) or \
           list(self.project_path.glob("*_test.py")):
            # Check if pytest is available
            try:
                subprocess.run(["pytest", "--version"], capture_output=True, timeout=5)
                return "pytest -v"
            except:
                return "python -m unittest discover -v"

        # Check for JavaScript/TypeScript
        if (self.project_path / "package.json").exists():
            try:
                with open(self.project_path / "package.json", 'r') as f:
                    package_data = json.load(f)
                    if "scripts" in package_data and "test" in package_data["scripts"]:
                        return "npm test"
            except:
                pass
            return "jest"

        # Check for Go
        if list(self.project_path.glob("*_test.go")):
            return "go test ./... -v"

        # Check for Rust
        if (self.project_path / "Cargo.toml").exists():
            return "cargo test"

        # Check for Java
        if (self.project_path / "pom.xml").exists():
            return "mvn test"
        if (self.project_path / "build.gradle").exists():
            return "gradle test"

        return None

    def run_tests(self, custom_command: Optional[str] = None) -> Dict:
        """
        Execute tests and capture results

        Args:
            custom_command: Optional custom test command (otherwise auto-detect)

        Returns:
            Dict with test results, pass/fail status, and error details
        """
        test_command = custom_command or self.detect_test_framework()

        if not test_command:
            return {
                "success": False,
                "error": "No test framework detected. Please create tests or specify test command.",
                "framework": None,
                "total_tests": 0,
                "passed": 0,
                "failed": 0,
                "errors": [],
                "failures": []
            }

        print(colorama.Fore.CYAN + f"\n🧪 Running tests: {test_command}" + colorama.Style.RESET_ALL)
        print(colorama.Fore.CYAN + f"   Working directory: {self.project_path}\n" + colorama.Style.RESET_ALL)

        try:
            # Run test command
            result = subprocess.run(
                test_command.split(),
                cwd=self.project_path,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )

            # Parse test results
            test_results = self._parse_test_output(
                result.stdout,
                result.stderr,
                result.returncode,
                test_command
            )

            # Record in history
            self.test_history.append(test_results)

            # Print summary
            self._print_test_summary(test_results)

            return test_results

        except subprocess.TimeoutExpired:
            error_result = {
                "success": False,
                "error": "Tests timed out after 5 minutes",
                "framework": test_command,
                "total_tests": 0,
                "passed": 0,
                "failed": 0,
                "errors": ["Test execution exceeded 5 minute timeout"],
                "failures": []
            }
            self.test_history.append(error_result)
            return error_result

        except Exception as e:
            error_result = {
                "success": False,
                "error": f"Failed to run tests: {str(e)}",
                "framework": test_command,
                "total_tests": 0,
                "passed": 0,
                "failed": 0,
                "errors": [str(e)],
                "failures": []
            }
            self.test_history.append(error_result)
            return error_result

    def _parse_test_output(
        self,
        stdout: str,
        stderr: str,
        returncode: int,
        framework: str
    ) -> Dict:
        """
        Parse test output to extract structured results

        Args:
            stdout: Standard output from test run
            stderr: Standard error from test run
            returncode: Exit code from test command
            framework: Test framework/command used

        Returns:
            Structured test results
        """
        full_output = stdout + "\n" + stderr
        results = {
            "success": returncode == 0,
            "framework": framework,
            "total_tests": 0,
            "passed": 0,
            "failed": 0,
            "errors": [],
            "failures": [],
            "stdout": stdout,
            "stderr": stderr,
            "returncode": returncode
        }

        # Parse pytest output
        if "pytest" in framework.lower():
            # Look for summary line like "5 passed, 2 failed in 1.23s"
            match = re.search(r'(\d+) passed', full_output)
            if match:
                results["passed"] = int(match.group(1))

            match = re.search(r'(\d+) failed', full_output)
            if match:
                results["failed"] = int(match.group(1))

            results["total_tests"] = results["passed"] + results["failed"]

            # Extract failure details
            results["failures"] = self._extract_pytest_failures(full_output)

        # Parse unittest output
        elif "unittest" in framework.lower():
            # Look for lines like "Ran 10 tests"
            match = re.search(r'Ran (\d+) test', full_output)
            if match:
                results["total_tests"] = int(match.group(1))

            # Check if OK or FAILED
            if "OK" in full_output:
                results["passed"] = results["total_tests"]
                results["failed"] = 0
            else:
                # Parse failures
                match = re.search(r'FAILED \(.*?failures=(\d+)', full_output)
                if match:
                    results["failed"] = int(match.group(1))
                    results["passed"] = results["total_tests"] - results["failed"]

            results["failures"] = self._extract_unittest_failures(full_output)

        # Parse Jest output
        elif "jest" in framework.lower() or "npm test" in framework.lower():
            match = re.search(r'Tests:\s+(\d+) failed.*?(\d+) passed.*?(\d+) total', full_output)
            if match:
                results["failed"] = int(match.group(1))
                results["passed"] = int(match.group(2))
                results["total_tests"] = int(match.group(3))

            results["failures"] = self._extract_jest_failures(full_output)

        # Parse Go test output
        elif "go test" in framework.lower():
            # Count PASS and FAIL lines
            results["passed"] = len(re.findall(r'--- PASS:', full_output))
            results["failed"] = len(re.findall(r'--- FAIL:', full_output))
            results["total_tests"] = results["passed"] + results["failed"]

            results["failures"] = self._extract_go_failures(full_output)

        # If we couldn't parse specific counts, at least note if tests failed
        if results["total_tests"] == 0 and returncode != 0:
            results["errors"].append("Tests failed but couldn't parse detailed results")
            results["failed"] = 1  # Mark as having failures

        return results

    def _extract_pytest_failures(self, output: str) -> List[Dict]:
        """Extract failure details from pytest output"""
        failures = []

        # Look for FAILED test lines
        failed_tests = re.findall(r'FAILED (.*?) - (.*?)(?:\n|$)', output)
        for test_name, error_msg in failed_tests:
            failures.append({
                "test": test_name.strip(),
                "error": error_msg.strip()
            })

        # Also look for assertion errors with more detail
        sections = re.split(r'_{70,}', output)  # Split on long underlines
        for section in sections:
            if 'AssertionError' in section or 'Error' in section:
                # Try to extract test name and error
                test_match = re.search(r'(test_\w+)', section)
                if test_match:
                    test_name = test_match.group(1)
                    # Get a few lines of error context
                    lines = section.split('\n')
                    error_lines = [l for l in lines if l.strip() and not l.startswith('_')][:5]
                    if error_lines and not any(f["test"] == test_name for f in failures):
                        failures.append({
                            "test": test_name,
                            "error": "\n".join(error_lines)
                        })

        return failures

    def _extract_unittest_failures(self, output: str) -> List[Dict]:
        """Extract failure details from unittest output"""
        failures = []

        # Look for FAIL: test_name lines
        sections = re.split(r'={70,}', output)
        for section in sections:
            if section.strip().startswith('FAIL:'):
                lines = section.split('\n')
                test_name = lines[0].replace('FAIL:', '').strip() if lines else "unknown"
                error_msg = '\n'.join(lines[1:5])  # Get a few lines of context
                failures.append({
                    "test": test_name,
                    "error": error_msg.strip()
                })

        return failures

    def _extract_jest_failures(self, output: str) -> List[Dict]:
        """Extract failure details from Jest output"""
        failures = []

        # Look for ● test name pattern
        test_blocks = re.split(r'●', output)
        for block in test_blocks[1:]:  # Skip first empty block
            lines = block.strip().split('\n')
            if lines:
                test_name = lines[0].strip()
                error_msg = '\n'.join(lines[1:5])  # Get a few lines
                failures.append({
                    "test": test_name,
                    "error": error_msg.strip()
                })

        return failures

    def _extract_go_failures(self, output: str) -> List[Dict]:
        """Extract failure details from Go test output"""
        failures = []

        # Look for --- FAIL: test_name
        fail_blocks = re.findall(r'--- FAIL: (\w+).*?\n(.*?)(?=---|\Z)', output, re.DOTALL)
        for test_name, error_msg in fail_blocks:
            failures.append({
                "test": test_name.strip(),
                "error": error_msg.strip()[:500]  # Limit error length
            })

        return failures

    def _print_test_summary(self, results: Dict):
        """Print formatted test summary"""
        if results["success"]:
            print(colorama.Fore.GREEN + "\n✅ ALL TESTS PASSED!" + colorama.Style.RESET_ALL)
            print(colorama.Fore.GREEN + f"   {results['passed']}/{results['total_tests']} tests passed\n" + colorama.Style.RESET_ALL)
        else:
            print(colorama.Fore.RED + "\n❌ TESTS FAILED!" + colorama.Style.RESET_ALL)
            print(colorama.Fore.RED + f"   {results['failed']}/{results['total_tests']} tests failed" + colorama.Style.RESET_ALL)
            print(colorama.Fore.GREEN + f"   {results['passed']}/{results['total_tests']} tests passed\n" + colorama.Style.RESET_ALL)

            # Print failure details
            if results["failures"]:
                print(colorama.Fore.YELLOW + "Failed tests:" + colorama.Style.RESET_ALL)
                for i, failure in enumerate(results["failures"][:5], 1):  # Show first 5
                    print(colorama.Fore.YELLOW + f"\n{i}. {failure['test']}" + colorama.Style.RESET_ALL)
                    print(colorama.Fore.RED + f"   {failure['error'][:200]}" + colorama.Style.RESET_ALL)
                if len(results["failures"]) > 5:
                    print(colorama.Fore.YELLOW + f"\n   ... and {len(results['failures']) - 5} more failures" + colorama.Style.RESET_ALL)

    def format_feedback_for_developer(self, test_results: Dict) -> str:
        """
        Format test results as actionable feedback for developer agents

        Args:
            test_results: Results from run_tests()

        Returns:
            Formatted feedback string for developer agents
        """
        if test_results["success"]:
            return f"""
🎉 TEST RESULTS: ALL TESTS PASSING

✅ {test_results['passed']}/{test_results['total_tests']} tests passed
Framework: {test_results['framework']}

Great job! The code is working correctly.
No changes needed based on test results.
"""

        # Tests failed - provide detailed feedback
        feedback = f"""
⚠️ TEST RESULTS: TESTS FAILING - CODE NEEDS FIXES

❌ {test_results['failed']}/{test_results['total_tests']} tests failed
✅ {test_results['passed']}/{test_results['total_tests']} tests passed
Framework: {test_results['framework']}

CRITICAL: You MUST fix the failing tests before proceeding.

Failed Tests:
"""

        # Add each failure with details
        failures = test_results.get("failures", [])
        if failures:
            for i, failure in enumerate(failures, 1):
                feedback += f"""
{i}. Test: {failure.get('test', 'unknown')}
   Error:
   {failure.get('error', 'No error details available')}
"""
        else:
            # If no failures list, check for errors
            errors = test_results.get("errors", [])
            if errors:
                for i, error in enumerate(errors, 1):
                    feedback += f"""
{i}. Error: {error}
"""
            else:
                # General error message
                feedback += f"""
General test failure. Error: {test_results.get('error', 'Unknown error')}
"""

        feedback += """

REQUIRED ACTIONS:
1. Read the test file to understand what's expected
2. Review the code that's being tested
3. Fix the bugs causing test failures
4. Provide the fixed code in ```update: filename format
5. Explain what was wrong and how you fixed it

DO NOT PROCEED until tests pass. Focus on fixing these specific failures.
"""

        # Add stderr if it has useful information
        if test_results.get("stderr") and len(test_results["stderr"]) > 10:
            feedback += f"""

Additional Error Output:
{test_results['stderr'][:1000]}
"""

        return feedback

    def get_test_history_summary(self) -> str:
        """Get a summary of all test runs"""
        if not self.test_history:
            return "No tests have been run yet."

        summary = "Test History:\n"
        for i, test_run in enumerate(self.test_history, 1):
            status = "✅ PASSED" if test_run["success"] else "❌ FAILED"
            summary += f"{i}. {status} - {test_run['passed']}/{test_run['total_tests']} passed\n"

        return summary


# Example usage
if __name__ == "__main__":
    # Example: Test a Python project
    executor = TestExecutor("./my_project")

    # Run tests
    results = executor.run_tests()

    # Get feedback for developers
    feedback = executor.format_feedback_for_developer(results)
    print(feedback)
