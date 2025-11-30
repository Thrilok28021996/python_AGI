"""
File-Aware Agent System
Agents can create, read, edit, and analyze actual code files
Similar to how Claude Code works - iterative development with real files
"""

import os
import json
from typing import List, Dict, Optional, Tuple
from pathlib import Path
from langchain_core.messages import HumanMessage, SystemMessage
from specialized_agent import SpecializedAgent
import colorama
import re

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

            # Backup old version
            if full_path.exists():
                backup_path = full_path.with_suffix(full_path.suffix + '.backup')
                with open(full_path, 'r') as f:
                    with open(backup_path, 'w') as b:
                        b.write(f.read())

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
            List of relative file paths
        """
        files = []
        for file_path in self.project_path.glob(pattern):
            if file_path.is_file() and not file_path.name.endswith('.backup'):
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
    min_iterations: int = 2
) -> Dict:
    """
    Complete workflow: agents create a project with actual files

    Args:
        project_name: Name of the project
        task: Project description
        agents: List of agent configs [{"type": "backend_developer", "name": "Bob"}, ...]
        output_dir: Where to create project
        max_iterations: Maximum improvement cycles (default: 10)
        stop_on_complete: Stop when agents signal completion (default: True)
        min_iterations: Minimum iterations before checking completion (default: 2)

    Returns:
        Dict with project path and results
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

    print(colorama.Fore.YELLOW + f"👥 Team: {', '.join(a.name for a in file_agents)}\n" + colorama.Style.RESET_ALL)

    if stop_on_complete:
        print(colorama.Fore.CYAN + "🎯 Auto-stop enabled: Will stop when project is complete" + colorama.Style.RESET_ALL)
        print(colorama.Fore.CYAN + f"   (Min iterations: {min_iterations}, Max: {max_iterations})\n" + colorama.Style.RESET_ALL)

    all_operations = []
    completion_signals = []  # Track completion signals from agents

    # Iteration loop: create, review, improve
    for iteration in range(max_iterations):
        print(colorama.Fore.CYAN + f"\n{'='*80}")
        print(f"ITERATION {iteration + 1}/{max_iterations}")
        print(f"{'='*80}\n" + colorama.Style.RESET_ALL)

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

            # Check if agent signals completion
            if stop_on_complete and agent._is_completion_signal(response.content):
                iteration_completion_count += 1
                completion_signals.append({
                    "agent": agent.name,
                    "iteration": iteration + 1
                })
                print(colorama.Fore.CYAN + f"  ✓ {agent.name} signals: Project looks complete" + colorama.Style.RESET_ALL)

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

    # Final summary
    print(colorama.Fore.GREEN + f"\n\n{'='*80}")
    print(f"✅ PROJECT COMPLETE!")
    print(f"{'='*80}\n" + colorama.Style.RESET_ALL)

    print(f"📁 Project created at: {project_path}")
    print(f"\n{file_manager.get_project_structure()}")

    final_files = file_manager.list_files()
    print(colorama.Fore.CYAN + f"\n📊 Total files created: {len(final_files)}" + colorama.Style.RESET_ALL)

    # Show completion signals if any
    if completion_signals:
        print(colorama.Fore.CYAN + f"\n✓ Completion signals received from: {', '.join([s['agent'] for s in completion_signals])}" + colorama.Style.RESET_ALL)

    return {
        "project_path": project_path,
        "files": final_files,
        "operations": all_operations,
        "file_manager": file_manager,
        "completion_signals": completion_signals,
        "stopped_early": len(completion_signals) > 0 and stop_on_complete
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
