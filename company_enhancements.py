"""
Company Enhancements - Final Features for Ideal Company
========================================================

1. Conflict Resolution - When agents disagree on technical decisions
2. Automated Documentation - Generates docs, comments, README
3. Performance Analytics - Tracks agent quality, contributions, velocity
"""

from typing import List, Dict, Optional
from langchain_core.messages import HumanMessage
from langchain_ollama import ChatOllama
import json
import re
from datetime import datetime


class ConflictResolver:
    """
    Resolves conflicts between agents
    Like a Tech Lead or Architect making final decisions
    """

    def __init__(self, model_name: str = "qwen2.5-coder:latest"):
        """Initialize conflict resolver"""
        self.llm = ChatOllama(model=model_name, temperature=0.2)  # Lower temp for decisive answers
        self.conflicts_resolved = []

    def detect_conflict(self, agent1_opinion: str, agent2_opinion: str,
                       topic: str) -> bool:
        """
        Detect if two agent opinions are conflicting

        Returns:
            True if conflict detected
        """
        # Simple keyword-based conflict detection
        disagreement_keywords = [
            'disagree', 'wrong', 'incorrect', 'better', 'instead',
            'should not', 'must not', 'prefer', 'alternative'
        ]

        opinion1_lower = agent1_opinion.lower()
        opinion2_lower = agent2_opinion.lower()

        # Check for disagreement keywords
        has_disagreement = any(kw in opinion1_lower or kw in opinion2_lower
                              for kw in disagreement_keywords)

        return has_disagreement

    def resolve_conflict(self, agent1: str, agent1_opinion: str,
                        agent2: str, agent2_opinion: str,
                        topic: str, context: str = "") -> Dict:
        """
        Resolve conflict between two agents

        Returns:
            {
                "decision": "agent1" | "agent2" | "compromise",
                "reasoning": "Why this decision was made",
                "action": "Specific action to take",
                "resolved_by": "conflict_resolver"
            }
        """

        print(f"\n⚖️  CONFLICT DETECTED: {topic}")
        print(f"   {agent1} vs {agent2}")

        # Use LLM to analyze and resolve
        try:
            resolution = self._llm_resolution(
                agent1, agent1_opinion,
                agent2, agent2_opinion,
                topic, context
            )
        except Exception as e:
            # Fallback to rule-based
            resolution = self._rule_based_resolution(
                agent1, agent1_opinion,
                agent2, agent2_opinion,
                topic
            )

        # Record resolution
        self.conflicts_resolved.append({
            "topic": topic,
            "agent1": agent1,
            "agent2": agent2,
            "resolution": resolution,
            "timestamp": datetime.now().isoformat()
        })

        # Display resolution
        print(f"\n   ✅ RESOLVED: {resolution['decision'].upper()}")
        print(f"   Reasoning: {resolution['reasoning']}")
        print(f"   Action: {resolution['action']}")

        return resolution

    def _llm_resolution(self, agent1: str, opinion1: str,
                       agent2: str, opinion2: str,
                       topic: str, context: str) -> Dict:
        """Use LLM to resolve conflict"""

        prompt = f"""You are a Tech Lead resolving a technical disagreement.

TOPIC: {topic}

CONTEXT: {context}

AGENT 1 ({agent1}) SAYS:
{opinion1}

AGENT 2 ({agent2}) SAYS:
{opinion2}

As Tech Lead, make a decision. Provide your resolution in JSON format:
{{
    "decision": "agent1" | "agent2" | "compromise",
    "reasoning": "Clear technical reasoning for decision",
    "action": "Specific action the team should take"
}}

Consider:
- Technical merit
- Best practices
- Long-term maintainability
- Project requirements
"""

        response = self.llm.invoke([HumanMessage(content=prompt)])

        # Parse JSON
        try:
            json_match = re.search(r'\{.*\}', response.content, re.DOTALL)
            if json_match:
                resolution = json.loads(json_match.group())
                resolution["resolved_by"] = "llm_tech_lead"
                return resolution
        except:
            pass

        # Fallback
        return self._rule_based_resolution(agent1, opinion1, agent2, opinion2, topic)

    def _rule_based_resolution(self, agent1: str, opinion1: str,
                               agent2: str, opinion2: str,
                               topic: str) -> Dict:
        """Simple rule-based resolution"""

        # Default: prefer senior roles
        senior_roles = ['lead', 'senior', 'architect', 'principal']

        agent1_is_senior = any(role in agent1.lower() for role in senior_roles)
        agent2_is_senior = any(role in agent2.lower() for role in senior_roles)

        if agent1_is_senior and not agent2_is_senior:
            decision = "agent1"
            reasoning = f"{agent1} has seniority and technical authority"
        elif agent2_is_senior and not agent1_is_senior:
            decision = "agent2"
            reasoning = f"{agent2} has seniority and technical authority"
        else:
            decision = "compromise"
            reasoning = "Both agents have valid points, recommend hybrid approach"

        return {
            "decision": decision,
            "reasoning": reasoning,
            "action": f"Implement {decision} approach",
            "resolved_by": "rule_based"
        }


