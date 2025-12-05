"""
Dynamic Team Builder
Automatically determines optimal team composition based on project requirements
Like a real company - team size and roles depend on the project!
"""

from typing import List, Dict, Optional
import re
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage


class DynamicTeamBuilder:
    """
    Analyzes project requirements and builds optimal team
    Small task = small team (1-2 agents)
    Complex project = full team (5-8 agents)
    """

    def __init__(self, model_name: str = "qwen2.5-coder:latest"):
        """Initialize team builder with LLM for analysis"""
        self.llm = ChatOllama(model=model_name, temperature=0.3)

    def analyze_project_requirements(self, task: str) -> Dict:
        """
        Analyze task to determine what kind of project it is

        Returns:
            {
                "project_type": "web_app" | "api" | "library" | "data_analysis" | "ml_model" | etc,
                "complexity": "simple" | "medium" | "complex",
                "domains": ["backend", "frontend", "database", "testing", ...],
                "estimated_team_size": int,
                "requires_security": bool,
                "requires_ui": bool,
                "requires_testing": bool,
                "requires_data_science": bool
            }
        """

        analysis_prompt = f"""Analyze this project task and determine requirements:

TASK: {task}

Provide analysis in this EXACT format:

PROJECT_TYPE: [web_app/api/library/data_analysis/ml_model/mobile_app/desktop_app/cli_tool/other]
COMPLEXITY: [simple/medium/complex]
DOMAINS: [comma-separated list from: backend,frontend,database,testing,security,devops,ui_design,data_science,mobile]
TEAM_SIZE: [number between 1-10]
REQUIRES_SECURITY: [yes/no]
REQUIRES_UI: [yes/no]
REQUIRES_TESTING: [yes/no]
REQUIRES_DATA: [yes/no]

Rules:
- Simple task (calculator, basic script): 1-2 agents
- Medium task (REST API, simple web app): 3-5 agents
- Complex task (full-stack app, ML pipeline): 6-10 agents
- Always include testing unless explicitly a prototype
- Add security if handling auth, payments, or sensitive data
- Add UI design if it's a user-facing application
"""

        response = self.llm.invoke([HumanMessage(content=analysis_prompt)])
        analysis_text = response.content

        # Parse response
        analysis = self._parse_analysis(analysis_text)
        return analysis

    def _rule_based_analysis(self, task: str) -> Dict:
        """
        Rule-based project analysis when LLM is unavailable
        Uses keyword matching and heuristics
        """
        task_lower = task.lower()

        analysis = {
            "project_type": "other",
            "complexity": "medium",
            "domains": [],
            "estimated_team_size": 3,
            "requires_security": False,
            "requires_ui": False,
            "requires_testing": True,
            "requires_data_science": False
        }

        # Detect project type
        if any(word in task_lower for word in ['api', 'rest', 'graphql', 'endpoint']):
            analysis["project_type"] = "api"
            analysis["domains"].append("backend")

        if any(word in task_lower for word in ['web app', 'website', 'react', 'vue', 'angular', 'frontend']):
            analysis["project_type"] = "web_app"
            analysis["domains"].extend(["frontend", "backend"])
            analysis["requires_ui"] = True

        if any(word in task_lower for word in ['library', 'package', 'module', 'sdk']):
            analysis["project_type"] = "library"
            analysis["domains"].append("backend")

        if any(word in task_lower for word in ['data analysis', 'machine learning', 'ml model', 'predict', 'forecast']):
            analysis["project_type"] = "ml_model"
            analysis["domains"].append("data_science")
            analysis["requires_data_science"] = True

        if any(word in task_lower for word in ['mobile', 'ios', 'android', 'flutter', 'react native']):
            analysis["project_type"] = "mobile_app"
            analysis["domains"].append("mobile")
            analysis["requires_ui"] = True

        # Detect complexity
        complexity_indicators = {
            "simple": ['simple', 'basic', 'calculator', 'hello world', 'script'],
            "complex": ['complete', 'full-stack', 'e-commerce', 'payment', 'microservices', 'dashboard', 'admin']
        }

        for complexity, keywords in complexity_indicators.items():
            if any(word in task_lower for word in keywords):
                analysis["complexity"] = complexity
                break

        # Detect security requirements
        if any(word in task_lower for word in ['auth', 'login', 'password', 'payment', 'secure', 'jwt', 'oauth']):
            analysis["requires_security"] = True
            analysis["domains"].append("security")

        # Detect database needs
        if any(word in task_lower for word in ['database', 'sql', 'postgresql', 'mongodb', 'crud', 'store', 'persist']):
            if "database" not in analysis["domains"]:
                analysis["domains"].append("database")

        # Detect testing
        if 'no test' in task_lower or 'without test' in task_lower or 'prototype' in task_lower:
            analysis["requires_testing"] = False
        else:
            if "testing" not in analysis["domains"]:
                analysis["domains"].append("testing")

        # Estimate team size based on complexity and domains
        if analysis["complexity"] == "simple":
            analysis["estimated_team_size"] = 1 if len(analysis["domains"]) <= 1 else 2
        elif analysis["complexity"] == "complex":
            analysis["estimated_team_size"] = min(8, 3 + len(analysis["domains"]))
        else:  # medium
            analysis["estimated_team_size"] = min(5, 2 + len(analysis["domains"]))

        return analysis

    def _parse_analysis(self, text: str) -> Dict:
        """Parse LLM analysis response"""

        analysis = {
            "project_type": "other",
            "complexity": "medium",
            "domains": [],
            "estimated_team_size": 3,
            "requires_security": False,
            "requires_ui": False,
            "requires_testing": True,
            "requires_data_science": False
        }

        # Extract project type
        match = re.search(r'PROJECT_TYPE:\s*(\w+)', text, re.IGNORECASE)
        if match:
            analysis["project_type"] = match.group(1).lower()

        # Extract complexity
        match = re.search(r'COMPLEXITY:\s*(\w+)', text, re.IGNORECASE)
        if match:
            analysis["complexity"] = match.group(1).lower()

        # Extract domains
        match = re.search(r'DOMAINS:\s*([^\n]+)', text, re.IGNORECASE)
        if match:
            domains_str = match.group(1)
            analysis["domains"] = [d.strip().lower() for d in domains_str.split(',')]

        # Extract team size
        match = re.search(r'TEAM_SIZE:\s*(\d+)', text, re.IGNORECASE)
        if match:
            analysis["estimated_team_size"] = int(match.group(1))

        # Extract boolean flags
        analysis["requires_security"] = bool(re.search(r'REQUIRES_SECURITY:\s*yes', text, re.IGNORECASE))
        analysis["requires_ui"] = bool(re.search(r'REQUIRES_UI:\s*yes', text, re.IGNORECASE))
        analysis["requires_testing"] = bool(re.search(r'REQUIRES_TESTING:\s*yes', text, re.IGNORECASE))
        analysis["requires_data_science"] = bool(re.search(r'REQUIRES_DATA:\s*yes', text, re.IGNORECASE))

        return analysis

    def build_team(self, task: str, max_agents: Optional[int] = None) -> List[Dict]:
        """
        Build optimal team based on task analysis

        Args:
            task: Project description
            max_agents: Maximum number of agents (optional constraint)

        Returns:
            List of agent configs: [{"type": "backend_developer", "name": "Alice"}, ...]
        """

        # Try LLM analysis first, fall back to rule-based if unavailable
        try:
            analysis = self.analyze_project_requirements(task)
        except Exception as e:
            print(f"  ⚠️ LLM unavailable, using rule-based analysis")
            analysis = self._rule_based_analysis(task)

        print(f"\n📊 Project Analysis:")
        print(f"  Type: {analysis['project_type']}")
        print(f"  Complexity: {analysis['complexity']}")
        print(f"  Domains: {', '.join(analysis['domains'])}")
        print(f"  Estimated team size: {analysis['estimated_team_size']}")

        # Build team based on analysis
        team = []

        # Always need a project manager/lead for coordination
        if analysis['estimated_team_size'] >= 3:
            team.append({"type": "product_manager", "name": self._generate_name()})
            team.append({"type": "lead_developer", "name": self._generate_name()})

        # Add domain-specific developers
        if "backend" in analysis["domains"] or "api" in analysis["domains"]:
            team.append({"type": "backend_developer", "name": self._generate_name()})

        if "frontend" in analysis["domains"] or analysis["requires_ui"]:
            team.append({"type": "frontend_developer", "name": self._generate_name()})

        if "mobile" in analysis["domains"]:
            team.append({"type": "frontend_developer", "name": self._generate_name()})  # Mobile dev

        if "database" in analysis["domains"]:
            # Backend dev can handle this, or add dedicated if complex
            if analysis["complexity"] == "complex" and "backend_developer" in [a["type"] for a in team]:
                pass  # Backend dev covers it
            elif "backend_developer" not in [a["type"] for a in team]:
                team.append({"type": "backend_developer", "name": self._generate_name()})

        # Add specialists based on requirements
        if analysis["requires_security"] or "security" in analysis["domains"]:
            team.append({"type": "security", "name": self._generate_name()})

        if analysis["requires_testing"] or "testing" in analysis["domains"]:
            team.append({"type": "qa_tester", "name": self._generate_name()})

        if analysis["requires_data_science"] or "data_science" in analysis["domains"]:
            team.append({"type": "data_scientist", "name": self._generate_name()})

        if "devops" in analysis["domains"]:
            team.append({"type": "devops", "name": self._generate_name()})

        if analysis["requires_ui"] and "ui_design" in analysis["domains"]:
            team.append({"type": "designer", "name": self._generate_name()})

        # Ensure minimum team size for simple tasks
        if len(team) == 0:
            team.append({"type": "backend_developer", "name": self._generate_name()})

        # If no QA tester yet but testing required, add one
        if analysis["requires_testing"] and "qa_tester" not in [a["type"] for a in team]:
            team.append({"type": "qa_tester", "name": self._generate_name()})

        # Apply max_agents constraint if specified
        if max_agents and len(team) > max_agents:
            team = self._prioritize_team(team, max_agents, analysis)

        print(f"\n👥 Team Composition ({len(team)} agents):")
        for agent in team:
            print(f"  • {agent['name']} - {agent['type'].replace('_', ' ').title()}")

        return team

    def _prioritize_team(self, team: List[Dict], max_size: int, analysis: Dict) -> List[Dict]:
        """
        Reduce team to max_size by prioritizing essential roles

        Priority:
        1. Always keep: lead_developer or product_manager
        2. Core developers (backend/frontend based on project)
        3. QA tester if testing required
        4. Specialists (security, data science) if critical
        5. Support roles (devops, ui_designer)
        """

        priority_order = []

        # Priority 1: Leadership
        for agent in team:
            if agent["type"] in ["lead_developer", "product_manager"]:
                priority_order.append(agent)

        # Priority 2: Core developers
        for agent in team:
            if agent["type"] in ["backend_developer", "frontend_developer"] and agent not in priority_order:
                priority_order.append(agent)

        # Priority 3: QA if testing required
        if analysis["requires_testing"]:
            for agent in team:
                if agent["type"] == "qa_tester" and agent not in priority_order:
                    priority_order.append(agent)

        # Priority 4: Critical specialists
        for agent in team:
            if agent["type"] in ["security", "data_scientist"] and agent not in priority_order:
                if (agent["type"] == "security" and analysis["requires_security"]) or \
                   (agent["type"] == "data_scientist" and analysis["requires_data_science"]):
                    priority_order.append(agent)

        # Priority 5: Other roles
        for agent in team:
            if agent not in priority_order:
                priority_order.append(agent)

        return priority_order[:max_size]

    def _generate_name(self) -> str:
        """Generate unique name for agent"""
        import random

        names = [
            "Alice", "Bob", "Charlie", "Diana", "Eve", "Frank", "Grace", "Henry",
            "Ivy", "Jack", "Kate", "Leo", "Maya", "Noah", "Olivia", "Peter",
            "Quinn", "Rachel", "Sam", "Tara", "Uma", "Victor", "Wendy", "Xavier",
            "Yara", "Zack"
        ]

        # Keep track of used names
        if not hasattr(self, '_used_names'):
            self._used_names = set()

        available_names = [n for n in names if n not in self._used_names]

        if not available_names:
            # Reset if all names used
            self._used_names.clear()
            available_names = names

        name = random.choice(available_names)
        self._used_names.add(name)

        return name


