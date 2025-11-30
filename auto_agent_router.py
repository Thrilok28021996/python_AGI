"""
Intelligent Auto-Agent Router
Automatically assigns the best agents for a task based on task description
"""

from typing import List, Dict, Tuple
import re
from agent_team import AgentTeam
import colorama

colorama.init(autoreset=True)


class TaskRouter:
    """
    Intelligently routes tasks to the most appropriate agents
    Analyzes task description and automatically selects agents and workflow
    """

    # Keywords that indicate which agents are needed
    AGENT_KEYWORDS = {
        "ceo": [
            "strategy", "strategic", "decision", "approve", "budget", "roadmap",
            "vision", "goal", "objective", "leadership", "prioritize", "direction",
            "business", "stakeholder", "executive"
        ],
        "product_manager": [
            "requirements", "features", "user story", "user stories", "specification",
            "product", "backlog", "sprint", "epic", "acceptance criteria", "roadmap",
            "functionality", "scope", "mvp", "release", "planning", "project"
        ],
        "lead_developer": [
            "architecture", "design pattern", "system design", "technical design",
            "scalability", "framework", "technology stack", "tech stack", "structure",
            "microservices", "monolith", "distributed", "technical lead", "technical architecture"
        ],
        "backend_developer": [
            "api", "rest", "graphql", "database", "server", "backend", "endpoint",
            "python", "fastapi", "django", "flask", "node", "sql", "nosql", "postgres",
            "crud", "data", "service", "logic", "processing", "storage", "query",
            "mysql", "mongodb", "redis", "orm", "model", "controller"
        ],
        "frontend_developer": [
            "ui", "frontend", "react", "vue", "angular", "javascript", "typescript",
            "css", "html", "component", "interface", "web page", "website", "responsive",
            "web app", "web application", "spa", "user interface", "client", "browser",
            "dom", "form", "button", "page", "view", "screen"
        ],
        "qa_tester": [
            "test", "testing", "quality", "qa", "bug", "validation", "verify",
            "unit test", "integration test", "test case", "quality assurance",
            "coverage", "assertion", "mock", "e2e", "automated test", "manual test"
        ],
        "devops": [
            "deploy", "deployment", "ci/cd", "docker", "kubernetes", "infrastructure",
            "cloud", "aws", "azure", "gcp", "pipeline", "automation", "monitoring",
            "container", "orchestration", "scaling", "production", "staging", "environment",
            "setup", "configuration", "provisioning"
        ],
        "designer": [
            "design", "ui/ux", "wireframe", "mockup", "prototype", "layout",
            "user experience", "user interface", "visual", "branding", "style",
            "aesthetic", "colors", "theme", "graphics", "usability"
        ],
        "security": [
            "security", "secure", "encryption", "authentication", "authorization",
            "vulnerability", "penetration", "audit", "compliance", "gdpr", "hipaa",
            "auth", "login", "password", "token", "jwt", "oauth", "ssl", "tls",
            "permissions", "access control", "firewall"
        ],
        "tech_writer": [
            "documentation", "docs", "readme", "guide", "tutorial", "manual",
            "api docs", "document", "write", "explain", "instructions",
            "help", "how-to", "reference", "wiki"
        ]
    }

    # Task type patterns
    TASK_PATTERNS = {
        "development": ["build", "create", "develop", "implement", "code", "write"],
        "planning": ["plan", "design", "architect", "strategy", "roadmap"],
        "review": ["review", "audit", "analyze", "assess", "evaluate"],
        "documentation": ["document", "explain", "describe", "guide"],
        "testing": ["test", "verify", "validate", "check"],
        "deployment": ["deploy", "launch", "release", "publish"]
    }

    def __init__(self):
        self.team = None

    def analyze_task(self, task: str) -> Dict:
        """
        Analyze a task and determine which agents are needed

        Returns:
            Dict with suggested agents, workflow type, and confidence scores
        """
        task_lower = task.lower()

        # Score each agent based on keyword matches
        agent_scores = {}
        for agent_type, keywords in self.AGENT_KEYWORDS.items():
            score = sum(1 for keyword in keywords if keyword in task_lower)
            if score > 0:
                agent_scores[agent_type] = score

        # Determine task type
        task_type = self._determine_task_type(task_lower)

        # Suggest workflow based on task type and number of agents
        workflow_type = self._suggest_workflow(task_type, len(agent_scores))

        return {
            "agents": agent_scores,
            "task_type": task_type,
            "workflow": workflow_type,
            "recommended_agents": self._get_recommended_agents(agent_scores, task_type)
        }

    def _determine_task_type(self, task: str) -> str:
        """Determine the type of task"""
        type_scores = {}
        for task_type, keywords in self.TASK_PATTERNS.items():
            score = sum(1 for keyword in keywords if keyword in task)
            if score > 0:
                type_scores[task_type] = score

        if type_scores:
            return max(type_scores.items(), key=lambda x: x[1])[0]
        return "general"

    def _suggest_workflow(self, task_type: str, num_agents: int) -> str:
        """Suggest the best workflow type"""
        # Development tasks work well sequentially
        if task_type == "development" and num_agents >= 3:
            return "sequential"

        # Planning/design benefits from collaboration
        if task_type in ["planning", "review"] and num_agents >= 2:
            return "collaborative"

        # If CEO or PM is involved with team, use hierarchical
        # (will be determined when we know specific agents)
        if num_agents >= 4:
            return "hierarchical"

        # Default to sequential for 2-3 agents
        if num_agents >= 2:
            return "sequential"

        return "single_agent"

    def _get_recommended_agents(self, agent_scores: Dict, task_type: str) -> List[str]:
        """
        Get ordered list of recommended agents based on scores and task type

        Returns agents in optimal execution order
        """
        if not agent_scores:
            # Default team for unknown tasks
            return ["product_manager", "backend_developer", "qa_tester"]

        # Sort by score (descending)
        sorted_agents = sorted(agent_scores.items(), key=lambda x: x[1], reverse=True)
        agents = [agent for agent, score in sorted_agents]

        # Add implied agents for common scenarios
        agents = self._add_implied_agents(agents, task_type, agent_scores)

        # Ensure logical ordering based on development workflow
        ordered_agents = self._order_agents_logically(agents, task_type)

        return ordered_agents

    def _add_implied_agents(self, agents: List[str], task_type: str, agent_scores: Dict) -> List[str]:
        """
        Add agents that are commonly needed but might not have keyword matches

        Args:
            agents: Current list of detected agents
            task_type: Type of task detected
            agent_scores: Scores for all agents

        Returns:
            Enhanced list of agents
        """
        implied = set(agents)

        # For development tasks, always include Product Manager if not present
        if task_type == "development":
            if not any(a in implied for a in ["product_manager", "ceo"]):
                # Add PM if we have multiple developers
                if any(a in implied for a in ["backend_developer", "frontend_developer"]):
                    implied.add("product_manager")

        # If we have backend OR frontend, likely need both for web apps
        if "frontend_developer" in implied and "backend_developer" not in implied:
            # Web app likely needs backend
            if any(keyword in str(agent_scores) for keyword in ["app", "application", "web"]):
                implied.add("backend_developer")

        if "backend_developer" in implied and "frontend_developer" not in implied:
            # If API or server mentioned with web context, might need frontend
            if any(keyword in str(agent_scores) for keyword in ["web", "website", "ui"]):
                implied.add("frontend_developer")

        # Development projects should have QA
        if task_type == "development" and len(implied) >= 2:
            if "qa_tester" not in implied:
                implied.add("qa_tester")

        # If we have a full team (backend + frontend), add Product Manager
        if "backend_developer" in implied and "frontend_developer" in implied:
            if "product_manager" not in implied and "ceo" not in implied:
                implied.add("product_manager")

        # Large teams benefit from technical leadership
        if len(implied) >= 4 and "lead_developer" not in implied:
            if any(a in implied for a in ["backend_developer", "frontend_developer"]):
                implied.add("lead_developer")

        return list(implied)

    def _order_agents_logically(self, agents: List[str], task_type: str) -> List[str]:
        """Order agents in a logical workflow sequence"""

        # Define typical workflow order
        workflow_order = [
            "ceo",
            "product_manager",
            "designer",
            "lead_developer",
            "backend_developer",
            "frontend_developer",
            "devops",
            "qa_tester",
            "security",
            "tech_writer"
        ]

        # Filter and order based on workflow
        ordered = []
        for role in workflow_order:
            if role in agents:
                ordered.append(role)

        # Add any remaining agents not in the standard order
        for agent in agents:
            if agent not in ordered:
                ordered.append(agent)

        return ordered

    def auto_execute(
        self,
        task: str,
        max_iterations: int = 1,
        max_rounds: int = 3,
        verbose: bool = True
    ) -> Dict:
        """
        Automatically analyze task, select agents, and execute

        Args:
            task: The task description
            max_iterations: Max iterations for sequential/hierarchical workflows
            max_rounds: Max rounds for collaborative workflow
            verbose: Print analysis details

        Returns:
            Dict with analysis and results
        """
        if verbose:
            print(colorama.Fore.CYAN + "\n" + "="*80)
            print("🤖 AUTO-AGENT ROUTER - Analyzing Task...")
            print("="*80 + colorama.Style.RESET_ALL)

        # Analyze task
        analysis = self.analyze_task(task)

        if verbose:
            print(colorama.Fore.YELLOW + f"\n📋 TASK TYPE: {analysis['task_type'].upper()}" + colorama.Style.RESET_ALL)
            print(colorama.Fore.YELLOW + f"🔄 WORKFLOW: {analysis['workflow'].upper()}" + colorama.Style.RESET_ALL)
            print(colorama.Fore.YELLOW + f"\n👥 SELECTED AGENTS ({len(analysis['recommended_agents'])}):" + colorama.Style.RESET_ALL)
            for i, agent in enumerate(analysis['recommended_agents'], 1):
                score = analysis['agents'].get(agent, 0)
                print(f"  {i}. {agent:20} (relevance: {'⭐' * min(score, 5)})")

        # Create team with selected agents
        team_config = {
            agent.capitalize(): agent
            for agent in analysis['recommended_agents']
        }

        self.team = AgentTeam(team_config)

        if verbose:
            print(colorama.Fore.GREEN + f"\n✅ Team assembled! Running {analysis['workflow']} workflow...\n" + colorama.Style.RESET_ALL)

        # Execute appropriate workflow
        results = None
        agent_names = list(team_config.keys())

        if analysis['workflow'] == "sequential":
            results = self.team.sequential_workflow(
                task=task,
                agent_order=agent_names,
                max_iterations=max_iterations
            )

        elif analysis['workflow'] == "collaborative":
            results = self.team.collaborative_workflow(
                task=task,
                agents=agent_names,
                max_rounds=max_rounds
            )

        elif analysis['workflow'] == "hierarchical":
            # Use first agent as manager if it's CEO or PM
            manager = agent_names[0] if analysis['recommended_agents'][0] in ['ceo', 'product_manager'] else agent_names[0]
            team_members = agent_names[1:] if len(agent_names) > 1 else agent_names

            results = self.team.hierarchical_workflow(
                task=task,
                manager=manager,
                team=team_members,
                max_iterations=max_iterations
            )

        elif analysis['workflow'] == "single_agent":
            # Just one agent - use sequential with one agent
            results = self.team.sequential_workflow(
                task=task,
                agent_order=agent_names[:1],
                max_iterations=1
            )

        return {
            "analysis": analysis,
            "results": results,
            "team": self.team
        }


