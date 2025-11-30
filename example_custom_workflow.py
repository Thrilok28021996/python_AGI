"""
Example: Custom Workflow
Create your own custom workflow mixing different approaches

Use case: Complex projects needing custom coordination
"""

from agent_team import AgentTeam
from langchain_core.messages import HumanMessage
import colorama


def custom_code_review_workflow():
    """
    Custom workflow: Code review process
    1. Developer writes code
    2. Multiple reviewers provide feedback simultaneously
    3. Developer addresses feedback
    4. Security expert does final check
    """

    project_task = """
    Implement a user authentication system with:
    - Email/password login
    - JWT tokens
    - Password hashing with bcrypt
    - Rate limiting
    - Session management
    """

    # Create team
    team_config = {
        "Dev": "backend_developer",
        "Lead": "lead_developer",
        "Security": "security",
        "QA": "qa_tester"
    }

    team = AgentTeam(team_config)

    print(colorama.Fore.MAGENTA + "\n" + "="*80)
    print("CUSTOM WORKFLOW: Code Review Process")
    print("="*80 + "\n" + colorama.Style.RESET_ALL)

    # Step 1: Developer implements
    print(colorama.Fore.CYAN + "=== Step 1: Initial Implementation ===" + colorama.Style.RESET_ALL)
    dev_agent = team.get_agent("Dev")
    dev_response = dev_agent.step(HumanMessage(content=f"Implement: {project_task}"))

    print(colorama.Fore.GREEN + f"Developer:\n{dev_response.content}\n" + colorama.Style.RESET_ALL)

    # Step 2: Parallel reviews
    print(colorama.Fore.CYAN + "\n=== Step 2: Parallel Code Reviews ===" + colorama.Style.RESET_ALL)

    review_context = f"Review this implementation:\n\n{dev_response.content}"

    reviewers = ["Lead", "Security", "QA"]
    reviews = []

    for reviewer_name in reviewers:
        reviewer = team.get_agent(reviewer_name)
        review = reviewer.step(HumanMessage(content=review_context))
        reviews.append((reviewer_name, review.content))

        print(colorama.Fore.GREEN + f"\n{reviewer.name} ({reviewer.role}):\n{review.content}\n" + colorama.Style.RESET_ALL)

    # Step 3: Developer addresses feedback
    print(colorama.Fore.CYAN + "\n=== Step 3: Address Feedback ===" + colorama.Style.RESET_ALL)

    feedback_summary = "\n\n".join([f"{name}: {review}" for name, review in reviews])
    revision_prompt = f"""Based on the following reviews, revise your implementation:

{feedback_summary}

Provide updated code addressing all concerns.
"""

    revision = dev_agent.step(HumanMessage(content=revision_prompt))
    print(colorama.Fore.GREEN + f"Developer (Revised):\n{revision.content}\n" + colorama.Style.RESET_ALL)

    # Step 4: Final security check
    print(colorama.Fore.CYAN + "\n=== Step 4: Final Security Approval ===" + colorama.Style.RESET_ALL)

    security_agent = team.get_agent("Security")
    final_check = security_agent.step(HumanMessage(
        content=f"Perform final security review:\n\n{revision.content}"
    ))

    print(colorama.Fore.GREEN + f"Security Expert:\n{final_check.content}\n" + colorama.Style.RESET_ALL)

    print(colorama.Fore.MAGENTA + "\n" + "="*80)
    print("CODE REVIEW COMPLETE")
    print("="*80 + "\n" + colorama.Style.RESET_ALL)


def custom_sprint_planning_workflow():
    """
    Custom workflow: Sprint planning
    1. Product manager defines user stories
    2. Team estimates together
    3. CEO approves sprint goals
    """

    project_task = """
    Plan a 2-week sprint for our project management app.
    We have 3 developers available.

    Backlog items:
    - Task dependencies feature
    - Gantt chart view
    - Email notifications
    - Mobile app improvements
    - Performance optimization
    """

    # Create team
    team_config = {
        "PM": "product_manager",
        "CEO": "ceo",
        "Lead": "lead_developer",
        "Dev1": "backend_developer",
        "Dev2": "frontend_developer"
    }

    team = AgentTeam(team_config)

    print(colorama.Fore.MAGENTA + "\n" + "="*80)
    print("CUSTOM WORKFLOW: Sprint Planning")
    print("="*80 + "\n" + colorama.Style.RESET_ALL)

    # Step 1: PM prioritizes
    print(colorama.Fore.CYAN + "=== Step 1: Product Manager Prioritization ===" + colorama.Style.RESET_ALL)
    pm_agent = team.get_agent("PM")
    pm_response = pm_agent.step(HumanMessage(content=f"Prioritize and create user stories:\n{project_task}"))
    print(colorama.Fore.GREEN + f"Product Manager:\n{pm_response.content}\n" + colorama.Style.RESET_ALL)

    # Step 2: Team estimation
    print(colorama.Fore.CYAN + "\n=== Step 2: Team Estimation ===" + colorama.Style.RESET_ALL)

    estimation_context = f"Estimate effort for these stories:\n\n{pm_response.content}"

    for dev_name in ["Lead", "Dev1", "Dev2"]:
        dev = team.get_agent(dev_name)
        estimate = dev.step(HumanMessage(content=estimation_context))
        print(colorama.Fore.GREEN + f"\n{dev.name}:\n{estimate.content}\n" + colorama.Style.RESET_ALL)

    # Step 3: CEO approval
    print(colorama.Fore.CYAN + "\n=== Step 3: CEO Approval ===" + colorama.Style.RESET_ALL)
    ceo_agent = team.get_agent("CEO")
    approval = ceo_agent.step(HumanMessage(
        content=f"Review sprint plan and approve:\n\n{pm_response.content}"
    ))
    print(colorama.Fore.GREEN + f"CEO:\n{approval.content}\n" + colorama.Style.RESET_ALL)

    print(colorama.Fore.MAGENTA + "\n" + "="*80)
    print("SPRINT PLANNING COMPLETE")
    print("="*80 + "\n" + colorama.Style.RESET_ALL)


def main():
    print("\nSelect a custom workflow to run:")
    print("1. Code Review Process")
    print("2. Sprint Planning")

    choice = input("\nEnter choice (1 or 2): ").strip()

    if choice == "1":
        custom_code_review_workflow()
    elif choice == "2":
        custom_sprint_planning_workflow()
    else:
        print("Invalid choice. Running Code Review Process...")
        custom_code_review_workflow()


if __name__ == "__main__":
    main()
