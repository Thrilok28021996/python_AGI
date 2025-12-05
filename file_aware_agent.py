"""
File-Aware Agent System
Agents can create, read, edit, and analyze actual code files
Similar to how Claude Code works - iterative development with real files
Includes automated testing and test-driven development (TDD) workflow
"""

import os
import json
from typing import List, Dict, Optional, Tuple
from pathlib import Path
from langchain_core.messages import HumanMessage, SystemMessage
from specialized_agent import SpecializedAgent
from test_executor import TestExecutor
import colorama
import re

# Import collaborative systems
try:
    from collaborative_review import CollaborativeReview, TeamReviewOrchestrator
    COLLABORATIVE_REVIEW_AVAILABLE = True
except ImportError:
    COLLABORATIVE_REVIEW_AVAILABLE = False
    print("⚠️ Collaborative review system not available")

try:
    from tdd_mode import TDDWorkflow
    TDD_AVAILABLE = True
except ImportError:
    TDD_AVAILABLE = False
    print("⚠️ TDD mode not available")

try:
    from security_scanner import SecurityScanner
    SECURITY_SCAN_AVAILABLE = True
except ImportError:
    SECURITY_SCAN_AVAILABLE = False
    print("⚠️ Security scanner not available")

try:
    from project_coordination import ProjectCoordinator
    PROJECT_COORDINATION_AVAILABLE = True
except ImportError:
    PROJECT_COORDINATION_AVAILABLE = False
    print("⚠️ Project coordination system not available")

try:
    from company_enhancements import (
        ConflictResolver,
        DocumentationGenerator,
        PerformanceAnalytics
    )
    COMPANY_ENHANCEMENTS_AVAILABLE = True
except ImportError:
    COMPANY_ENHANCEMENTS_AVAILABLE = False
    print("⚠️ Company enhancements (conflict resolution, docs, analytics) not available")

colorama.init(autoreset=True)


class FileManager:
    """
    Manages file operations for agents
    Creates a project workspace where agents can work with real files
    """

    def __init__(self, project_path: str):
        """
        Initialize file manager

        Args:
            project_path: Path where project files will be created
        """
        self.project_path = Path(project_path)
        self.project_path.mkdir(parents=True, exist_ok=True)
        self.file_history = []  # Track all file operations

    def create_file(self, file_path: str, content: str, agent_name: str = "Unknown") -> bool:
        """
        Create a new file with content

        Args:
            file_path: Relative path from project root
            content: File content
            agent_name: Which agent created this file

        Returns:
            True if successful
        """
        try:
            full_path = self.project_path / file_path
            full_path.parent.mkdir(parents=True, exist_ok=True)

            with open(full_path, 'w') as f:
                f.write(content)

            self.file_history.append({
                "action": "create",
                "file": file_path,
                "agent": agent_name,
                "success": True
            })

            print(colorama.Fore.GREEN + f"  ✓ Created: {file_path}" + colorama.Style.RESET_ALL)
            return True

        except Exception as e:
            print(colorama.Fore.RED + f"  ✗ Error creating {file_path}: {e}" + colorama.Style.RESET_ALL)
            self.file_history.append({
                "action": "create",
                "file": file_path,
                "agent": agent_name,
                "success": False,
                "error": str(e)
            })
            return False

    def read_file(self, file_path: str) -> Optional[str]:
        """
        Read a file's content

        Args:
            file_path: Relative path from project root

        Returns:
            File content or None if error
        """
        try:
            full_path = self.project_path / file_path
            with open(full_path, 'r') as f:
                return f.read()
        except Exception as e:
            print(colorama.Fore.RED + f"  ✗ Error reading {file_path}: {e}" + colorama.Style.RESET_ALL)
            return None

    def update_file(self, file_path: str, content: str, agent_name: str = "Unknown") -> bool:
        """
        Update an existing file

        Args:
            file_path: Relative path from project root
            content: New content
            agent_name: Which agent updated this file

        Returns:
            True if successful
        """
        try:
            full_path = self.project_path / file_path

            # Only backup if file exists and content is different
            if full_path.exists():
                with open(full_path, 'r') as f:
                    old_content = f.read()

                # Only create backup if content is actually different
                if old_content != content:
                    backup_path = full_path.with_suffix(full_path.suffix + '.backup')
                    with open(backup_path, 'w') as b:
                        b.write(old_content)
                else:
                    # Content is same, no need to update
                    return True

            with open(full_path, 'w') as f:
                f.write(content)

            self.file_history.append({
                "action": "update",
                "file": file_path,
                "agent": agent_name,
                "success": True
            })

            print(colorama.Fore.YELLOW + f"  ↻ Updated: {file_path}" + colorama.Style.RESET_ALL)
            return True

        except Exception as e:
            print(colorama.Fore.RED + f"  ✗ Error updating {file_path}: {e}" + colorama.Style.RESET_ALL)
            return False

    def list_files(self, pattern: str = "**/*") -> List[str]:
        """
        List all files in project matching pattern

        Args:
            pattern: Glob pattern (default: all files)

        Returns:
            List of relative file paths (automatically excludes system files like .DS_Store)
        """
        from utils import should_ignore_file

        files = []
        for file_path in self.project_path.glob(pattern):
            # Skip system files using centralized filter
            if file_path.is_file() and not should_ignore_file(file_path):
                rel_path = file_path.relative_to(self.project_path)
                files.append(str(rel_path))
        return sorted(files)

    def get_project_structure(self) -> str:
        """Get a tree view of the project structure"""
        files = self.list_files()
        if not files:
            return "Project is empty"

        lines = ["Project Structure:"]
        for file_path in files:
            indent = "  " * (len(Path(file_path).parts) - 1)
            lines.append(f"{indent}├── {Path(file_path).name}")

        return "\n".join(lines)