# Convenience function for one-line execution
def auto_solve(task: str, max_iterations: int = 1, max_rounds: int = 3, verbose: bool = True) -> Dict:
    """
    One-line function to automatically solve a task with the best agents

    Usage:
        result = auto_solve("Build a REST API for user management")

    Args:
        task: Task description
        max_iterations: Max iterations for sequential/hierarchical workflows
        max_rounds: Max rounds for collaborative workflow
        verbose: Print progress

    Returns:
        Dict with analysis and results
    """
    router = TaskRouter()
    return router.auto_execute(task, max_iterations, max_rounds, verbose)


if __name__ == "__main__":
    # Example usage
    print(colorama.Fore.MAGENTA + """
╔═══════════════════════════════════════════════════════════════════════╗
║                    AUTO-AGENT ROUTER DEMO                             ║
║                                                                       ║
║  Automatically selects the best agents for your task!                ║
╚═══════════════════════════════════════════════════════════════════════╝
    """ + colorama.Style.RESET_ALL)

    # Example task
    example_task = """
    Build a web application for task management with user authentication,
    CRUD operations for tasks, and a responsive UI. Include proper testing
    and deployment setup.
    """

    print(colorama.Fore.CYAN + "\nExample Task:" + colorama.Style.RESET_ALL)
    print(example_task)

    # Auto-solve!
    result = auto_solve(example_task, max_iterations=1)

    print(colorama.Fore.GREEN + f"\n\n✅ Task completed with {len(result['analysis']['recommended_agents'])} agents!" + colorama.Style.RESET_ALL)
