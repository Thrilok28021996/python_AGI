"""
Project Coordination System
Like a real Product Manager/Project Manager coordinating the team
- Delegates tasks to appropriate agents
- Tracks progress and blockers
- Facilitates communication between agents
- Resolves conflicts and prioritizes work
"""

from typing import List, Dict, Optional
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_ollama import ChatOllama
import json


class ProjectCoordinator:
    """
    Acts as Project Manager - coordinates all agents
    Like a real PM in a company
    """

    def __init__(self, project_name: str, task: str, model_name: str = "qwen2.5-coder:latest"):
        """Initialize project coordinator"""
        self.project_name = project_name
        self.task = task
        self.model_name = model_name
        self.llm = ChatOllama(model=model_name, temperature=0.3)

        # Track project state
        self.iteration_history = []
        self.current_iteration = 0
        self.blockers = []
        self.knowledge_base = {}  # Shared knowledge between agents
        self.task_assignments = []

    def plan_iteration(self, team: List, current_files: List[str],
                       previous_results: Optional[Dict] = None) -> Dict:
        """
        Plan the next iteration
        - Decide what each agent should work on
        - Identify dependencies
        - Set priorities

        Returns:
            {
                "iteration_plan": {
                    "agent_name": {"task": "...", "priority": "high/medium/low", "dependencies": []},
                    ...
                },
                "goals": ["goal1", "goal2"],
                "risks": ["risk1", "risk2"]
            }
        """

        self.current_iteration += 1

        print(f"\n🎯 Project Manager Planning Iteration {self.current_iteration}...")

        # Build context for planning
        context = self._build_planning_context(team, current_files, previous_results)

        # Try LLM-based planning
        try:
            plan = self._llm_based_planning(context, team)
        except Exception as e:
            print(f"  ⚠️ LLM planning failed, using rule-based planning")
            plan = self._rule_based_planning(team, current_files, previous_results)

        # Store in history
        self.iteration_history.append({
            "iteration": self.current_iteration,
            "plan": plan,
            "timestamp": self._get_timestamp()
        })

        # Display plan
        self._display_iteration_plan(plan)

        return plan

    def _build_planning_context(self, team: List, current_files: List[str],
                                 previous_results: Optional[Dict]) -> str:
        """Build context for iteration planning"""

        context = f"""PROJECT: {self.project_name}
GOAL: {self.task}

CURRENT TEAM ({len(team)} agents):
"""
        for agent in team:
            role = agent.role if hasattr(agent, 'role') else 'Unknown'
            name = agent.name if hasattr(agent, 'name') else 'Unknown'
            context += f"  - {name} ({role})\n"

        context += f"\nCURRENT FILES ({len(current_files)}):\n"
        for file in current_files[:10]:  # Show first 10
            context += f"  - {file}\n"
        if len(current_files) > 10:
            context += f"  ... and {len(current_files) - 10} more\n"

        if previous_results:
            test_status = previous_results.get('final_test_results', {})
            if test_status:
                context += f"\nPREVIOUS ITERATION RESULTS:\n"
                if test_status.get('success'):
                    context += f"  ✓ Tests: {test_status.get('passed', 0)}/{test_status.get('total_tests', 0)} passing\n"
                else:
                    context += f"  ✗ Tests: {test_status.get('failed', 0)} failing\n"

        if self.blockers:
            context += f"\nCURRENT BLOCKERS:\n"
            for blocker in self.blockers:
                context += f"  • {blocker}\n"

        return context

    def _llm_based_planning(self, context: str, team: List) -> Dict:
        """Use LLM to create iteration plan"""

        prompt = f"""{context}

As the Project Manager, plan the next iteration. For each team member, assign specific tasks.

Provide your plan in this JSON format:
{{
    "iteration_plan": {{
        "Agent Name": {{
            "task": "Specific task description",
            "priority": "high/medium/low",
            "dependencies": ["Other agent names this depends on"],
            "estimated_complexity": "simple/medium/complex"
        }}
    }},
    "goals": ["Main goal 1", "Main goal 2"],
    "success_factors": ["Key success factor 1", "Key success factor 2"]
}}

IMPORTANT:
- Be specific and actionable about what each agent should do
- Identify dependencies (e.g., Frontend depends on Backend API)
- Set realistic priorities based on current project state
- Focus on success factors and what needs to happen, not potential problems
- Be decisive and execution-focused
"""

        response = self.llm.invoke([HumanMessage(content=prompt)])

        # Try to parse JSON response
        try:
            # Extract JSON from response
            response_text = response.content
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                plan = json.loads(json_match.group())
                return plan
        except:
            pass

        # Fallback to rule-based
        return self._rule_based_planning(team, [], None)

    def _rule_based_planning(self, team: List, current_files: List[str],
                             previous_results: Optional[Dict]) -> Dict:
        """Rule-based iteration planning when LLM unavailable"""

        plan = {
            "iteration_plan": {},
            "goals": [],
            "risks": []
        }

        # Determine iteration goals based on what's been done
        if not current_files or len(current_files) == 0:
            # First iteration: create initial implementation
            plan["goals"] = ["Create initial project structure", "Implement core functionality"]

            for agent in team:
                agent_name = agent.name if hasattr(agent, 'name') else 'Unknown'
                agent_role = agent.role if hasattr(agent, 'role') else 'Unknown'

                if 'backend' in agent_role.lower():
                    plan["iteration_plan"][agent_name] = {
                        "task": "Create backend API structure and core endpoints",
                        "priority": "high",
                        "dependencies": [],
                        "estimated_complexity": "medium"
                    }
                elif 'frontend' in agent_role.lower():
                    plan["iteration_plan"][agent_name] = {
                        "task": "Create frontend components and UI structure",
                        "priority": "high",
                        "dependencies": ["Backend Developer"],
                        "estimated_complexity": "medium"
                    }
                elif 'qa' in agent_role.lower() or 'tester' in agent_role.lower():
                    plan["iteration_plan"][agent_name] = {
                        "task": "Create comprehensive test suite",
                        "priority": "high",
                        "dependencies": [],
                        "estimated_complexity": "medium"
                    }
                elif 'lead' in agent_role.lower():
                    plan["iteration_plan"][agent_name] = {
                        "task": "Design system architecture and code structure",
                        "priority": "high",
                        "dependencies": [],
                        "estimated_complexity": "simple"
                    }
                else:
                    plan["iteration_plan"][agent_name] = {
                        "task": f"Implement {agent_role.lower()} specific features",
                        "priority": "medium",
                        "dependencies": [],
                        "estimated_complexity": "medium"
                    }

        else:
            # Later iterations: improve and refine
            plan["goals"] = ["Fix issues", "Improve code quality", "Add missing features"]

            # Check if tests are failing
            has_test_failures = False
            if previous_results and previous_results.get('final_test_results'):
                test_results = previous_results['final_test_results']
                has_test_failures = not test_results.get('success', True)

            for agent in team:
                agent_name = agent.name if hasattr(agent, 'name') else 'Unknown'
                agent_role = agent.role if hasattr(agent, 'role') else 'Unknown'

                if has_test_failures and 'developer' in agent_role.lower():
                    plan["iteration_plan"][agent_name] = {
                        "task": "Fix failing tests and bugs",
                        "priority": "high",
                        "dependencies": ["QA Tester"],
                        "estimated_complexity": "medium"
                    }
                elif 'security' in agent_role.lower():
                    plan["iteration_plan"][agent_name] = {
                        "task": "Review code for security vulnerabilities",
                        "priority": "high",
                        "dependencies": [],
                        "estimated_complexity": "simple"
                    }
                else:
                    plan["iteration_plan"][agent_name] = {
                        "task": "Review and improve code quality",
                        "priority": "medium",
                        "dependencies": [],
                        "estimated_complexity": "simple"
                    }

        # Add success factors instead of risks
        plan["success_factors"] = [
            "Clear task assignments enable parallel work",
            "Test-driven development ensures quality",
            "Code review catches issues early"
        ]

        return plan

    def _display_iteration_plan(self, plan: Dict):
        """Display iteration plan in readable format"""

        print(f"\n📋 Iteration Plan:")

        if plan.get('goals'):
            print(f"\n🎯 Goals:")
            for goal in plan['goals']:
                print(f"  • {goal}")

        if plan.get('iteration_plan'):
            print(f"\n👥 Task Assignments:")
            for agent_name, assignment in plan['iteration_plan'].items():
                priority = assignment.get('priority', 'medium')
                priority_icon = "🔴" if priority == "high" else "🟡" if priority == "medium" else "🟢"

                print(f"\n  {priority_icon} {agent_name}:")
                print(f"     Task: {assignment.get('task', 'Not specified')}")
                print(f"     Priority: {priority}")

                deps = assignment.get('dependencies', [])
                if deps:
                    print(f"     Depends on: {', '.join(deps)}")

        if plan.get('success_factors'):
            print(f"\n✅ Success Factors:")
            for factor in plan['success_factors'][:3]:  # Show top 3
                print(f"  • {factor}")

    def record_blocker(self, agent_name: str, blocker_description: str):
        """Record a blocker encountered by an agent"""

        self.blockers.append({
            "agent": agent_name,
            "blocker": blocker_description,
            "iteration": self.current_iteration,
            "timestamp": self._get_timestamp()
        })

        print(f"\n🚧 BLOCKER recorded for {agent_name}: {blocker_description}")

    def resolve_blocker(self, blocker_index: int, resolution: str):
        """Mark blocker as resolved"""

        if 0 <= blocker_index < len(self.blockers):
            self.blockers[blocker_index]['resolved'] = True
            self.blockers[blocker_index]['resolution'] = resolution
            print(f"\n✅ BLOCKER resolved: {resolution}")

    def facilitate_communication(self, from_agent: str, to_agent: str, message: str):
        """
        Facilitate communication between agents
        Like Slack/Teams messages in a real company
        """

        communication = {
            "from": from_agent,
            "to": to_agent,
            "message": message,
            "iteration": self.current_iteration,
            "timestamp": self._get_timestamp()
        }

        if 'communications' not in self.knowledge_base:
            self.knowledge_base['communications'] = []

        self.knowledge_base['communications'].append(communication)

        print(f"\n💬 {from_agent} → {to_agent}: {message}")

    def generate_progress_report(self) -> Dict:
        """
        Generate project progress report
        Like a daily/weekly standup report
        """

        report = {
            "project": self.project_name,
            "current_iteration": self.current_iteration,
            "total_iterations": len(self.iteration_history),
            "active_blockers": [b for b in self.blockers if not b.get('resolved', False)],
            "resolved_blockers": [b for b in self.blockers if b.get('resolved', False)],
            "knowledge_items": len(self.knowledge_base),
            "timestamp": self._get_timestamp()
        }

        return report

    def conduct_retrospective(self, final_results: Dict) -> Dict:
        """
        Conduct iteration retrospective
        - What went well
        - What didn't go well
        - What to improve
        """

        print(f"\n🔄 Project Manager Conducting Retrospective...")

        retrospective = {
            "iteration": self.current_iteration,
            "went_well": [],
            "went_poorly": [],
            "improvements": []
        }

        # Analyze results
        if final_results.get('final_test_results'):
            test_results = final_results['final_test_results']
            if test_results.get('success'):
                retrospective['went_well'].append("All tests passing")
            else:
                retrospective['went_poorly'].append(f"{test_results.get('failed', 0)} tests failing")
                retrospective['improvements'].append("Improve test coverage and fix failing tests")

        # Check for security issues
        if final_results.get('security_scan_results'):
            vulns = final_results['security_scan_results'].get('vulnerabilities', [])
            if len(vulns) == 0:
                retrospective['went_well'].append("No security vulnerabilities found")
            else:
                retrospective['went_poorly'].append(f"{len(vulns)} security issues found")
                retrospective['improvements'].append("Address security vulnerabilities")

        # Check for code reviews
        if final_results.get('review_results'):
            reviews = final_results['review_results']
            improved = sum(1 for r in reviews if r.get('result', {}).get('rounds_completed', 0) > 1)
            if improved > 0:
                retrospective['went_well'].append(f"{improved} files improved through peer review")

        # Check for blockers
        active_blockers = [b for b in self.blockers if not b.get('resolved', False)]
        if active_blockers:
            retrospective['went_poorly'].append(f"{len(active_blockers)} unresolved blockers")
            retrospective['improvements'].append("Resolve blockers faster in next iteration")

        # Display retrospective
        print(f"\n✅ What Went Well:")
        for item in retrospective['went_well']:
            print(f"  • {item}")

        if retrospective['went_poorly']:
            print(f"\n❌ What Didn't Go Well:")
            for item in retrospective['went_poorly']:
                print(f"  • {item}")

        if retrospective['improvements']:
            print(f"\n💡 Improvements for Next Time:")
            for item in retrospective['improvements']:
                print(f"  • {item}")

        return retrospective

    def share_knowledge(self, category: str, key: str, value: any):
        """
        Add to shared knowledge base
        Like team wiki/documentation
        """

        if category not in self.knowledge_base:
            self.knowledge_base[category] = {}

        self.knowledge_base[category][key] = value
        print(f"\n📚 Knowledge added: [{category}] {key}")

    def get_knowledge(self, category: str, key: Optional[str] = None) -> any:
        """Retrieve from knowledge base"""

        if category not in self.knowledge_base:
            return None

        if key is None:
            return self.knowledge_base[category]

        return self.knowledge_base[category].get(key)

    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# Import for JSON parsing