class FileAwareAgent(SpecializedAgent):
    """
    Enhanced agent that can work with actual files
    Can create, read, and modify code files
    """

    def __init__(self, role: str, name: str, expertise: List[str],
                 model_name: str, temperature: float, file_manager: FileManager):
        super().__init__(role, name, expertise, model_name, temperature)
        self.file_manager = file_manager

        # Enhance system message with file operation instructions
        self.system_message = self._create_file_aware_system_message()
        self.init_messages()

    def _create_file_aware_system_message(self) -> SystemMessage:
        """Create system message that includes file operation instructions"""

        expertise_str = ", ".join(self.expertise)

        content = f"""You are {self.name}, a {self.role} in a software development company.

Your expertise includes: {expertise_str}

**IMPORTANT: You can create and modify actual code files!**

When working on tasks, you should:
1. CREATE files using this format:
   ```filename: path/to/file.py
   [file content here]
   ```

2. UPDATE existing files by showing the full new content:
   ```update: path/to/file.py
   [complete new file content]
   ```

3. REFERENCE files you want to read:
   ```read: path/to/file.py```

Your responsibilities as {self.role}:
{self._get_role_responsibilities()}

**COMMUNICATION FORMAT:**

Response:
[Your analysis and decisions]

Files to Create/Update:
[List any files you want to create or modify using the format above]

Analysis:
[Your analysis of existing code if reviewing]

Recommendations:
[Specific improvements or next steps]

IMPORTANT:
- Always provide complete, working code
- Include proper error handling
- Follow best practices for {self.role}
- Create files iteratively - start simple, then improve
"""
        return SystemMessage(content=content)

    def _get_role_responsibilities(self) -> str:
        """Get specific responsibilities for file operations"""
        # Use parent class responsibilities
        return super()._get_role_responsibilities()

    def _is_completion_signal(self, response: str) -> bool:
        """
        Detect if agent response signals completion

        Args:
            response: The agent's response text

        Returns:
            True if response indicates task is complete
        """
        completion_keywords = [
            "project is complete",
            "task is complete",
            "implementation is complete",
            "all requirements met",
            "no further improvements needed",
            "ready for deployment",
            "ready to deploy",
            "fully implemented",
            "everything is working",
            "all tests passing",
            "no issues found",
            "project complete",
            "task complete",
            "TASK_DONE",
            "project finished",
            "implementation finished"
        ]

        response_lower = response.lower()

        # Check for explicit completion keywords
        for keyword in completion_keywords:
            if keyword in response_lower:
                return True

        # Check for patterns like "no more changes needed"
        if "no more" in response_lower and any(word in response_lower for word in ["changes", "improvements", "updates", "modifications"]):
            return True

        return False

    def process_and_execute_file_operations(self, response_content: str) -> Dict:
        """
        Parse agent response and execute file operations

        Args:
            response_content: The agent's response text

        Returns:
            Dict with created/updated files and any errors
        """
        operations = {
            "created": [],
            "updated": [],
            "read": [],
            "errors": []
        }

        # Extract file operations from response
        file_blocks = self._extract_file_blocks(response_content)

        for operation, file_path, content in file_blocks:
            if operation == "create":
                success = self.file_manager.create_file(file_path, content, self.name)
                if success:
                    operations["created"].append(file_path)
                else:
                    operations["errors"].append(f"Failed to create {file_path}")

            elif operation == "update":
                success = self.file_manager.update_file(file_path, content, self.name)
                if success:
                    operations["updated"].append(file_path)
                else:
                    operations["errors"].append(f"Failed to update {file_path}")

            elif operation == "read":
                content = self.file_manager.read_file(file_path)
                if content:
                    operations["read"].append((file_path, content))
                else:
                    operations["errors"].append(f"Failed to read {file_path}")

        return operations

    def _extract_file_blocks(self, text: str) -> List[Tuple[str, str, str]]:
        """
        Extract file operation blocks from agent response

        Returns:
            List of (operation, file_path, content) tuples
        """
        operations = []

        # Pattern for create/update blocks
        # ```filename: path/to/file.ext or ```update: path/to/file.ext
        pattern = r'```(?:filename|update|read):\s*(\S+)\s*\n(.*?)```'

        matches = re.findall(pattern, text, re.DOTALL)

        for match in matches:
            file_path = match[0].strip()

            # Sanitize filename - remove backticks, quotes, and invalid characters
            file_path = file_path.replace('`', '').replace('"', '').replace("'", '')
            file_path = re.sub(r'[^\w\s\-_./]', '', file_path)  # Remove invalid chars
            file_path = file_path.strip()

            # Skip if filename is empty after sanitization
            if not file_path:
                continue

            content = match[1].strip()

            # Determine operation type
            if '```filename:' in text or '```create:' in text:
                operation = "create"
            elif '```update:' in text:
                operation = "update"
            elif '```read:' in text:
                operation = "read"
            else:
                operation = "create"  # Default

            # Find which operation it actually is
            before_match = text[:text.find(match[0])]
            if '```update:' in before_match[-50:]:
                operation = "update"
            elif '```read:' in before_match[-50:]:
                operation = "read"
            elif '```filename:' in before_match[-50:] or '```create:' in before_match[-50:]:
                operation = "create"

            operations.append((operation, file_path, content))

        return operations


