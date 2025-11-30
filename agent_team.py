"""
Agent Team Manager
Coordinates multiple specialized agents working together on a project
"""

from typing import List, Dict, Optional
from langchain_core.messages import HumanMessage
import colorama
from specialized_agent import SpecializedAgent, create_agent


class AgentTeam:
    """
    Manages a team of specialized agents working on a project

    The team can work in different modes:
    - Sequential: Agents work one after another
    - Collaborative: Agents discuss and iterate together
    - Hierarchical: CEO/Manager directs other agents
    """

    def __init__(self, team_config: Dict[str, str]):
        """
        Initialize an agent team

        Args:
            team_config: Dict mapping agent names to agent types
                        e.g., {"Alice": "ceo", "Bob": "lead_developer"}
        """
        self.agents: Dict[str, SpecializedAgent] = {}
        self.conversation_history: List[Dict] = []

        # Create all agents
        for name, agent_type in team_config.items():
            self.agents[name] = create_agent(agent_type, name)

        colorama.init(autoreset=True)

    def get_agent(self, name: str) -> SpecializedAgent:
        """Get an agent by name"""
        if name not in self.agents:
            raise ValueError(f"Agent {name} not found. Available: {list(self.agents.keys())}")
        return self.agents[name]

    def reset_all(self):
        """Reset all agents' conversation histories"""
        for agent in self.agents.values():
            agent.reset()
        self.conversation_history = []

    def sequential_workflow(
        self,
        task: str,
        agent_order: List[str],
        max_iterations: int = 1
    ) -> List[Dict]:
        """
        Run a sequential workflow where agents work one after another

        Args:
            task: The task/project description
            agent_order: List of agent names in execution order
            max_iterations: How many times to go through the sequence

        Returns:
            List of all agent responses
        """
        results = []

        print(colorama.Fore.MAGENTA + f"\n{'='*80}")
        print(f"SEQUENTIAL WORKFLOW: {task}")
        print(f"{'='*80}\n" + colorama.Style.RESET_ALL)

        for iteration in range(max_iterations):
            print(colorama.Fore.CYAN + f"\n--- Iteration {iteration + 1} ---\n" + colorama.Style.RESET_ALL)

            current_context = task
            for agent_name in agent_order:
                agent = self.get_agent(agent_name)

                # Create message with context from previous agent
                message = HumanMessage(content=current_context)

                print(colorama.Fore.YELLOW + f"\n>>> {agent.name} ({agent.role}) is working...\n" + colorama.Style.RESET_ALL)

                # Get agent response
                response = agent.step(message)

                # Store result
                result = {
                    "iteration": iteration + 1,
                    "agent": agent_name,
                    "role": agent.role,
                    "response": response.content
                }
                results.append(result)
                self.conversation_history.append(result)

                # Print response
                print(colorama.Fore.GREEN + f"{agent.name} ({agent.role}):\n")
                print(f"{response.content}\n" + colorama.Style.RESET_ALL)

                # Update context for next agent
                current_context = f"Previous work by {agent.name}:\n{response.content}\n\nContinue working on: {task}"

        return results

    def collaborative_workflow(
        self,
        task: str,
        agents: List[str],
        max_rounds: int = 5,
        convergence_check: bool = True
    ) -> List[Dict]:
        """
        Run a collaborative workflow where agents discuss together

        Args:
            task: The task/project description
            agents: List of agent names to participate
            max_rounds: Maximum discussion rounds
            convergence_check: Stop if agents reach agreement

        Returns:
            List of all agent responses
        """
        results = []

        print(colorama.Fore.MAGENTA + f"\n{'='*80}")
        print(f"COLLABORATIVE WORKFLOW: {task}")
        print(f"Team: {', '.join(agents)}")
        print(f"{'='*80}\n" + colorama.Style.RESET_ALL)

        # Initial context
        current_context = task

        for round_num in range(max_rounds):
            print(colorama.Fore.CYAN + f"\n--- Round {round_num + 1} ---\n" + colorama.Style.RESET_ALL)

            round_responses = []

            for agent_name in agents:
                agent = self.get_agent(agent_name)

                # Create message with current context
                message = HumanMessage(content=current_context)

                print(colorama.Fore.YELLOW + f"\n>>> {agent.name} ({agent.role}) is contributing...\n" + colorama.Style.RESET_ALL)

                # Get agent response
                response = agent.step(message)

                # Store result
                result = {
                    "round": round_num + 1,
                    "agent": agent_name,
                    "role": agent.role,
                    "response": response.content
                }
                results.append(result)
                round_responses.append(response.content)
                self.conversation_history.append(result)

                # Print response
                print(colorama.Fore.GREEN + f"{agent.name} ({agent.role}):\n")
                print(f"{response.content}\n" + colorama.Style.RESET_ALL)

            # Update context with all responses
            context_parts = [f"\n--- {task} ---\n"]
            for i, (agent_name, response) in enumerate(zip(agents, round_responses)):
                agent = self.get_agent(agent_name)
                context_parts.append(f"\n{agent.name} ({agent.role}) said:\n{response}\n")

            context_parts.append("\nBased on the discussion above, provide your next input:")
            current_context = "\n".join(context_parts)

            # Check for convergence
            if convergence_check and round_num > 0:
                if self._check_convergence(round_responses):
                    print(colorama.Fore.MAGENTA + "\n✓ Team has reached consensus!\n" + colorama.Style.RESET_ALL)
                    break

        return results

    def hierarchical_workflow(
        self,
        task: str,
        manager: str,
        team: List[str],
        max_iterations: int = 3
    ) -> List[Dict]:
        """
        Run a hierarchical workflow where manager directs the team

        Args:
            task: The task/project description
            manager: Name of the manager agent (CEO, Product Manager, etc.)
            team: List of team member agent names
            max_iterations: Number of management cycles

        Returns:
            List of all agent responses
        """
        results = []

        print(colorama.Fore.MAGENTA + f"\n{'='*80}")
        print(f"HIERARCHICAL WORKFLOW: {task}")
        print(f"Manager: {manager}")
        print(f"Team: {', '.join(team)}")
        print(f"{'='*80}\n" + colorama.Style.RESET_ALL)

        manager_agent = self.get_agent(manager)

        for iteration in range(max_iterations):
            print(colorama.Fore.CYAN + f"\n--- Iteration {iteration + 1} ---\n" + colorama.Style.RESET_ALL)

            # Manager assigns tasks
            manager_prompt = f"""As the {manager_agent.role}, analyze this project and assign specific tasks to your team:

Project: {task}

Your team consists of:
{self._format_team_info(team)}

Provide:
1. Overall strategy
2. Specific assignments for each team member
3. Success criteria
"""

            print(colorama.Fore.YELLOW + f"\n>>> {manager_agent.name} is planning...\n" + colorama.Style.RESET_ALL)

            manager_response = manager_agent.step(HumanMessage(content=manager_prompt))

            result = {
                "iteration": iteration + 1,
                "agent": manager,
                "role": manager_agent.role,
                "type": "planning",
                "response": manager_response.content
            }
            results.append(result)
            self.conversation_history.append(result)

            print(colorama.Fore.GREEN + f"{manager_agent.name} ({manager_agent.role}):\n")
            print(f"{manager_response.content}\n" + colorama.Style.RESET_ALL)

            # Team members execute
            team_outputs = []
            for agent_name in team:
                agent = self.get_agent(agent_name)

                work_prompt = f"""The {manager_agent.role} has given the following direction:

{manager_response.content}

Based on your role as {agent.role}, work on your assigned portion of the project: {task}

Provide your work output, progress, and any blockers.
"""

                print(colorama.Fore.YELLOW + f"\n>>> {agent.name} is working...\n" + colorama.Style.RESET_ALL)

                work_response = agent.step(HumanMessage(content=work_prompt))

                result = {
                    "iteration": iteration + 1,
                    "agent": agent_name,
                    "role": agent.role,
                    "type": "execution",
                    "response": work_response.content
                }
                results.append(result)
                team_outputs.append((agent_name, work_response.content))
                self.conversation_history.append(result)

                print(colorama.Fore.GREEN + f"{agent.name} ({agent.role}):\n")
                print(f"{work_response.content}\n" + colorama.Style.RESET_ALL)

            # Manager reviews
            review_prompt = f"""Review the work from your team:

{self._format_team_outputs(team_outputs)}

Provide:
1. Feedback on each team member's work
2. Next steps
3. Whether the project is complete or needs more iteration
"""

            print(colorama.Fore.YELLOW + f"\n>>> {manager_agent.name} is reviewing...\n" + colorama.Style.RESET_ALL)

            review_response = manager_agent.step(HumanMessage(content=review_prompt))

            result = {
                "iteration": iteration + 1,
                "agent": manager,
                "role": manager_agent.role,
                "type": "review",
                "response": review_response.content
            }
            results.append(result)
            self.conversation_history.append(result)

            print(colorama.Fore.GREEN + f"{manager_agent.name} ({manager_agent.role}) - Review:\n")
            print(f"{review_response.content}\n" + colorama.Style.RESET_ALL)

        return results

    def _format_team_info(self, team: List[str]) -> str:
        """Format team information for display"""
        lines = []
        for agent_name in team:
            agent = self.get_agent(agent_name)
            lines.append(f"  - {agent.name}: {agent.role} (Expertise: {', '.join(agent.expertise)})")
        return "\n".join(lines)

    def _format_team_outputs(self, outputs: List[tuple]) -> str:
        """Format team outputs for manager review"""
        lines = []
        for agent_name, output in outputs:
            agent = self.get_agent(agent_name)
            lines.append(f"\n{agent.name} ({agent.role}):\n{output}\n{'-'*60}")
        return "\n".join(lines)

    def _check_convergence(self, responses: List[str]) -> bool:
        """
        Simple convergence check
        In a real system, this could use semantic similarity
        """
        # Placeholder: just check if responses mention "complete" or "done"
        completion_keywords = ["complete", "finished", "done", "ready", "approved"]
        return any(keyword in response.lower() for response in responses for keyword in completion_keywords)

    def get_summary(self) -> str:
        """Get a summary of the team's work"""
        summary_lines = [
            f"\nTeam Summary:",
            f"Total agents: {len(self.agents)}",
            f"Total exchanges: {len(self.conversation_history)}",
            f"\nAgents:",
        ]

        for agent in self.agents.values():
            summary_lines.append(f"  - {agent.name}: {agent.role}")

        return "\n".join(summary_lines)
