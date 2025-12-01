"""
Task/Project Rewriter
Rewrites user task descriptions to be clearer and more detailed while preserving meaning
The rewritten task is then used by agents for better understanding and execution
"""

from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage
from typing import Dict
import colorama

colorama.init(autoreset=True)


class TaskRewriter:
    """
    Rewrites user tasks/projects to be clearer, more detailed, and better structured
    while preserving the original meaning and intent
    """

    def __init__(self, model_name: str = "llama3.2", temperature: float = 0.3):
        """
        Initialize the task rewriter

        Args:
            model_name: LLM model to use for rewriting
            temperature: Lower = more focused, higher = more creative (0.0-1.0)
        """
        self.model_name = model_name
        self.temperature = temperature
        self.llm = ChatOllama(
            model=model_name,
            temperature=temperature
        )

    def rewrite_task(self, original_task: str, project_type: str = "general") -> Dict:
        """
        Rewrite a task description to be clearer and more detailed

        Args:
            original_task: The original task/project description from user
            project_type: Type of project (general, web_app, api, cli, library, etc.)

        Returns:
            Dict with original task, rewritten task, and improvements made
        """
        print(colorama.Fore.CYAN + "\n🔄 Rewriting task for better clarity...\n" + colorama.Style.RESET_ALL)

        system_prompt = """You are a technical project requirements analyst.

Your job is to take a user's brief project description and rewrite it to be:
1. **Clearer** - Remove ambiguity
2. **More Detailed** - Add necessary details while preserving meaning
3. **Structured** - Organize requirements logically
4. **Actionable** - Make it easy for developers to understand what to build

CRITICAL RULES:
- **PRESERVE THE ORIGINAL MEANING** - Do not change what the user wants
- **DO NOT ADD NEW FEATURES** - Only clarify existing intent
- **DO NOT REMOVE REQUIREMENTS** - Keep all user requirements
- **EXPAND ON IMPLICIT NEEDS** - Make implicit requirements explicit

Format your rewritten task as:

# Project Goal
[Clear 1-2 sentence description of what to build]

# Core Requirements
- [Requirement 1]
- [Requirement 2]
- [etc.]

# Technical Specifications
- [Technical detail 1]
- [Technical detail 2]
- [etc.]

# Success Criteria
- [How to know when it's complete]

# Notes
[Any additional context or clarifications]
"""

        user_prompt = f"""Original task from user:
"{original_task}"

Project type: {project_type}

Please rewrite this task to be clearer and more detailed while preserving the original meaning.
DO NOT add features the user didn't ask for.
DO make implicit requirements explicit (e.g., if they say "REST API" they implicitly need endpoints, error handling, etc.)."""

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ]

        try:
            response = self.llm.invoke(messages)
            rewritten_task = response.content

            # Extract improvements made
            improvements = self._analyze_improvements(original_task, rewritten_task)

            print(colorama.Fore.GREEN + "✓ Task rewritten successfully!\n" + colorama.Style.RESET_ALL)

            return {
                "original": original_task,
                "rewritten": rewritten_task,
                "improvements": improvements,
                "project_type": project_type
            }

        except Exception as e:
            print(colorama.Fore.RED + f"✗ Error rewriting task: {e}\n" + colorama.Style.RESET_ALL)
            # Return original task if rewriting fails
            return {
                "original": original_task,
                "rewritten": original_task,
                "improvements": [],
                "project_type": project_type,
                "error": str(e)
            }

    def _analyze_improvements(self, original: str, rewritten: str) -> list:
        """
        Analyze what improvements were made during rewriting

        Args:
            original: Original task description
            rewritten: Rewritten task description

        Returns:
            List of improvements made
        """
        improvements = []

        # Check length increase (more detail)
        if len(rewritten) > len(original) * 1.2:
            improvements.append("Added more detailed specifications")

        # Check for structure (sections)
        if "#" in rewritten and "#" not in original:
            improvements.append("Added structured sections")

        # Check for requirements list
        if rewritten.count("-") > original.count("-"):
            improvements.append("Broke down requirements into clear list")

        # Check for technical specs
        if "technical" in rewritten.lower() and "technical" not in original.lower():
            improvements.append("Added technical specifications")

        # Check for success criteria
        if "success" in rewritten.lower() or "complete" in rewritten.lower():
            improvements.append("Added success criteria")

        return improvements if improvements else ["Clarified and structured the task"]

    def rewrite_with_context(
        self,
        original_task: str,
        agents_selected: list = None,
        tech_stack: list = None
    ) -> Dict:
        """
        Rewrite task with additional context about agents and tech stack

        Args:
            original_task: Original task description
            agents_selected: List of agent types that will work on this
            tech_stack: Technologies to use (e.g., ["FastAPI", "PostgreSQL"])

        Returns:
            Dict with rewritten task and metadata
        """
        context_parts = []

        if agents_selected:
            agent_roles = ", ".join(agents_selected)
            context_parts.append(f"Agents available: {agent_roles}")

        if tech_stack:
            tech_list = ", ".join(tech_stack)
            context_parts.append(f"Technology stack: {tech_list}")

        context = "\n".join(context_parts) if context_parts else ""

        system_prompt = f"""You are a technical project requirements analyst.

Rewrite the user's task to be clearer and more detailed while preserving meaning.

{context}

Make sure the rewritten task is appropriate for the available agents and tech stack.

Format as:
# Project Goal
[Clear description]

# Core Requirements
- [Requirement 1]
- [etc.]

# Technical Specifications
{f"- Use {tech_stack[0] if tech_stack else 'appropriate technology'}" if tech_stack else ""}
- [Other specs]

# Agent Responsibilities
{self._generate_agent_responsibilities(agents_selected) if agents_selected else ""}

# Success Criteria
- [Criteria]
"""

        user_prompt = f"""Original task: "{original_task}"

Rewrite this to be clearer while preserving the original intent."""

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ]

        try:
            response = self.llm.invoke(messages)
            rewritten_task = response.content

            return {
                "original": original_task,
                "rewritten": rewritten_task,
                "agents": agents_selected,
                "tech_stack": tech_stack,
                "improvements": self._analyze_improvements(original_task, rewritten_task)
            }

        except Exception as e:
            return {
                "original": original_task,
                "rewritten": original_task,
                "agents": agents_selected,
                "tech_stack": tech_stack,
                "error": str(e)
            }

    def _generate_agent_responsibilities(self, agents: list) -> str:
        """Generate agent-specific responsibilities based on agent types"""
        if not agents:
            return ""

        responsibilities = {
            "product_manager": "- Define requirements and user stories",
            "backend_developer": "- Implement server-side logic and APIs",
            "frontend_developer": "- Build user interface and interactions",
            "qa_tester": "- Create comprehensive tests and verify quality",
            "devops": "- Set up deployment and infrastructure",
            "designer": "- Create UI/UX designs and assets",
            "security": "- Review security and implement best practices",
            "tech_writer": "- Write documentation and guides",
            "ceo": "- Oversee project and make strategic decisions",
            "data_scientist": "- Handle data analysis and ML components"
        }

        agent_tasks = []
        for agent in agents:
            if agent in responsibilities:
                agent_tasks.append(responsibilities[agent])

        return "\n".join(agent_tasks) if agent_tasks else ""

    def compare_tasks(self, original: str, rewritten: str):
        """
        Display a comparison of original vs rewritten task

        Args:
            original: Original task
            rewritten: Rewritten task
        """
        print(colorama.Fore.YELLOW + "=" * 80)
        print("TASK COMPARISON")
        print("=" * 80 + colorama.Style.RESET_ALL)

        print(colorama.Fore.CYAN + "\n📝 ORIGINAL TASK:" + colorama.Style.RESET_ALL)
        print(f"{original}\n")

        print(colorama.Fore.GREEN + "✨ REWRITTEN TASK:" + colorama.Style.RESET_ALL)
        print(f"{rewritten}\n")

        print(colorama.Fore.YELLOW + "=" * 80 + colorama.Style.RESET_ALL)


