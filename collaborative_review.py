"""
Collaborative Agent Review System
Agents critique and improve each other's work in real-time

Workflow:
1. Developer agent creates code
2. Lead developer reviews architecture
3. Other developers review implementation
4. QA tester reviews testability and creates tests
5. Original developer addresses feedback
6. Iterate until consensus
"""

from typing import List, Dict, Optional
from pathlib import Path
from langchain_core.messages import HumanMessage, SystemMessage
import colorama
import re

colorama.init(autoreset=True)


class CollaborativeReview:
    """
    Manages collaborative code review between agents
    Each agent type provides specialized feedback
    """

    def __init__(self):
        """Initialize collaborative review system"""
        self.review_rounds = []
        self.feedback_history = []

    def conduct_review(
        self,
        file_path: str,
        code_content: str,
        author_agent: 'FileAwareAgent',
        reviewer_agents: List['FileAwareAgent'],
        context: str,
        file_manager: 'FileManager',
        max_rounds: int = 2
    ) -> Dict:
        """
        Conduct collaborative code review

        Args:
            file_path: Path to the file being reviewed
            code_content: The code content
            author_agent: Agent who wrote the code
            reviewer_agents: Agents who will review
            context: Project context
            file_manager: FileManager for code updates
            max_rounds: Maximum review rounds

        Returns:
            Dict with review results and final code
        """
        print(colorama.Fore.MAGENTA + f"\n{'='*80}")
        print(f"🤝 COLLABORATIVE REVIEW: {file_path}")
        print(f"Author: {author_agent.name} ({author_agent.role})")
        print(f"Reviewers: {', '.join([a.name for a in reviewer_agents])}")
        print(f"{'='*80}\n" + colorama.Style.RESET_ALL)

        current_code = code_content
        all_feedback = []

        for round_num in range(max_rounds):
            print(colorama.Fore.CYAN + f"\n--- Review Round {round_num + 1} ---\n" + colorama.Style.RESET_ALL)

            round_feedback = []
            has_critical_issues = False

            # Each reviewer provides feedback
            for reviewer in reviewer_agents:
                print(colorama.Fore.YELLOW + f"👤 {reviewer.name} ({reviewer.role}) reviewing..." + colorama.Style.RESET_ALL)

                feedback = self._get_specialized_feedback(
                    reviewer,
                    file_path,
                    current_code,
                    context
                )

                round_feedback.append({
                    "reviewer": reviewer.name,
                    "role": reviewer.role,
                    "feedback": feedback["feedback"],
                    "issues": feedback["issues"],
                    "approval": feedback["approval"]
                })

                # Print summary
                if feedback["approval"]:
                    print(colorama.Fore.GREEN + f"  ✅ Approved by {reviewer.name}" + colorama.Style.RESET_ALL)
                else:
                    print(colorama.Fore.RED + f"  ❌ Issues found by {reviewer.name}" + colorama.Style.RESET_ALL)
                    has_critical_issues = True
                    for issue in feedback["issues"][:3]:
                        print(colorama.Fore.YELLOW + f"     • {issue}" + colorama.Style.RESET_ALL)

            all_feedback.extend(round_feedback)

            # If all approved, done!
            if not has_critical_issues:
                print(colorama.Fore.GREEN + f"\n✅ All reviewers approved! Review complete.\n" + colorama.Style.RESET_ALL)
                break

            # Author addresses feedback
            print(colorama.Fore.CYAN + f"\n🔧 {author_agent.name} addressing feedback...\n" + colorama.Style.RESET_ALL)

            updated_code = self._author_addresses_feedback(
                author_agent,
                file_path,
                current_code,
                round_feedback,
                context
            )

            if updated_code and updated_code != current_code:
                current_code = updated_code
                print(colorama.Fore.GREEN + f"  ✓ Code updated based on feedback" + colorama.Style.RESET_ALL)

                # Save updated code
                file_manager.update_file(file_path, current_code, author_agent.name)
            else:
                print(colorama.Fore.YELLOW + f"  ⚠️ No changes made" + colorama.Style.RESET_ALL)
                break

        return {
            "file": file_path,
            "author": author_agent.name,
            "reviewers": [r.name for r in reviewer_agents],
            "rounds": round_num + 1,
            "feedback": all_feedback,
            "final_code": current_code,
            "approved": not has_critical_issues
        }

    def _get_specialized_feedback(
        self,
        reviewer: 'FileAwareAgent',
        file_path: str,
        code: str,
        context: str
    ) -> Dict:
        """
        Get specialized feedback based on reviewer role

        Args:
            reviewer: The reviewing agent
            file_path: File being reviewed
            code: Code content
            context: Project context

        Returns:
            Dict with feedback and approval status
        """
        role = reviewer.role.lower()

        # Customize review prompt based on role
        if "lead" in role or "architect" in role:
            focus_areas = """
Focus on:
- System architecture and design patterns
- Code organization and structure
- Scalability and maintainability
- Best practices and standards
- Integration with other components
"""
        elif "backend" in role:
            focus_areas = """
Focus on:
- API design and endpoints
- Database queries and optimization
- Error handling and validation
- Security vulnerabilities
- Performance implications
"""
        elif "frontend" in role:
            focus_areas = """
Focus on:
- UI/UX implementation
- Component structure
- State management
- Accessibility
- Browser compatibility
"""
        elif "qa" in role or "tester" in role:
            focus_areas = """
Focus on:
- Testability of the code
- Edge cases and error scenarios
- Test coverage gaps
- Potential bugs
- Whether comprehensive tests exist
"""
        elif "security" in role:
            focus_areas = """
Focus on:
- Security vulnerabilities
- Input validation
- Authentication/authorization
- Data protection
- Common security pitfalls (OWASP Top 10)
"""
        else:
            focus_areas = """
Focus on:
- Code quality
- Best practices
- Potential issues
"""

        review_prompt = f"""You are reviewing code as a {reviewer.role}.

**File:** {file_path}
**Context:** {context}

**Code to Review:**
```
{code}
```

{focus_areas}

Provide your review in this format:

## Your Assessment
[APPROVE/REQUEST_CHANGES]

## Issues Found (if any)
1. Issue description
2. Issue description
...

## Specific Recommendations
- Recommendation 1
- Recommendation 2

## Approval Decision
State clearly: APPROVE or REQUEST_CHANGES

Be specific and constructive. Focus on your area of expertise.
"""

        response = reviewer.step(HumanMessage(content=review_prompt))
        feedback_text = response.content

        # Parse approval decision
        approval = "APPROVE" in feedback_text.upper()

        # Extract issues (lines starting with numbers or bullets)
        issues = []
        for line in feedback_text.split('\n'):
            line = line.strip()
            if line and (line[0].isdigit() or line.startswith('-') or line.startswith('•')):
                # Clean up the line
                issue = line.lstrip('0123456789.-•').strip()
                if len(issue) > 10:  # Meaningful issue
                    issues.append(issue)

        return {
            "feedback": feedback_text,
            "approval": approval,
            "issues": issues[:10]  # Max 10 issues
        }

    def _author_addresses_feedback(
        self,
        author: 'FileAwareAgent',
        file_path: str,
        current_code: str,
        feedback_list: List[Dict],
        context: str
    ) -> Optional[str]:
        """
        Original author addresses reviewer feedback

        Args:
            author: The author agent
            file_path: File being updated
            current_code: Current code version
            feedback_list: List of feedback from reviewers
            context: Project context

        Returns:
            Updated code or None if no changes
        """
        # Compile all feedback
        feedback_summary = f"Your code for {file_path} has been reviewed.\n\n"

        for fb in feedback_list:
            feedback_summary += f"\n**{fb['reviewer']} ({fb['role']}):**\n"
            if fb['approval']:
                feedback_summary += "✅ Approved\n"
            else:
                feedback_summary += "❌ Requested Changes:\n"
                for issue in fb['issues'][:5]:
                    feedback_summary += f"  • {issue}\n"

        update_prompt = f"""You wrote the following code:

**File:** {file_path}
**Context:** {context}

**Your Code:**
```
{current_code}
```

{feedback_summary}

Please address ALL the issues raised by reviewers and provide updated code.

**Requirements:**
1. Fix all critical issues mentioned
2. Implement suggested improvements
3. Maintain code functionality
4. Keep the code clean and readable

Provide your updated code in this format:

```filename: {file_path}
[Your updated code here]
```

If you believe no changes are needed, explain why.
"""

        response = author.step(HumanMessage(content=update_prompt))
        response_text = response.content

        # Extract updated code
        if f"```filename: {file_path}" in response_text or "```update:" in response_text:
            # Parse code blocks
            pattern = r'```(?:filename:|update:)\s*' + re.escape(file_path) + r'\s*\n(.*?)```'
            matches = re.findall(pattern, response_text, re.DOTALL)

            if matches:
                return matches[0].strip()

        # Alternative: look for any code block
        code_blocks = re.findall(r'```(?:\w+)?\s*\n(.*?)```', response_text, re.DOTALL)
        if code_blocks:
            return code_blocks[0].strip()

        return None

    def get_review_summary(self, review_result: Dict) -> str:
        """
        Generate a summary of the review process

        Args:
            review_result: Result from conduct_review()

        Returns:
            Formatted summary string
        """
        summary = f"""
{'='*80}
COLLABORATIVE REVIEW SUMMARY
{'='*80}

File: {review_result['file']}
Author: {review_result['author']}
Reviewers: {', '.join(review_result['reviewers'])}
Rounds: {review_result['rounds']}
Final Status: {"✅ APPROVED" if review_result['approved'] else "⚠️ NEEDS MORE WORK"}

Review Feedback:
"""

        for fb in review_result['feedback']:
            summary += f"\n{fb['reviewer']} ({fb['role']}):\n"
            if fb['approval']:
                summary += "  ✅ Approved\n"
            else:
                summary += "  ❌ Issues found:\n"
                for issue in fb['issues'][:3]:
                    summary += f"    • {issue}\n"

        summary += "\n" + "="*80 + "\n"
        return summary