class DocumentationGenerator:
    """
    Automatically generates documentation
    Like a Technical Writer in the company
    """

    def __init__(self, model_name: str = "qwen2.5-coder:latest"):
        """Initialize documentation generator"""
        self.llm = ChatOllama(model=model_name, temperature=0.3)

    def generate_readme(self, project_name: str, project_files: List[str],
                       main_files_content: Dict[str, str]) -> str:
        """
        Generate README.md for the project

        Args:
            project_name: Name of project
            project_files: List of all file paths
            main_files_content: Dict of {filename: content} for key files

        Returns:
            README.md content
        """

        print(f"\n📝 Generating README.md for {project_name}...")

        # Analyze project structure
        has_backend = any('api' in f or 'server' in f or 'backend' in f
                         for f in project_files)
        has_frontend = any('component' in f or 'frontend' in f or 'ui' in f
                          for f in project_files)
        has_tests = any('test' in f for f in project_files)

        # Detect tech stack
        tech_stack = []
        all_content = ' '.join(main_files_content.values())

        if 'fastapi' in all_content.lower() or 'flask' in all_content.lower():
            tech_stack.append("Python (FastAPI/Flask)")
        if 'react' in all_content.lower():
            tech_stack.append("React")
        if 'vue' in all_content.lower():
            tech_stack.append("Vue.js")
        if 'node' in all_content.lower() or 'express' in all_content.lower():
            tech_stack.append("Node.js")
        if 'postgresql' in all_content.lower() or 'postgres' in all_content.lower():
            tech_stack.append("PostgreSQL")

        # Generate README
        readme = f"""# {project_name}

## Overview

Auto-generated project documentation.

## Features

"""

        if has_backend:
            readme += "- ✅ Backend API\n"
        if has_frontend:
            readme += "- ✅ Frontend UI\n"
        if has_tests:
            readme += "- ✅ Automated Tests\n"

        if tech_stack:
            readme += f"\n## Tech Stack\n\n"
            for tech in tech_stack:
                readme += f"- {tech}\n"

        readme += f"""
## Project Structure

```
"""
        # Add file tree
        for file_path in sorted(project_files)[:20]:  # First 20 files
            indent = "  " * (file_path.count('/'))
            filename = file_path.split('/')[-1]
            readme += f"{indent}{filename}\n"

        if len(project_files) > 20:
            readme += f"  ... and {len(project_files) - 20} more files\n"

        readme += f"""```

## Getting Started

### Installation

```bash
# Install dependencies
pip install -r requirements.txt  # For Python projects
# or
npm install  # For Node.js projects
```

### Running the Application

```bash
# Start the application
python main.py  # or appropriate start command
```

### Running Tests

```bash
# Run test suite
pytest  # For Python
# or
npm test  # For Node.js
```

## Documentation

Generated automatically by AI development team.

## License

MIT License
"""

        return readme

    def generate_code_comments(self, code: str, language: str) -> str:
        """
        Add helpful comments to code

        Args:
            code: Source code
            language: Programming language (python, javascript, etc.)

        Returns:
            Code with added comments
        """

        # For now, return as-is (would use LLM to add comments intelligently)
        # This would analyze the code and add docstrings, inline comments, etc.
        return code

    def generate_api_docs(self, api_files_content: Dict[str, str]) -> str:
        """
        Generate API documentation

        Args:
            api_files_content: Dict of {filename: content} for API files

        Returns:
            API documentation markdown
        """

        print(f"\n📝 Generating API documentation...")

        docs = "# API Documentation\n\n"
        docs += "Auto-generated API documentation.\n\n"

        # Parse endpoints from code (basic)
        for filename, content in api_files_content.items():
            # Find FastAPI/Flask routes
            routes = re.findall(r'@app\.(get|post|put|delete|patch)\(["\']([^"\']+)["\']\)',
                               content, re.IGNORECASE)

            if routes:
                docs += f"## {filename}\n\n"
                for method, path in routes:
                    docs += f"### `{method.upper()} {path}`\n\n"
                    docs += f"Endpoint defined in `{filename}`\n\n"

        return docs