# Example usage and integration functions

def rewrite_task_for_agents(
    task: str,
    agents: list = None,
    model: str = "llama3.2"
) -> str:
    """
    Helper function to rewrite a task and return just the rewritten version

    Args:
        task: Original task description
        agents: Optional list of agent types
        model: LLM model to use

    Returns:
        Rewritten task string
    """
    rewriter = TaskRewriter(model_name=model, temperature=0.3)

    if agents:
        result = rewriter.rewrite_with_context(task, agents_selected=agents)
    else:
        result = rewriter.rewrite_task(task)

    # Show comparison
    rewriter.compare_tasks(result["original"], result["rewritten"])

    return result["rewritten"]


def interactive_task_rewrite():
    """
    Interactive mode for rewriting tasks
    """
    print(colorama.Fore.MAGENTA + """
╔═══════════════════════════════════════════════════════════════════════╗
║                    TASK REWRITER                                      ║
║                                                                       ║
║  Enter your project idea and get a clear, detailed task description ║
╚═══════════════════════════════════════════════════════════════════════╝
    """ + colorama.Style.RESET_ALL)

    # Get task from user
    print(colorama.Fore.CYAN + "Enter your project/task description:" + colorama.Style.RESET_ALL)
    task = input("> ")

    if not task.strip():
        print(colorama.Fore.RED + "Error: Task cannot be empty" + colorama.Style.RESET_ALL)
        return

    # Get project type
    print(colorama.Fore.CYAN + "\nProject type (web_app/api/cli/library/general) [general]:" + colorama.Style.RESET_ALL)
    project_type = input("> ").strip() or "general"

    # Rewrite task
    rewriter = TaskRewriter(model_name="llama3.2", temperature=0.3)
    result = rewriter.rewrite_task(task, project_type)

    # Show comparison
    rewriter.compare_tasks(result["original"], result["rewritten"])

    # Show improvements
    if result.get("improvements"):
        print(colorama.Fore.CYAN + "\n💡 Improvements made:" + colorama.Style.RESET_ALL)
        for improvement in result["improvements"]:
            print(f"   • {improvement}")

    # Ask if user wants to use it
    print(colorama.Fore.YELLOW + "\n📋 Use this rewritten task? (y/n):" + colorama.Style.RESET_ALL)
    use_it = input("> ").strip().lower()

    if use_it == 'y':
        print(colorama.Fore.GREEN + "\n✓ Great! You can now use this task with the agents.\n" + colorama.Style.RESET_ALL)
        return result["rewritten"]
    else:
        print(colorama.Fore.YELLOW + "\n📝 Keeping original task.\n" + colorama.Style.RESET_ALL)
        return result["original"]


if __name__ == "__main__":
    # Example 1: Simple rewrite
    print(colorama.Fore.CYAN + "\n=== EXAMPLE 1: Simple Task Rewrite ===" + colorama.Style.RESET_ALL)

    original = "Create a todo app"
    rewritten = rewrite_task_for_agents(original)

    # Example 2: Rewrite with context
    print(colorama.Fore.CYAN + "\n\n=== EXAMPLE 2: Rewrite with Agent Context ===" + colorama.Style.RESET_ALL)

    original2 = "Build a REST API for user management"
    agents = ["backend_developer", "qa_tester", "security"]

    rewriter = TaskRewriter()
    result = rewriter.rewrite_with_context(
        original2,
        agents_selected=agents,
        tech_stack=["FastAPI", "PostgreSQL", "JWT"]
    )
    rewriter.compare_tasks(result["original"], result["rewritten"])

    # Example 3: Interactive mode
    print(colorama.Fore.CYAN + "\n\n=== EXAMPLE 3: Interactive Mode ===" + colorama.Style.RESET_ALL)
    print("(Uncomment to try interactive mode)")
    # interactive_task_rewrite()
