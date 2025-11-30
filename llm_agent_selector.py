"""
LLM-Powered Agent Selector
Uses an Ollama model to intelligently decide which agents are needed for a task
"""

from typing import List, Dict
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage
import json
import re
from agent_team import AgentTeam
import colorama

colorama.init(autoreset=True)


class LLMAgentSelector:
    """
    Uses an LLM to analyze tasks and select the most appropriate agents
    Much more intelligent than keyword matching!
    """

    # Available agent types with descriptions
    AVAILABLE_AGENTS = {
        "ceo": "Strategic planning, decision making, and leadership. Approves major decisions and sets direction.",
        "product_manager": "Defines product requirements, creates user stories, prioritizes features, manages product roadmap.",
        "lead_developer": "Designs system architecture, makes technical decisions, reviews code, provides technical leadership.",
        "backend_developer": "Implements server-side logic, builds APIs, manages databases, writes backend code (Python, Node, etc).",
        "frontend_developer": "Builds user interfaces, implements React/Vue/Angular apps, handles client-side logic and styling.",
        "qa_tester": "Creates test cases, performs testing (unit, integration, e2e), finds bugs, ensures quality.",
        "devops": "Sets up CI/CD pipelines, manages infrastructure, handles deployments, cloud services (AWS, Docker, K8s).",
        "designer": "Creates UI/UX designs, wireframes, mockups, prototypes, ensures good user experience.",
        "security": "Security audits, implements authentication/authorization, reviews for vulnerabilities, ensures compliance.",
        "tech_writer": "Writes documentation, API docs, user guides, README files, technical explanations."
    }

    def __init__(self, model_name: str = "mistral:latest"):
        """
        Initialize the LLM-based selector

        Args:
            model_name: Which Ollama model to use for selection
                       Recommended: mistral (good reasoning), deepseek-r1 (deep analysis)
        """
        self.model = ChatOllama(model=model_name, temperature=0.3)  # Low temp for consistent decisions
        self.model_name = model_name

    def select_agents(self, task: str, min_agents: int = 2, max_agents: int = 10, verbose: bool = True) -> Dict:
        """
        Use LLM to select the best agents for a task

        Args:
            task: Task description
            min_agents: Minimum number of agents to select
            max_agents: Maximum number of agents to select
            verbose: Print analysis details

        Returns:
            Dict with selected agents, reasoning, and workflow suggestion
        """
        if verbose:
            print(colorama.Fore.CYAN + f"\n🤖 Using {self.model_name} to analyze task and select agents...\n" + colorama.Style.RESET_ALL)

        # Create prompt for LLM
        prompt = self._create_selection_prompt(task, min_agents, max_agents)

        # Get LLM response
        try:
            response = self.model.invoke([
                SystemMessage(content="You are an expert at analyzing software development tasks and selecting the right team members."),
                HumanMessage(content=prompt)
            ])

            # Parse response
            selection = self._parse_llm_response(response.content, verbose)

            if verbose:
                print(colorama.Fore.GREEN + "\n✅ Agent selection complete!\n" + colorama.Style.RESET_ALL)

            return selection

        except Exception as e:
            if verbose:
                print(colorama.Fore.RED + f"\n❌ LLM selection failed: {e}" + colorama.Style.RESET_ALL)
                print(colorama.Fore.YELLOW + "Falling back to default team...\n" + colorama.Style.RESET_ALL)

            # Fallback to default
            return {
                "agents": ["product_manager", "backend_developer", "qa_tester"],
                "reasoning": "Fallback: Default development team",
                "workflow": "sequential",
                "priorities": []
            }

    def _create_selection_prompt(self, task: str, min_agents: int, max_agents: int) -> str:
        """Create the prompt for the LLM"""

        # Format available agents
        agents_list = "\n".join([
            f"- **{agent}**: {description}"
            for agent, description in self.AVAILABLE_AGENTS.items()
        ])

        prompt = f"""Analyze this task and select the most appropriate team of AI agents to complete it:

**TASK:**
{task}

**AVAILABLE AGENTS:**
{agents_list}

**REQUIREMENTS:**
1. Select between {min_agents} and {max_agents} agents
2. Only select agents that are truly needed for this specific task
3. Consider the natural workflow order (e.g., Product Manager before Developers, Developers before QA)
4. Think about what specialists are required

**RESPOND IN THIS EXACT FORMAT:**

SELECTED AGENTS:
[List agent names, one per line, in workflow order]

REASONING:
[Explain why each agent is needed]

WORKFLOW:
[Choose: sequential, collaborative, or hierarchical]

PRIORITIES:
[Which agents are most critical vs nice-to-have]

**EXAMPLE RESPONSE FORMAT:**

SELECTED AGENTS:
product_manager
backend_developer
frontend_developer
qa_tester

REASONING:
- product_manager: Needed to define requirements and user stories
- backend_developer: Required to build the API and database
- frontend_developer: Necessary for the user interface
- qa_tester: Essential to ensure quality

WORKFLOW:
sequential

PRIORITIES:
Critical: product_manager, backend_developer
Nice-to-have: qa_tester

---

Now analyze the task and respond:
"""
        return prompt

    def _parse_llm_response(self, response: str, verbose: bool = True) -> Dict:
        """Parse the LLM's response and extract agent selections"""

        # Extract sections
        agents = []
        reasoning = ""
        workflow = "sequential"
        priorities = []

        lines = response.split('\n')
        current_section = None

        for line in lines:
            line_stripped = line.strip()

            # Detect sections
            if "SELECTED AGENTS:" in line_stripped:
                current_section = "agents"
                continue
            elif "REASONING:" in line_stripped:
                current_section = "reasoning"
                continue
            elif "WORKFLOW:" in line_stripped:
                current_section = "workflow"
                continue
            elif "PRIORITIES:" in line_stripped:
                current_section = "priorities"
                continue

            # Parse content
            if current_section == "agents" and line_stripped:
                # Extract agent name (handle bullets, numbers, etc.)
                agent = line_stripped.lower()
                agent = re.sub(r'^[-•*\d.)\s]+', '', agent)  # Remove bullets/numbers
                agent = agent.strip()

                # Validate it's a real agent
                if agent in self.AVAILABLE_AGENTS:
                    if agent not in agents:  # Avoid duplicates
                        agents.append(agent)

            elif current_section == "reasoning" and line_stripped:
                reasoning += line_stripped + "\n"

            elif current_section == "workflow" and line_stripped:
                # Extract workflow type
                workflow_lower = line_stripped.lower()
                if "sequential" in workflow_lower:
                    workflow = "sequential"
                elif "collaborative" in workflow_lower:
                    workflow = "collaborative"
                elif "hierarchical" in workflow_lower:
                    workflow = "hierarchical"

            elif current_section == "priorities" and line_stripped:
                priorities.append(line_stripped)

        # Fallback if parsing failed
        if not agents:
            if verbose:
                print(colorama.Fore.YELLOW + "⚠️  Could not parse agents from LLM response. Using defaults." + colorama.Style.RESET_ALL)
            agents = ["product_manager", "backend_developer", "qa_tester"]

        if verbose:
            print(colorama.Fore.YELLOW + f"\n📋 LLM ANALYSIS:\n" + colorama.Style.RESET_ALL)
            print(f"Selected {len(agents)} agents: {', '.join(agents)}")
            print(f"Workflow: {workflow}")
            if reasoning:
                print(f"\nReasoning:\n{reasoning}")

        return {
            "agents": agents,
            "reasoning": reasoning.strip(),
            "workflow": workflow,
            "priorities": priorities,
            "raw_response": response
        }

    def auto_execute(
        self,
        task: str,
        min_agents: int = 2,
        max_agents: int = 10,
        max_iterations: int = 1,
        max_rounds: int = 3,
        verbose: bool = True
    ) -> Dict:
        """
        Full auto-execution: LLM selects agents, then executes the task

        Args:
            task: Task description
            min_agents: Minimum agents to select
            max_agents: Maximum agents to select
            max_iterations: Max iterations for workflows
            max_rounds: Max rounds for collaborative
            verbose: Print details

        Returns:
            Dict with selection, results, and team
        """
        # Select agents using LLM
        selection = self.select_agents(task, min_agents, max_agents, verbose)

        # Create team
        team_config = {
            agent.capitalize(): agent
            for agent in selection['agents']
        }

        team = AgentTeam(team_config)
        agent_names = list(team_config.keys())

        if verbose:
            print(colorama.Fore.GREEN + f"\n🚀 Executing with {selection['workflow']} workflow...\n" + colorama.Style.RESET_ALL)

        # Execute based on selected workflow
        results = None

        if selection['workflow'] == "sequential":
            results = team.sequential_workflow(
                task=task,
                agent_order=agent_names,
                max_iterations=max_iterations
            )

        elif selection['workflow'] == "collaborative":
            results = team.collaborative_workflow(
                task=task,
                agents=agent_names,
                max_rounds=max_rounds
            )

        elif selection['workflow'] == "hierarchical":
            manager = agent_names[0] if selection['agents'][0] in ['ceo', 'product_manager'] else agent_names[0]
            team_members = agent_names[1:] if len(agent_names) > 1 else agent_names

            results = team.hierarchical_workflow(
                task=task,
                manager=manager,
                team=team_members,
                max_iterations=max_iterations
            )

        return {
            "selection": selection,
            "results": results,
            "team": team
        }