class TeamReviewOrchestrator:
    """
    Orchestrates collaborative reviews for entire projects
    Determines which agents should review which files
    """

    def __init__(self):
        """Initialize team review orchestrator"""
        self.collaborative_review = CollaborativeReview()

    def determine_reviewers(
        self,
        author_role: str,
        file_path: str,
        all_agents: List['FileAwareAgent']
    ) -> List['FileAwareAgent']:
        """
        Determine which agents should review a file

        Args:
            author_role: Role of the author agent
            file_path: File being reviewed
            all_agents: All available agents

        Returns:
            List of reviewer agents
        """
        reviewers = []
        file_ext = Path(file_path).suffix
        author_role_lower = author_role.lower()

        # Always include lead developer if available
        for agent in all_agents:
            if "lead" in agent.role.lower() and agent.role.lower() != author_role_lower:
                reviewers.append(agent)
                break

        # Add role-specific reviewers based on file type
        if file_ext in ['.py', '.js', '.ts', '.java', '.go']:
            # Code file - add developers
            for agent in all_agents:
                role_lower = agent.role.lower()

                # Add complementary developers
                if "backend" in author_role_lower and "frontend" in role_lower:
                    reviewers.append(agent)
                elif "frontend" in author_role_lower and "backend" in role_lower:
                    reviewers.append(agent)

        # Always add QA tester for code files
        for agent in all_agents:
            if ("qa" in agent.role.lower() or "tester" in agent.role.lower()) and agent not in reviewers:
                reviewers.append(agent)
                break

        # Add security expert for sensitive files
        if any(keyword in file_path.lower() for keyword in ['auth', 'login', 'password', 'security', 'api']):
            for agent in all_agents:
                if "security" in agent.role.lower() and agent not in reviewers:
                    reviewers.append(agent)
                    break

        # Limit to 3 reviewers max
        return reviewers[:3]

    def review_project_files(
        self,
        files_created: Dict,  # {file_path: {author: agent, content: code}}
        all_agents: List['FileAwareAgent'],
        file_manager: 'FileManager',
        context: str
    ) -> List[Dict]:
        """
        Review all files in a project

        Args:
            files_created: Dict of files created this iteration
            all_agents: All available agents
            file_manager: FileManager instance
            context: Project context

        Returns:
            List of review results
        """
        print(colorama.Fore.MAGENTA + f"\n{'='*80}")
        print(f"🔍 STARTING COLLABORATIVE PROJECT REVIEW")
        print(f"Files to review: {len(files_created)}")
        print(f"{'='*80}\n" + colorama.Style.RESET_ALL)

        results = []

        for file_path, file_info in files_created.items():
            author = file_info['author']
            content = file_info['content']

            # Determine appropriate reviewers
            reviewers = self.determine_reviewers(
                author.role,
                file_path,
                [a for a in all_agents if a != author]
            )

            if not reviewers:
                print(colorama.Fore.YELLOW + f"⚠️ No reviewers available for {file_path}" + colorama.Style.RESET_ALL)
                continue

            # Conduct review
            review_result = self.collaborative_review.conduct_review(
                file_path,
                content,
                author,
                reviewers,
                context,
                file_manager,
                max_rounds=2
            )

            results.append(review_result)

            # Print summary
            summary = self.collaborative_review.get_review_summary(review_result)
            print(summary)

        return results


# Example usage
if __name__ == "__main__":
    print("\n🧪 Testing Collaborative Review System\n")

    # This would normally use real FileAwareAgent instances
    # Here we just demonstrate the structure

    print("""
Collaborative Review Workflow:

1. Frontend Developer creates React component
   ↓
2. Lead Developer reviews architecture
   ↓
3. Backend Developer reviews API integration
   ↓
4. QA Tester reviews testability
   ↓
5. Frontend Developer addresses all feedback
   ↓
6. Second review round if needed
   ↓
7. Approval by all reviewers

Benefits:
✅ Catches issues early
✅ Knowledge sharing across team
✅ Better code quality
✅ Multiple perspectives
✅ Collaborative improvement
""")

    print("✅ Collaborative review system ready for integration!")