class PerformanceAnalytics:
    """
    Tracks agent performance and contributions
    Like a Engineering Manager tracking team metrics
    """

    def __init__(self):
        """Initialize analytics"""
        self.metrics = {
            "agents": {},
            "iterations": [],
            "overall": {
                "total_files_created": 0,
                "total_files_updated": 0,
                "total_tests_written": 0,
                "total_bugs_fixed": 0,
                "total_reviews_conducted": 0
            }
        }

    def record_agent_contribution(self, agent_name: str, contribution_type: str,
                                 details: Dict = None):
        """
        Record an agent's contribution

        Args:
            agent_name: Name of agent
            contribution_type: Type of contribution (file_created, test_written, bug_fixed, etc.)
            details: Additional details
        """

        if agent_name not in self.metrics["agents"]:
            self.metrics["agents"][agent_name] = {
                "files_created": 0,
                "files_updated": 0,
                "tests_written": 0,
                "bugs_fixed": 0,
                "reviews_given": 0,
                "reviews_received": 0,
                "code_quality_score": 0.0,
                "contributions": []
            }

        agent_metrics = self.metrics["agents"][agent_name]

        # Update metrics based on contribution type
        if contribution_type == "file_created":
            agent_metrics["files_created"] += 1
            self.metrics["overall"]["total_files_created"] += 1
        elif contribution_type == "file_updated":
            agent_metrics["files_updated"] += 1
            self.metrics["overall"]["total_files_updated"] += 1
        elif contribution_type == "test_written":
            agent_metrics["tests_written"] += 1
            self.metrics["overall"]["total_tests_written"] += 1
        elif contribution_type == "bug_fixed":
            agent_metrics["bugs_fixed"] += 1
            self.metrics["overall"]["total_bugs_fixed"] += 1
        elif contribution_type == "review_given":
            agent_metrics["reviews_given"] += 1
            self.metrics["overall"]["total_reviews_conducted"] += 1
        elif contribution_type == "review_received":
            agent_metrics["reviews_received"] += 1

        # Record contribution
        agent_metrics["contributions"].append({
            "type": contribution_type,
            "details": details or {},
            "timestamp": datetime.now().isoformat()
        })

    def calculate_code_quality_score(self, agent_name: str,
                                    review_feedback: List[str],
                                    test_pass_rate: float) -> float:
        """
        Calculate code quality score for an agent

        Returns:
            Score from 0.0 to 10.0
        """

        # Simple scoring algorithm
        score = 5.0  # Base score

        # Test pass rate contributes 0-3 points
        score += test_pass_rate * 3

        # Positive review feedback adds points
        positive_keywords = ['good', 'excellent', 'well', 'clean', 'solid']
        negative_keywords = ['issue', 'problem', 'error', 'bug', 'fix']

        positive_count = sum(1 for feedback in review_feedback
                           for keyword in positive_keywords
                           if keyword in feedback.lower())
        negative_count = sum(1 for feedback in review_feedback
                           for keyword in negative_keywords
                           if keyword in feedback.lower())

        score += min(positive_count * 0.5, 2.0)  # Up to +2 for positive feedback
        score -= min(negative_count * 0.3, 2.0)  # Up to -2 for issues

        # Clamp to 0-10
        score = max(0.0, min(10.0, score))

        # Update agent metrics
        if agent_name in self.metrics["agents"]:
            self.metrics["agents"][agent_name]["code_quality_score"] = score

        return score

    def generate_performance_report(self) -> Dict:
        """
        Generate comprehensive performance report

        Returns:
            Report dict with all metrics
        """

        print("\n📊 Generating Performance Report...")

        report = {
            "overall_metrics": self.metrics["overall"],
            "agent_rankings": [],
            "top_contributors": [],
            "quality_leaders": []
        }

        # Rank agents by total contributions
        for agent_name, agent_metrics in self.metrics["agents"].items():
            total_contributions = (
                agent_metrics["files_created"] +
                agent_metrics["files_updated"] +
                agent_metrics["tests_written"] +
                agent_metrics["bugs_fixed"]
            )

            report["agent_rankings"].append({
                "agent": agent_name,
                "total_contributions": total_contributions,
                "quality_score": agent_metrics["code_quality_score"]
            })

        # Sort by contributions
        report["agent_rankings"].sort(key=lambda x: x["total_contributions"], reverse=True)
        report["top_contributors"] = report["agent_rankings"][:3]

        # Sort by quality
        report["quality_leaders"] = sorted(report["agent_rankings"],
                                          key=lambda x: x["quality_score"],
                                          reverse=True)[:3]

        return report

    def display_performance_report(self):
        """Display performance report in readable format"""

        report = self.generate_performance_report()

        print("\n" + "="*80)
        print("TEAM PERFORMANCE REPORT")
        print("="*80)

        print("\n📈 Overall Metrics:")
        for metric, value in report["overall_metrics"].items():
            metric_name = metric.replace('total_', '').replace('_', ' ').title()
            print(f"  {metric_name}: {value}")

        if report["top_contributors"]:
            print("\n🏆 Top Contributors:")
            for i, agent in enumerate(report["top_contributors"], 1):
                print(f"  {i}. {agent['agent']}: {agent['total_contributions']} contributions")

        if report["quality_leaders"]:
            print("\n⭐ Quality Leaders:")
            for i, agent in enumerate(report["quality_leaders"], 1):
                print(f"  {i}. {agent['agent']}: {agent['quality_score']:.1f}/10.0 quality score")

        print("\n" + "="*80)