# Convenience function
def llm_solve(
    task: str,
    model: str = "mistral:latest",
    min_agents: int = 2,
    max_agents: int = 10,
    max_iterations: int = 1,
    verbose: bool = True
) -> Dict:
    """
    One-line function to solve a task using LLM-based agent selection

    Args:
        task: Task description
        model: Ollama model to use for selection (mistral, deepseek-r1, etc)
        min_agents: Minimum agents
        max_agents: Maximum agents
        max_iterations: Workflow iterations
        verbose: Print progress

    Returns:
        Dict with selection and results

    Example:
        result = llm_solve("Build a REST API for user management")
    """
    selector = LLMAgentSelector(model_name=model)
    return selector.auto_execute(task, min_agents, max_agents, max_iterations, verbose=verbose)


if __name__ == "__main__":
    print(colorama.Fore.MAGENTA + """
╔═══════════════════════════════════════════════════════════════════════╗
║                  LLM-POWERED AGENT SELECTOR                           ║
║                                                                       ║
║  Uses AI to intelligently select the perfect team for your task!     ║
╚═══════════════════════════════════════════════════════════════════════╝
    """ + colorama.Style.RESET_ALL)

    # Example
    example_task = "Build a web application for task management with user authentication, CRUD operations, and deployment to AWS"

    print(colorama.Fore.CYAN + "\nExample Task:" + colorama.Style.RESET_ALL)
    print(example_task)

    result = llm_solve(example_task, model="mistral:latest")

    print(colorama.Fore.GREEN + f"\n\n✅ Task completed!" + colorama.Style.RESET_ALL)