def create_project_workflow(
    project_name: str,
    task: str,
    agents: List[Dict],
    output_dir: str = "./generated_projects",
    max_iterations: int = 10,
    stop_on_complete: bool = True,
    min_iterations: int = 2,
    enable_testing: bool = True,
    test_command: Optional[str] = None,
    enable_collaborative_review: bool = True,
    enable_security_scan: bool = True,
    use_tdd: bool = False,
    enable_pm_coordination: bool = True
) -> Dict:
    """
    Complete workflow: agents create a project with actual files
    Includes automated testing, collaborative review, security scanning, PM coordination, and optional TDD

    Args:
        project_name: Name of the project
        task: Project description
        agents: List of agent configs [{"type": "backend_developer", "name": "Bob"}, ...]
        output_dir: Where to create project
        max_iterations: Maximum improvement cycles (default: 10)
        stop_on_complete: Stop when agents signal completion (default: True)
        min_iterations: Minimum iterations before checking completion (default: 2)
        enable_testing: Run tests after each iteration and provide feedback (default: True)
        test_command: Custom test command (default: auto-detect)
        enable_collaborative_review: Enable peer code review between agents (default: True)
        enable_security_scan: Run security vulnerability scan (default: True)
        enable_pm_coordination: Enable Project Manager coordination (default: True)
        use_tdd: Use Test-Driven Development mode (tests first) (default: False)

    Returns:
        Dict with project path, test results, and operations
    """
    print(colorama.Fore.MAGENTA + f"""
╔═══════════════════════════════════════════════════════════════════════╗
║              FILE-AWARE PROJECT BUILDER                               ║
║                                                                       ║
║  Agents will create actual code files for your project!              ║
╚═══════════════════════════════════════════════════════════════════════╝
    """ + colorama.Style.RESET_ALL)

    print(colorama.Fore.CYAN + f"\n📁 Project: {project_name}")
    print(f"📋 Task: {task}\n" + colorama.Style.RESET_ALL)

    # Create project directory
    project_path = os.path.join(output_dir, project_name)
    file_manager = FileManager(project_path)

    # Initialize test executor if testing is enabled
    test_executor = None
    if enable_testing:
        test_executor = TestExecutor(project_path)
        print(colorama.Fore.CYAN + "🧪 Testing enabled: Will run tests after each iteration\n" + colorama.Style.RESET_ALL)

    # Create file-aware agents
    file_agents = []
    for agent_config in agents:
        from specialized_agent import AGENT_CONFIGS

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

    print(colorama.Fore.YELLOW + f"👥 Team: {', '.join(f'{a.name} ({a.role})' for a in file_agents)}\n" + colorama.Style.RESET_ALL)

    # Initialize collaborative review system if enabled
    collaborative_review = None
    team_review_orchestrator = None
    if enable_collaborative_review and COLLABORATIVE_REVIEW_AVAILABLE:
        collaborative_review = CollaborativeReview()
        team_review_orchestrator = TeamReviewOrchestrator()
        print(colorama.Fore.CYAN + "👥 Collaborative Review enabled: Agents will peer-review each other's code\n" + colorama.Style.RESET_ALL)

    # Initialize TDD workflow if enabled
    tdd_workflow = None
    if use_tdd and TDD_AVAILABLE:
        tdd_workflow = TDDWorkflow(file_manager, test_executor if test_executor else TestExecutor(project_path))
        print(colorama.Fore.CYAN + "🔴 TDD Mode enabled: Tests will be written first (RED→GREEN→REFACTOR)\n" + colorama.Style.RESET_ALL)

    # Initialize security scanner if enabled
    security_scanner = None
    if enable_security_scan and SECURITY_SCAN_AVAILABLE:
        security_scanner = SecurityScanner(project_path)
        print(colorama.Fore.CYAN + "🔒 Security Scan enabled: Will scan for vulnerabilities\n" + colorama.Style.RESET_ALL)

    # Initialize Project Manager coordination if enabled
    pm_coordinator = None
    if enable_pm_coordination and PROJECT_COORDINATION_AVAILABLE:
        pm_coordinator = ProjectCoordinator(project_name, task)
        print(colorama.Fore.CYAN + "👔 Project Manager enabled: Will coordinate team and track progress\n" + colorama.Style.RESET_ALL)

    # Initialize Company Enhancements (Conflict Resolution, Docs, Analytics)
    conflict_resolver = None
    doc_generator = None
    performance_analytics = None
    if COMPANY_ENHANCEMENTS_AVAILABLE:
        conflict_resolver = ConflictResolver()
        doc_generator = DocumentationGenerator()
        performance_analytics = PerformanceAnalytics()
        print(colorama.Fore.CYAN + "🏢 Company Enhancements enabled: Conflict resolution, auto-docs, performance tracking\n" + colorama.Style.RESET_ALL)

    if stop_on_complete:
        print(colorama.Fore.CYAN + "🎯 Auto-stop enabled: Will stop when project is complete" + colorama.Style.RESET_ALL)
        print(colorama.Fore.CYAN + f"   (Min iterations: {min_iterations}, Max: {max_iterations})\n" + colorama.Style.RESET_ALL)

    all_operations = []
    completion_signals = []  # Track completion signals from agents
    test_results = None  # Initialize test results
    review_results = []  # Track all review results

    # If TDD mode is enabled, run TDD workflow instead of regular iterations
    if use_tdd and tdd_workflow:
        print(colorama.Fore.MAGENTA + f"\n{'='*80}")
        print(f"🔴 STARTING TDD WORKFLOW (Test-Driven Development)")
        print(f"{'='*80}\n" + colorama.Style.RESET_ALL)

        # Find QA and developer agents
        qa_agents = [a for a in file_agents if "qa" in a.role.lower() or "tester" in a.role.lower()]
        developer_agents = [a for a in file_agents if "developer" in a.role.lower()]

        if not qa_agents:
            print(colorama.Fore.RED + "⚠️ TDD mode requires a QA/Tester agent! Falling back to regular workflow." + colorama.Style.RESET_ALL)
        elif not developer_agents:
            print(colorama.Fore.RED + "⚠️ TDD mode requires developer agents! Falling back to regular workflow." + colorama.Style.RESET_ALL)
        else:
            # Run TDD cycle
            tdd_result = tdd_workflow.execute_tdd_cycle(
                task=task,
                qa_agent=qa_agents[0],  # Use first QA agent
                developer_agents=developer_agents,
                context=f"Project: {project_name}",
                max_cycles=max_iterations
            )

            # Get final test results
            test_results = tdd_result.get("final_test_results")

            # Add TDD operations to all_operations
            all_operations.append({
                "iteration": "TDD",
                "type": "tdd_workflow",
                "result": tdd_result
            })

            # Skip regular iteration loop
            print(colorama.Fore.GREEN + f"\n✅ TDD workflow complete!" + colorama.Style.RESET_ALL)

    # Regular iteration loop: create, review, improve (skipped if TDD mode used)
    if not (use_tdd and tdd_workflow and qa_agents and developer_agents):
        for iteration in range(max_iterations):
            print(colorama.Fore.CYAN + f"\n{'='*80}")
            print(f"ITERATION {iteration + 1}/{max_iterations}")
            print(f"{'='*80}\n" + colorama.Style.RESET_ALL)

            # PM plans iteration (if enabled)
            iteration_plan = None
            if pm_coordinator:
                current_files = file_manager.list_files()
                previous_results = {
                    'final_test_results': test_results
                } if iteration > 0 else None

                iteration_plan = pm_coordinator.plan_iteration(
                    team=file_agents,
                    current_files=current_files,
                    previous_results=previous_results
                )

            iteration_completion_count = 0  # Count agents saying "done" this iteration

            for agent in file_agents:
                print(colorama.Fore.YELLOW + f"\n>>> {agent.name} ({agent.role}) working...\n" + colorama.Style.RESET_ALL)

                # Build context for agent
                if iteration == 0:
                    # First iteration: create initial files
                    context = f"""Create the initial implementation for this project:

{task}

Project Structure so far:
{file_manager.get_project_structure()}

Your task: Create the files needed for your part of the project.
Use the ```filename: path/to/file.ext format to create files.
"""
                else:
                    # Later iterations: review and improve
                    existing_files = file_manager.list_files()
                    files_content = ""
                    for file_path in existing_files:
                        content = file_manager.read_file(file_path)
                        files_content += f"\n--- {file_path} ---\n{content}\n"

                    context = f"""Review and improve the project:

{task}

Current Project Structure:
{file_manager.get_project_structure()}

Existing Files:
{files_content}

Your task: Review the code and make improvements. Fix any issues you find.
Use ```update: path/to/file.ext to modify existing files.
Use ```filename: path/to/file.ext to create new files if needed.

IMPORTANT: If you believe the project is complete and meets all requirements,
clearly state "Project is complete" or "Task is complete" in your response.
Only do this if:
- All core functionality is implemented
- Code quality is good
- No critical issues remain
- Your part of the project is finished
"""

                # Get agent response
                response = agent.step(HumanMessage(content=context))

                # Execute file operations
                print(colorama.Fore.GREEN + f"\n{agent.name} creating/updating files:" + colorama.Style.RESET_ALL)
                operations = agent.process_and_execute_file_operations(response.content)
                all_operations.append({
                    "iteration": iteration + 1,
                    "agent": agent.name,
                    "operations": operations
                })

                # Print summary
                if operations["created"]:
                    print(colorama.Fore.GREEN + f"  Created {len(operations['created'])} files" + colorama.Style.RESET_ALL)
                if operations["updated"]:
                    print(colorama.Fore.YELLOW + f"  Updated {len(operations['updated'])} files" + colorama.Style.RESET_ALL)
                if operations["errors"]:
                    print(colorama.Fore.RED + f"  Errors: {len(operations['errors'])}" + colorama.Style.RESET_ALL)

                # Track performance analytics
                if performance_analytics:
                    for _ in operations["created"]:
                        performance_analytics.record_agent_contribution(
                            agent_name=agent.name,
                            contribution_type="file_created",
                            details={"iteration": iteration + 1}
                        )
                    for _ in operations["updated"]:
                        performance_analytics.record_agent_contribution(
                            agent_name=agent.name,
                            contribution_type="file_updated",
                            details={"iteration": iteration + 1}
                        )

                # Collaborative Review: If enabled and files were created/updated, have peers review
                if collaborative_review and team_review_orchestrator and iteration > 0:
                    files_to_review = operations["created"] + operations["updated"]
                    if files_to_review:
                        print(colorama.Fore.MAGENTA + f"\n👥 Initiating peer review for {agent.name}'s code..." + colorama.Style.RESET_ALL)

                        # Determine which agents should review this work
                        reviewer_agents = team_review_orchestrator.determine_reviewers(
                            author_role=agent.role,
                            file_path=files_to_review[0] if files_to_review else "",
                            all_agents=file_agents
                        )

                        # Filter out the author from reviewers
                        reviewer_agents = [r for r in reviewer_agents if r.name != agent.name]

                        if reviewer_agents:
                            # Review each created/updated file
                            for file_path in files_to_review[:3]:  # Limit to 3 files per agent to avoid overwhelming reviews
                                code_content = file_manager.read_file(file_path)
                                if code_content:
                                    review_result = collaborative_review.conduct_review(
                                        file_path=file_path,
                                        code_content=code_content,
                                        author_agent=agent,
                                        reviewer_agents=reviewer_agents,
                                        context=task,
                                        file_manager=file_manager,
                                        max_rounds=2  # Limit review rounds to keep workflow moving
                                    )

                                    review_results.append({
                                        "iteration": iteration + 1,
                                        "file": file_path,
                                        "author": agent.name,
                                        "result": review_result
                                    })

                                    # Track review contributions
                                    if performance_analytics:
                                        # Author received review
                                        performance_analytics.record_agent_contribution(
                                            agent_name=agent.name,
                                            contribution_type="review_received",
                                            details={"file": file_path, "iteration": iteration + 1}
                                        )
                                        # Reviewers gave review
                                        for reviewer in reviewer_agents:
                                            performance_analytics.record_agent_contribution(
                                                agent_name=reviewer.name,
                                                contribution_type="review_given",
                                                details={"file": file_path, "iteration": iteration + 1}
                                            )

                                    # If review led to improvements, update operations tracking
                                    if review_result.get("rounds_completed", 0) > 1:
                                        print(colorama.Fore.GREEN + f"  ✓ Code improved through {review_result['rounds_completed']} review rounds" + colorama.Style.RESET_ALL)

                # Check if agent signals completion
                if stop_on_complete and agent._is_completion_signal(response.content):
                    iteration_completion_count += 1
                    completion_signals.append({
                        "agent": agent.name,
                        "iteration": iteration + 1
                    })
                    print(colorama.Fore.CYAN + f"  ✓ {agent.name} signals: Project looks complete" + colorama.Style.RESET_ALL)

            # After all agents in this iteration, run tests if enabled
            if test_executor and iteration > 0:  # Skip testing on first iteration (no code yet)
                print(colorama.Fore.CYAN + f"\n{'='*80}")
                print(f"RUNNING TESTS FOR ITERATION {iteration + 1}")
                print(f"{'='*80}\n" + colorama.Style.RESET_ALL)

                test_results = test_executor.run_tests(test_command)

                # If tests failed, provide feedback to developers for next iteration
                if not test_results.get("success", False) and iteration < max_iterations - 1:
                    print(colorama.Fore.YELLOW + f"\n⚠️ Tests failed! Providing feedback to developers for fixes...\n" + colorama.Style.RESET_ALL)

                    # Generate feedback for developers
                    test_feedback = test_executor.format_feedback_for_developer(test_results)

                    # Find developer agents to give them test feedback
                    developer_agents = [a for a in file_agents if "developer" in a.role.lower()]

                    if developer_agents:
                        print(colorama.Fore.YELLOW + f"🔧 Running fix iteration with {len(developer_agents)} developer(s)...\n" + colorama.Style.RESET_ALL)

                        for dev_agent in developer_agents:
                            print(colorama.Fore.YELLOW + f"\n>>> {dev_agent.name} fixing test failures...\n" + colorama.Style.RESET_ALL)

                            # Build context with test failures
                            existing_files = file_manager.list_files()
                            files_content = ""
                            for file_path in existing_files:
                                content = file_manager.read_file(file_path)
                                files_content += f"\n--- {file_path} ---\n{content}\n"

                            fix_context = f"""{test_feedback}

Current Project Files:
{files_content}

Your task: Fix the bugs causing test failures.
- Read the test files to understand what's expected
- Identify the bugs in the implementation
- Provide fixed code using ```update: path/to/file.ext format
- Explain what was wrong and how you fixed it

CRITICAL: Focus ONLY on fixing the failing tests. Do not add new features."""

                            # Get developer's fix
                            fix_response = dev_agent.step(HumanMessage(content=fix_context))

                            # Execute file operations
                            print(colorama.Fore.GREEN + f"\n{dev_agent.name} applying fixes:" + colorama.Style.RESET_ALL)
                            fix_operations = dev_agent.process_and_execute_file_operations(fix_response.content)
                            all_operations.append({
                                "iteration": iteration + 1,
                                "agent": dev_agent.name,
                                "type": "test_fix",
                                "operations": fix_operations
                            })

                            if fix_operations["updated"]:
                                print(colorama.Fore.GREEN + f"  Fixed {len(fix_operations['updated'])} files" + colorama.Style.RESET_ALL)

                        # Re-run tests after fixes
                        print(colorama.Fore.CYAN + f"\n{'='*80}")
                        print(f"RE-RUNNING TESTS AFTER FIXES")
                        print(f"{'='*80}\n" + colorama.Style.RESET_ALL)

                        test_results = test_executor.run_tests(test_command)

            # After all agents in this iteration, check if we should stop
            if stop_on_complete and iteration >= min_iterations - 1:
                # Calculate percentage of agents who signaled completion this iteration
                completion_percentage = iteration_completion_count / len(file_agents)

                print(colorama.Fore.CYAN + f"\n📊 Completion Status: {iteration_completion_count}/{len(file_agents)} agents signal complete ({completion_percentage*100:.0f}%)" + colorama.Style.RESET_ALL)

                # Stop if 70% or more agents agree project is complete
                if completion_percentage >= 0.7:
                    print(colorama.Fore.GREEN + f"\n🎉 Majority of agents agree project is complete!" + colorama.Style.RESET_ALL)
                    print(colorama.Fore.GREEN + f"   Stopping after iteration {iteration + 1}/{max_iterations}" + colorama.Style.RESET_ALL)
                    break
                elif completion_percentage > 0:
                    print(colorama.Fore.YELLOW + f"   Some agents think it's complete, but continuing for more refinement..." + colorama.Style.RESET_ALL)

    # Run final security scan if enabled
    security_scan_results = None
    if security_scanner:
        print(colorama.Fore.MAGENTA + f"\n{'='*80}")
        print(f"🔒 RUNNING SECURITY SCAN")
        print(f"{'='*80}\n" + colorama.Style.RESET_ALL)

        security_scan_results = security_scanner.scan_project()

        # Display security scan summary
        vulnerability_count = len(security_scan_results.get("vulnerabilities", []))
        if vulnerability_count == 0:
            print(colorama.Fore.GREEN + "✅ No security vulnerabilities detected!" + colorama.Style.RESET_ALL)
        else:
            print(colorama.Fore.YELLOW + f"⚠️ Found {vulnerability_count} potential security issues:" + colorama.Style.RESET_ALL)

            # Group by severity
            by_severity = {}
            for vuln in security_scan_results.get("vulnerabilities", []):
                severity = vuln.get("severity", "UNKNOWN")
                by_severity[severity] = by_severity.get(severity, 0) + 1

            for severity in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]:
                if severity in by_severity:
                    color = colorama.Fore.RED if severity in ["CRITICAL", "HIGH"] else colorama.Fore.YELLOW
                    print(color + f"  {severity}: {by_severity[severity]}" + colorama.Style.RESET_ALL)

            # Show critical issues
            critical_issues = [v for v in security_scan_results.get("vulnerabilities", [])
                             if v.get("severity") in ["CRITICAL", "HIGH"]]
            if critical_issues:
                print(colorama.Fore.RED + f"\n⚠️ CRITICAL ISSUES REQUIRE IMMEDIATE ATTENTION:" + colorama.Style.RESET_ALL)
                for issue in critical_issues[:5]:  # Show first 5
                    print(colorama.Fore.RED + f"  • {issue.get('type', 'unknown')} in {issue.get('file', 'unknown')}" + colorama.Style.RESET_ALL)
                    print(f"    Line {issue.get('line', 'unknown')}: {issue.get('description', 'No description')}")

    # PM conducts retrospective (if enabled)
    retrospective_result = None
    if pm_coordinator:
        final_results_for_retro = {
            'final_test_results': test_results,
            'security_scan_results': security_scan_results,
            'review_results': review_results
        }
        retrospective_result = pm_coordinator.conduct_retrospective(final_results_for_retro)

    # Final summary
    print(colorama.Fore.GREEN + f"\n\n{'='*80}")
    print(f"✅ PROJECT COMPLETE!")
    print(f"{'='*80}\n" + colorama.Style.RESET_ALL)

    print(f"📁 Project created at: {project_path}")
    print(f"\n{file_manager.get_project_structure()}")

    final_files = file_manager.list_files()
    print(colorama.Fore.CYAN + f"\n📊 Total files created: {len(final_files)}" + colorama.Style.RESET_ALL)

    # Show collaborative review summary if any reviews were conducted
    if review_results:
        total_reviews = len(review_results)
        improved_count = sum(1 for r in review_results if r["result"].get("rounds_completed", 0) > 1)
        print(colorama.Fore.CYAN + f"\n👥 Collaborative Reviews: {total_reviews} code reviews conducted" + colorama.Style.RESET_ALL)
        if improved_count > 0:
            print(colorama.Fore.GREEN + f"  ✓ {improved_count} files improved through peer feedback" + colorama.Style.RESET_ALL)

    # Show completion signals if any
    if completion_signals:
        print(colorama.Fore.CYAN + f"\n✓ Completion signals received from: {', '.join([s['agent'] for s in completion_signals])}" + colorama.Style.RESET_ALL)

    # Show final test results if testing was enabled
    if test_executor:
        print(colorama.Fore.CYAN + f"\n📊 Test Summary:" + colorama.Style.RESET_ALL)
        print(test_executor.get_test_history_summary())

    # Show security scan summary if available
    if security_scan_results:
        vulnerability_count = len(security_scan_results.get("vulnerabilities", []))
        if vulnerability_count == 0:
            print(colorama.Fore.GREEN + f"\n🔒 Security: No vulnerabilities detected" + colorama.Style.RESET_ALL)
        else:
            print(colorama.Fore.YELLOW + f"\n🔒 Security: {vulnerability_count} potential issues found (review required)" + colorama.Style.RESET_ALL)

    # Generate auto-documentation if enabled
    readme_content = None
    if doc_generator:
        try:
            # Get main files content for better documentation
            main_files_content = {}
            for file_path in final_files[:5]:  # Top 5 files
                content = file_manager.read_file(file_path)
                if content:
                    main_files_content[file_path] = content

            readme_content = doc_generator.generate_readme(
                project_name=project_name,
                project_files=final_files,
                main_files_content=main_files_content
            )

            # Save README.md
            readme_path = os.path.join(project_path, "README.md")
            with open(readme_path, 'w') as f:
                f.write(readme_content)

            print(colorama.Fore.GREEN + f"\n📝 Auto-documentation: README.md generated" + colorama.Style.RESET_ALL)
        except Exception as e:
            print(colorama.Fore.YELLOW + f"\n⚠️ Could not generate documentation: {e}" + colorama.Style.RESET_ALL)

    # Show performance analytics if enabled
    performance_report = None
    if performance_analytics:
        try:
            # Calculate quality scores for each agent
            for agent in file_agents:
                # Get review feedback for this agent
                review_feedback = []
                for review in review_results:
                    if review.get("author") == agent.name:
                        result = review.get("result", {})
                        for round_data in result.get("rounds", []):
                            for reviewer_feedback in round_data.get("reviews", []):
                                review_feedback.append(reviewer_feedback.get("feedback", ""))

                # Calculate test pass rate
                test_pass_rate = 1.0 if test_results and test_results.get("success") else 0.7

                # Calculate quality score
                performance_analytics.calculate_code_quality_score(
                    agent_name=agent.name,
                    review_feedback=review_feedback,
                    test_pass_rate=test_pass_rate
                )

            # Display performance report
            performance_analytics.display_performance_report()
            performance_report = performance_analytics.generate_performance_report()
        except Exception as e:
            print(colorama.Fore.YELLOW + f"\n⚠️ Could not generate performance analytics: {e}" + colorama.Style.RESET_ALL)

    return {
        "project_path": project_path,
        "files": final_files,
        "operations": all_operations,
        "file_manager": file_manager,
        "completion_signals": completion_signals,
        "stopped_early": len(completion_signals) > 0 and stop_on_complete,
        "test_history": test_executor.test_history if test_executor else [],
        "final_test_results": test_results if test_executor else None,
        "review_results": review_results if review_results else [],
        "security_scan_results": security_scan_results if security_scan_results else None,
        "performance_report": performance_report if performance_report else None,
        "readme_generated": readme_content is not None
    }


if __name__ == "__main__":
    # Example usage with auto-stop enabled
    result = create_project_workflow(
        project_name="todo_api",
        task="Create a simple REST API for a todo list application with FastAPI. Include endpoints for creating, reading, updating, and deleting todos. Add proper error handling and a simple README.",
        agents=[
            {"type": "backend_developer", "name": "Alice"},
            {"type": "qa_tester", "name": "Bob"},
        ],
        max_iterations=5,  # Set max, but will stop early if agents agree it's complete
        stop_on_complete=True,  # Default: auto-stop when complete
        min_iterations=2  # Require at least 2 iterations before checking completion
    )

    print(f"\n\nProject files saved to: {result['project_path']}")
    if result.get('stopped_early'):
        print("✅ Project completed early - agents agreed it was done!")
    print(f"Completion signals: {len(result.get('completion_signals', []))}")
