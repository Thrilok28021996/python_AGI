"""
Example: Hierarchical Workflow
A manager (CEO/Product Manager) directs a team of specialists

Use case: Complete project development with management oversight
"""

from agent_team import AgentTeam


def main():
    # Define the project
    project_task = """
    Develop a complete e-commerce website for selling handmade crafts:

    Features needed:
    - Product catalog with search and filters
    - Shopping cart
    - Checkout with payment integration (Stripe)
    - User accounts and order history
    - Admin panel for sellers
    - Responsive design
    - Email notifications

    Timeline: 2 sprints
    Budget: Limited - use open source tools
    """

    # Create a team with a CEO managing specialists
    team_config = {
        "Jennifer": "ceo",                  # Manager
        "Chris": "backend_developer",       # Backend specialist
        "Nina": "frontend_developer",       # Frontend specialist
        "Kevin": "designer",                # UI/UX designer
        "Olivia": "qa_tester"              # QA specialist
    }

    # Initialize the team
    team = AgentTeam(team_config)

    print("\n" + "="*80)
    print("HIERARCHICAL WORKFLOW EXAMPLE")
    print("CEO manages and coordinates the development team")
    print("="*80 + "\n")

    # Run hierarchical workflow
    results = team.hierarchical_workflow(
        task=project_task,
        manager="Jennifer",  # CEO directs the team
        team=["Chris", "Nina", "Kevin", "Olivia"],
        max_iterations=2  # 2 management cycles
    )

    # Print summary
    print("\n" + "="*80)
    print("PROJECT COMPLETE")
    print(team.get_summary())
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
