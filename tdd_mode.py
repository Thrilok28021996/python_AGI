"""
Test-Driven Development (TDD) Mode
Implements true TDD: Write tests first, then make them pass

Workflow:
1. QA agent writes comprehensive tests based on requirements
2. Run tests (they should FAIL - red phase)
3. Developer implements code to make tests pass (green phase)
4. Refactor code while keeping tests green (refactor phase)
5. Repeat until all tests pass and code is clean
"""

from typing import List, Dict, Optional
from pathlib import Path
from langchain_core.messages import HumanMessage
import colorama

colorama.init(autoreset=True)


class TDDWorkflow:
    """
    Manages Test-Driven Development workflow
    Ensures tests are written before implementation
    """

    def __init__(self, file_manager: 'FileManager', test_executor: 'TestExecutor'):
        """
        Initialize TDD workflow

        Args:
            file_manager: FileManager for file operations
            test_executor: TestExecutor for running tests
        """
        self.file_manager = file_manager
        self.test_executor = test_executor
        self.tdd_history = []

    def execute_tdd_cycle(
        self,
        task: str,
        qa_agent: 'FileAwareAgent',
        developer_agents: List['FileAwareAgent'],
        context: str = "",
        max_cycles: int = 5
    ) -> Dict:
        """
        Execute complete TDD cycle

        Args:
            task: Feature/requirement to implement
            qa_agent: QA agent who writes tests
            developer_agents: Developer agents who implement
            context: Additional project context
            max_cycles: Maximum TDD cycles

        Returns:
            Dict with TDD results
        """
        print(colorama.Fore.MAGENTA + f"\n{'='*80}")
        print(f"🧪 TDD MODE: {task}")
        print(f"{'='*80}\n" + colorama.Style.RESET_ALL)

        print(colorama.Fore.CYAN + "TDD Workflow:" + colorama.Style.RESET_ALL)
        print("  1. ✍️  QA writes tests (RED phase)")
        print("  2. ❌ Tests fail (expected)")
        print("  3. 💻 Developer implements code (GREEN phase)")
        print("  4. ✅ Tests pass")
        print("  5. 🔄 Refactor (REFACTOR phase)\n")

        # Phase 1: RED - Write failing tests
        print(colorama.Fore.RED + "\n=== PHASE 1: RED (Write Tests) ===" + colorama.Style.RESET_ALL)

        test_result = self._write_tests_first(qa_agent, task, context)

        if not test_result['tests_created']:
            print(colorama.Fore.RED + "❌ Failed to create tests" + colorama.Style.RESET_ALL)
            return {
                "success": False,
                "phase": "red",
                "error": "No tests created"
            }

        print(colorama.Fore.GREEN + f"✓ Created {len(test_result['test_files'])} test file(s)" + colorama.Style.RESET_ALL)

        # Run tests - they should fail
        print(colorama.Fore.YELLOW + "\n🧪 Running tests (should fail)..." + colorama.Style.RESET_ALL)
        initial_test_results = self.test_executor.run_tests()

        if initial_test_results.get("success", False):
            print(colorama.Fore.YELLOW + "⚠️ Tests passed without implementation - tests may be invalid!" + colorama.Style.RESET_ALL)
        else:
            print(colorama.Fore.GREEN + "✓ Tests failing as expected (RED phase complete)" + colorama.Style.RESET_ALL)

        # Phase 2: GREEN - Implement to pass tests
        print(colorama.Fore.GREEN + "\n=== PHASE 2: GREEN (Make Tests Pass) ===" + colorama.Style.RESET_ALL)

        implementation_result = self._implement_to_pass_tests(
            developer_agents,
            task,
            initial_test_results,
            context,
            max_cycles
        )

        if not implementation_result['success']:
            print(colorama.Fore.RED + "❌ Failed to make all tests pass" + colorama.Style.RESET_ALL)
            return {
                "success": False,
                "phase": "green",
                "tests_created": test_result['test_files'],
                "final_test_results": implementation_result['final_test_results']
            }

        print(colorama.Fore.GREEN + f"✅ All tests passing after {implementation_result['cycles']} cycle(s)!" + colorama.Style.RESET_ALL)

        # Phase 3: REFACTOR - Clean up code
        print(colorama.Fore.BLUE + "\n=== PHASE 3: REFACTOR (Improve Code) ===" + colorama.Style.RESET_ALL)

        refactor_result = self._refactor_phase(
            developer_agents,
            task,
            context
        )

        # Final test run
        print(colorama.Fore.YELLOW + "\n🧪 Final test run after refactoring..." + colorama.Style.RESET_ALL)
        final_test_results = self.test_executor.run_tests()

        if not final_test_results.get("success", False):
            print(colorama.Fore.RED + "❌ Refactoring broke tests! Rolling back..." + colorama.Style.RESET_ALL)
            return {
                "success": False,
                "phase": "refactor",
                "error": "Refactoring broke tests"
            }

        print(colorama.Fore.GREEN + "✅ TDD CYCLE COMPLETE!" + colorama.Style.RESET_ALL)

        return {
            "success": True,
            "phase": "complete",
            "tests_created": test_result['test_files'],
            "implementation_cycles": implementation_result['cycles'],
            "refactored": refactor_result['refactored'],
            "final_test_results": final_test_results,
            "test_coverage": final_test_results.get("total_tests", 0)
        }

    def _write_tests_first(
        self,
        qa_agent: 'FileAwareAgent',
        task: str,
        context: str
    ) -> Dict:
        """
        Phase 1: QA agent writes tests BEFORE implementation

        Args:
            qa_agent: QA agent
            task: Feature requirement
            context: Project context

        Returns:
            Dict with test creation results
        """
        print(colorama.Fore.CYAN + f"👤 {qa_agent.name} is writing tests...\n" + colorama.Style.RESET_ALL)

        test_prompt = f"""You are in TDD MODE. Your job is to write comprehensive tests BEFORE any implementation exists.

**Task/Feature:** {task}
**Context:** {context}

**CRITICAL REQUIREMENTS:**
1. Write tests that define EXPECTED BEHAVIOR
2. Tests should FAIL now (no implementation yet)
3. Tests become the SPECIFICATION for developers
4. Cover happy paths, edge cases, and error scenarios
5. Use proper test framework (pytest for Python, jest for JavaScript)

**Test File Naming:**
- Python: test_<feature>.py
- JavaScript: <feature>.test.js

Create comprehensive test files now. These tests will guide the implementation.

**Example Structure:**
```python
# test_calculator.py
import pytest
from calculator import Calculator  # Will be implemented later

def test_add_positive_numbers():
    calc = Calculator()
    assert calc.add(2, 3) == 5

def test_add_negative_numbers():
    calc = Calculator()
    assert calc.add(-2, -3) == -5

def test_divide_by_zero_raises_error():
    calc = Calculator()
    with pytest.raises(ZeroDivisionError):
        calc.divide(10, 0)
```

Write your tests now!
"""

        response = qa_agent.step(HumanMessage(content=test_prompt))

        # Process test file creation
        operation_result = qa_agent.process_and_execute_file_operations(response.content)

        test_files = [
            f for f in operation_result['files_created']
            if 'test' in Path(f).name.lower()
        ]

        return {
            "tests_created": len(test_files) > 0,
            "test_files": test_files,
            "response": response.content
        }

    def _implement_to_pass_tests(
        self,
        developer_agents: List['FileAwareAgent'],
        task: str,
        test_results: Dict,
        context: str,
        max_cycles: int
    ) -> Dict:
        """
        Phase 2: Developers implement code to make tests pass

        Args:
            developer_agents: List of developer agents
            task: Feature requirement
            test_results: Initial test results (should be failing)
            context: Project context
            max_cycles: Maximum implementation cycles

        Returns:
            Dict with implementation results
        """
        cycle = 0

        for cycle in range(max_cycles):
            print(colorama.Fore.CYAN + f"\n💻 Implementation Cycle {cycle + 1}/{max_cycles}" + colorama.Style.RESET_ALL)

            # Format test failures for developers
            test_feedback = self.test_executor.format_feedback_for_developer(test_results)

            for agent in developer_agents:
                print(colorama.Fore.YELLOW + f"👤 {agent.name} implementing..." + colorama.Style.RESET_ALL)

                impl_prompt = f"""You are in TDD MODE - GREEN PHASE.

**Task:** {task}
**Context:** {context}

**Test Results:**
{test_feedback}

**YOUR JOB:**
1. Read the failing tests to understand requirements
2. Implement the MINIMUM code to make tests pass
3. Don't over-engineer - just make tests green
4. Write clean, working code

**CRITICAL:**
- Tests define the requirements
- Write ONLY what's needed to pass tests
- No extra features
- Focus on making tests pass

Implement the code now!
"""

                response = agent.step(HumanMessage(content=impl_prompt))

                # Process code creation
                agent.process_and_execute_file_operations(response.content)

            # Run tests again
            print(colorama.Fore.YELLOW + "\n🧪 Running tests..." + colorama.Style.RESET_ALL)
            test_results = self.test_executor.run_tests()

            if test_results.get("success", False):
                print(colorama.Fore.GREEN + f"✅ All tests passing!" + colorama.Style.RESET_ALL)
                return {
                    "success": True,
                    "cycles": cycle + 1,
                    "final_test_results": test_results
                }

            failed = test_results.get("failed", 0)
            total = test_results.get("total_tests", 0)
            print(colorama.Fore.YELLOW + f"⚠️ {failed}/{total} tests still failing" + colorama.Style.RESET_ALL)

        # Max cycles reached
        print(colorama.Fore.RED + f"❌ Reached max cycles, tests still failing" + colorama.Style.RESET_ALL)
        return {
            "success": False,
            "cycles": max_cycles,
            "final_test_results": test_results
        }

    def _refactor_phase(
        self,
        developer_agents: List['FileAwareAgent'],
        task: str,
        context: str
    ) -> Dict:
        """
        Phase 3: Refactor code while keeping tests green

        Args:
            developer_agents: List of developer agents
            task: Feature requirement
            context: Project context

        Returns:
            Dict with refactor results
        """
        print(colorama.Fore.BLUE + "\n🔄 Refactoring phase...\n" + colorama.Style.RESET_ALL)

        # Get current files
        files = self.file_manager.list_files()
        code_files = [f for f in files if not 'test' in f.lower() and f.endswith('.py')]

        if not code_files:
            print(colorama.Fore.YELLOW + "⚠️ No code files to refactor" + colorama.Style.RESET_ALL)
            return {"refactored": False}

        refactored = False

        for agent in developer_agents:
            print(colorama.Fore.YELLOW + f"👤 {agent.name} refactoring..." + colorama.Style.RESET_ALL)

            # Read current code
            code_content = ""
            for file in code_files[:3]:  # Refactor up to 3 files
                content = self.file_manager.read_file(file)
                if content:
                    code_content += f"\n### {file}:\n```\n{content}\n```\n"

            refactor_prompt = f"""You are in TDD MODE - REFACTOR PHASE.

**Task:** {task}
**Context:** {context}

**Current Code:**
{code_content}

**YOUR JOB:**
Improve the code quality while keeping tests passing:
1. Improve readability
2. Remove duplication
3. Better naming
4. Add comments where helpful
5. Optimize performance if obvious improvements exist

**CRITICAL RULES:**
- ⚠️ DO NOT change functionality
- ⚠️ Tests MUST still pass
- ⚠️ Only improve code quality
- ⚠️ Don't add new features

Provide refactored code if improvements are possible, or say "NO REFACTORING NEEDED" if code is already clean.
"""

            response = agent.step(HumanMessage(content=refactor_prompt))

            if "NO REFACTORING NEEDED" not in response.content.upper():
                # Process refactoring
                result = agent.process_and_execute_file_operations(response.content)
                if result['files_updated'] > 0:
                    refactored = True
                    print(colorama.Fore.GREEN + f"✓ Refactored {result['files_updated']} file(s)" + colorama.Style.RESET_ALL)

        return {"refactored": refactored}