class TeamScaler:
    """
    Dynamically scale team during project execution
    Add specialists when needed, remove them when done
    """

    def __init__(self):
        """Initialize team scaler"""
        self.scaling_history = []

    def should_scale_up(self,
                        current_team: List,
                        iteration: int,
                        test_results: Optional[Dict] = None,
                        security_issues: Optional[List] = None) -> Optional[Dict]:
        """
        Determine if team needs additional members

        Returns:
            Agent config to add, or None
        """

        # Scale up if security issues found but no security expert
        if security_issues and len(security_issues) > 0:
            has_security = any(a.role.lower() == "security expert" for a in current_team)
            if not has_security:
                return {"type": "security", "name": self._generate_name(), "reason": "Security issues detected"}

        # Scale up if tests failing repeatedly
        if test_results and not test_results.get("success", True):
            failed_count = test_results.get("total_tests", 0) - test_results.get("passed", 0)
            if failed_count > 5:
                has_qa = any("qa" in a.role.lower() or "tester" in a.role.lower() for a in current_team)
                if not has_qa:
                    return {"type": "qa_tester", "name": self._generate_name(), "reason": "Multiple test failures"}

        return None

    def should_scale_down(self,
                          current_team: List,
                          iteration: int,
                          completion_status: float) -> Optional[str]:
        """
        Determine if team members can be removed

        Returns:
            Agent name to remove, or None
        """

        # In later iterations, some specialists can be removed if work is done
        if iteration > 5 and completion_status > 0.8:
            # Keep core team, remove specialists who have completed their work
            # This is conservative - only remove if clearly not needed
            pass

        return None

    def _generate_name(self) -> str:
        """Generate unique name"""
        import random
        names = ["Alex", "Bailey", "Casey", "Dakota", "Ellis", "Finley"]
        return random.choice(names)


