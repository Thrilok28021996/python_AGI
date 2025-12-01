#!/usr/bin/env python3
"""
Example: Test the 5-agent system with automated testing
Demonstrates how tests automatically run and provide feedback to developers
"""

from file_aware_agent import create_project_workflow
import colorama

colorama.init(autoreset=True)

def main():
    print(colorama.Fore.CYAN + """
╔═══════════════════════════════════════════════════════════════════════╗
║         TEST: 5-AGENT SYSTEM WITH AUTOMATED TESTING                   ║
║                                                                       ║
║  This example demonstrates the complete TDD workflow:                ║
║  1. QA Tester creates tests                                          ║
║  2. Backend Developer writes code                                    ║
║  3. Tests run automatically                                          ║
║  4. If tests fail, developer gets feedback and fixes bugs           ║
║  5. Tests re-run to verify fixes                                    ║
╚═══════════════════════════════════════════════════════════════════════╝
    """ + colorama.Style.RESET_ALL)

    result = create_project_workflow(
        project_name="calculator_tdd",
        task="""
Create a Python calculator library using Test-Driven Development.

Requirements:
- Calculator class with methods: add, subtract, multiply, divide
- Handle edge cases (division by zero, negative numbers, floats)
- Input validation
- Comprehensive tests using pytest

QA TESTER:
- Create test_calculator.py with comprehensive tests
- Include tests for:
  * Basic operations (add, subtract, multiply, divide)
  * Edge cases (zero, negative, floats)
  * Error handling (division by zero)
  * At least 10 test cases total

BACKEND DEVELOPER:
- Create calculator.py with Calculator class
- Implement all methods to pass tests
- Add proper error handling
- Include docstrings

The tests should run automatically and guide development!
        """,
        agents=[
            {"type": "backend_developer", "name": "Alice"},
            {"type": "qa_tester", "name": "Bob"},
        ],
        output_dir="./generated_projects",
        max_iterations=4,  # Enough for: create, test, fix, verify
        stop_on_complete=True,
        min_iterations=2,  # Allow at least 2 iterations for testing
        enable_testing=True,  # Enable automated testing
        test_command=None  # Auto-detect (will use pytest)
    )

    # Print detailed results
    print(colorama.Fore.GREEN + "\n\n" + "="*80)
    print("FINAL RESULTS")
    print("="*80 + colorama.Style.RESET_ALL)

    print(f"\n📁 Project Location: {result['project_path']}")
    print(f"📊 Files Created: {len(result['files'])}")

    print(colorama.Fore.CYAN + "\n📂 Project Structure:" + colorama.Style.RESET_ALL)
    for file in result['files']:
        print(f"   {file}")

    # Show test history
    if result['test_history']:
        print(colorama.Fore.CYAN + "\n🧪 Test History:" + colorama.Style.RESET_ALL)
        for i, test_run in enumerate(result['test_history'], 1):
            status = "✅ PASS" if test_run['success'] else "❌ FAIL"
            print(f"   Run {i}: {status} - {test_run['passed']}/{test_run['total_tests']} tests passed")

            if not test_run['success'] and test_run.get('failures'):
                print(colorama.Fore.YELLOW + "      Failed tests:")
                for failure in test_run['failures'][:3]:  # Show first 3
                    print(f"      - {failure['test']}")

    # Final test results
    if result['final_test_results']:
        final_test = result['final_test_results']
        print(colorama.Fore.CYAN + "\n✅ Final Test Results:" + colorama.Style.RESET_ALL)
        if final_test['success']:
            print(colorama.Fore.GREEN + f"   ALL TESTS PASSING! ({final_test['passed']}/{final_test['total_tests']})" + colorama.Style.RESET_ALL)
        else:
            print(colorama.Fore.RED + f"   TESTS FAILING: {final_test['failed']}/{final_test['total_tests']} failed" + colorama.Style.RESET_ALL)

    print(colorama.Fore.MAGENTA + "\n💡 Next Steps:" + colorama.Style.RESET_ALL)
    print(f"   1. Review the code: cd {result['project_path']}")
    print(f"   2. Run tests manually: pytest -v")
    print(f"   3. Use the calculator: python -c 'from calculator import Calculator; c = Calculator(); print(c.add(5, 3))'")

    print(colorama.Fore.GREEN + "\n🎉 Test-Driven Development Complete!" + colorama.Style.RESET_ALL)


if __name__ == "__main__":
    main()