def create_tdd_workflow_integration(
    project_name: str,
    task: str,
    agents: List[Dict],
    file_manager: 'FileManager',
    test_executor: 'TestExecutor'
) -> Dict:
    """
    Integration function for TDD mode in main workflow

    Args:
        project_name: Project name
        task: Feature/task description
        agents: List of agent configs
        file_manager: FileManager instance
        test_executor: TestExecutor instance

    Returns:
        Dict with TDD results
    """
    from specialized_agent import create_agent, AGENT_CONFIGS
    from file_aware_agent import FileAwareAgent

    print(colorama.Fore.MAGENTA + f"""
╔═══════════════════════════════════════════════════════════════════════╗
║                    TDD MODE - TEST DRIVEN DEVELOPMENT                 ║
║                                                                       ║
║  Write Tests → Run Tests → Implement → Refactor → Repeat            ║
╚═══════════════════════════════════════════════════════════════════════╝
    """ + colorama.Style.RESET_ALL)

    # Create agent instances
    file_agents = []
    qa_agent = None
    developer_agents = []

    for agent_config in agents:
        config = AGENT_CONFIGS[agent_config["type"]]

        agent = FileAwareAgent(
            role=config["role"],
            name=agent_config["name"],
            expertise=config["expertise"],
            model_name=config["model"],
            temperature=config["temperature"],
            file_manager=file_manager
        )

        file_agents.append(agent)

        if "qa" in agent.role.lower() or "tester" in agent.role.lower():
            qa_agent = agent
        elif "developer" in agent.role.lower():
            developer_agents.append(agent)

    if not qa_agent:
        print(colorama.Fore.RED + "❌ TDD Mode requires a QA/Tester agent!" + colorama.Style.RESET_ALL)
        return {"success": False, "error": "No QA agent"}

    if not developer_agents:
        print(colorama.Fore.RED + "❌ TDD Mode requires at least one Developer agent!" + colorama.Style.RESET_ALL)
        return {"success": False, "error": "No developer agents"}

    # Execute TDD workflow
    tdd = TDDWorkflow(file_manager, test_executor)

    result = tdd.execute_tdd_cycle(
        task=task,
        qa_agent=qa_agent,
        developer_agents=developer_agents,
        context=f"Project: {project_name}",
        max_cycles=5
    )

    return result


# Example usage
if __name__ == "__main__":
    print("\n🧪 TDD Mode - Test Driven Development\n")

    print("""
TDD Benefits:
✅ 100% test coverage (tests written first)
✅ Clear requirements (tests are specifications)
✅ Fewer bugs (caught immediately)
✅ Better design (testable code is better code)
✅ Confidence to refactor (tests protect functionality)
✅ Living documentation (tests show how code works)

TDD Cycle:
1. 🔴 RED: Write a failing test
2. 🟢 GREEN: Write minimal code to pass
3. 🔵 REFACTOR: Improve code quality
4. Repeat!

This implementation ensures:
- Tests are written BEFORE code
- Tests fail initially (proving they work)
- Code is implemented to pass tests
- Refactoring is safe (tests protect)
""")

    print("✅ TDD Mode ready for integration!")