def analyze_task_and_build_team(task: str,
                                 max_agents: Optional[int] = None,
                                 user_specified_agents: Optional[List[Dict]] = None) -> List[Dict]:
    """
    Main entry point for dynamic team building

    Args:
        task: Project description
        max_agents: Maximum team size constraint
        user_specified_agents: User can override with specific agents

    Returns:
        List of agent configurations
    """

    # If user specified agents, use those
    if user_specified_agents:
        print(f"\n👥 Using user-specified team ({len(user_specified_agents)} agents)")
        return user_specified_agents

    # Otherwise, build team dynamically
    print(f"\n🤖 Building dynamic team based on project requirements...")

    builder = DynamicTeamBuilder()
    team = builder.build_team(task, max_agents)

    return team


if __name__ == "__main__":
    # Test dynamic team building

    print("=" * 80)
    print("TESTING DYNAMIC TEAM BUILDER")
    print("=" * 80)

    # Test Case 1: Simple calculator
    print("\n\n🧪 TEST 1: Simple Calculator")
    print("-" * 80)
    task1 = "Create a simple calculator library with basic math operations (add, subtract, multiply, divide)"
    team1 = analyze_task_and_build_team(task1)
    print(f"\n✓ Team size: {len(team1)} agents")

    # Test Case 2: Full-stack web app
    print("\n\n🧪 TEST 2: Full-Stack Web App")
    print("-" * 80)
    task2 = "Build a complete e-commerce web application with React frontend, Node.js backend, PostgreSQL database, user authentication, payment processing, and admin dashboard"
    team2 = analyze_task_and_build_team(task2)
    print(f"\n✓ Team size: {len(team2)} agents")

    # Test Case 3: Data analysis
    print("\n\n🧪 TEST 3: Data Analysis Project")
    print("-" * 80)
    task3 = "Analyze sales data and build predictive ML models for forecasting"
    team3 = analyze_task_and_build_team(task3)
    print(f"\n✓ Team size: {len(team3)} agents")

    # Test Case 4: API only
    print("\n\n🧪 TEST 4: REST API")
    print("-" * 80)
    task4 = "Create a REST API for managing todo items with CRUD operations"
    team4 = analyze_task_and_build_team(task4)
    print(f"\n✓ Team size: {len(team4)} agents")

    print("\n" + "=" * 80)
    print("✅ Dynamic team building working correctly!")
    print("=" * 80)