import re


if __name__ == "__main__":
    # Test project coordination

    print("=" * 80)
    print("TESTING PROJECT COORDINATION SYSTEM")
    print("=" * 80)

    # Create mock team
    class MockAgent:
        def __init__(self, name, role):
            self.name = name
            self.role = role

    team = [
        MockAgent("Alice", "Lead Developer"),
        MockAgent("Bob", "Backend Developer"),
        MockAgent("Charlie", "Frontend Developer"),
        MockAgent("Diana", "QA Tester")
    ]

    # Create coordinator
    coordinator = ProjectCoordinator(
        project_name="test_project",
        task="Build a web application"
    )

    # Test iteration planning
    print("\n\n🧪 TEST 1: Iteration Planning")
    print("-" * 80)

    plan = coordinator.plan_iteration(
        team=team,
        current_files=[],
        previous_results=None
    )

    # Test blocker recording
    print("\n\n🧪 TEST 2: Blocker Recording")
    print("-" * 80)

    coordinator.record_blocker("Bob", "Waiting for API design from Alice")
    coordinator.record_blocker("Charlie", "Need backend endpoints before implementing UI")

    # Test knowledge sharing
    print("\n\n🧪 TEST 3: Knowledge Sharing")
    print("-" * 80)

    coordinator.share_knowledge("api_design", "user_endpoint", "/api/users")
    coordinator.share_knowledge("api_design", "auth_endpoint", "/api/auth")

    # Test progress report
    print("\n\n🧪 TEST 4: Progress Report")
    print("-" * 80)

    report = coordinator.generate_progress_report()
    print(f"\nProgress Report:")
    print(f"  Iteration: {report['current_iteration']}")
    print(f"  Active Blockers: {len(report['active_blockers'])}")
    print(f"  Knowledge Items: {report['knowledge_items']}")

    print("\n" + "=" * 80)
    print("✅ Project coordination system working!")
    print("=" * 80)