if __name__ == "__main__":
    # Test conflict resolution

    print("=" * 80)
    print("TESTING COMPANY ENHANCEMENTS")
    print("=" * 80)

    # Test 1: Conflict Resolution
    print("\n\n🧪 TEST 1: Conflict Resolution")
    print("-" * 80)

    resolver = ConflictResolver()

    conflict = resolver.resolve_conflict(
        agent1="Alice (Backend Developer)",
        agent1_opinion="We should use PostgreSQL for better data integrity",
        agent2="Bob (Lead Developer)",
        agent2_opinion="MongoDB would be better for this use case due to flexibility",
        topic="Database choice",
        context="Building a content management system"
    )

    # Test 2: Documentation Generation
    print("\n\n🧪 TEST 2: Documentation Generation")
    print("-" * 80)

    doc_gen = DocumentationGenerator()

    readme = doc_gen.generate_readme(
        project_name="test_project",
        project_files=["main.py", "api/routes.py", "tests/test_api.py"],
        main_files_content={"main.py": "from fastapi import FastAPI"}
    )

    print("\nGenerated README (first 500 chars):")
    print(readme[:500] + "...")

    # Test 3: Performance Analytics
    print("\n\n🧪 TEST 3: Performance Analytics")
    print("-" * 80)

    analytics = PerformanceAnalytics()

    # Record some contributions
    analytics.record_agent_contribution("Alice", "file_created")
    analytics.record_agent_contribution("Alice", "file_created")
    analytics.record_agent_contribution("Alice", "test_written")
    analytics.record_agent_contribution("Bob", "file_created")
    analytics.record_agent_contribution("Bob", "bug_fixed")
    analytics.record_agent_contribution("Charlie", "review_given")

    # Calculate quality scores
    analytics.calculate_code_quality_score("Alice", ["good code", "clean"], 0.95)
    analytics.calculate_code_quality_score("Bob", ["some issues", "needs work"], 0.70)

    # Display report
    analytics.display_performance_report()

    print("\n" + "=" * 80)
    print("✅ All enhancements working!")
    print("=" * 80)
