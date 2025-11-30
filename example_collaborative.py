"""
Example: Collaborative Workflow
Multiple agents discuss and iterate together

Use case: Design decisions or architecture planning that needs input from multiple specialists
"""

from agent_team import AgentTeam


def main():
    # Define the project
    project_task = """
    We need to design the architecture for a real-time chat application that supports:
    - 10,000+ concurrent users
    - Private and group chats
    - File sharing
    - Message history
    - End-to-end encryption
    - Mobile and web clients

    Discuss and decide on:
    - Backend technology stack
    - Database choice
    - Real-time communication protocol
    - Scaling strategy
    - Security approach
    """

    # Create a team for collaborative discussion
    team_config = {
        "Lisa": "lead_developer",
        "Tom": "backend_developer",
        "Rachel": "devops",
        "James": "security"
    }

    # Initialize the team
    team = AgentTeam(team_config)

    print("\n" + "="*80)
    print("COLLABORATIVE WORKFLOW EXAMPLE")
    print("Agents discuss together to reach the best solution")
    print("="*80 + "\n")

    # Run collaborative workflow
    results = team.collaborative_workflow(
        task=project_task,
        agents=["Lisa", "Tom", "Rachel", "James"],
        max_rounds=3,  # 3 rounds of discussion
        convergence_check=True
    )

    # Print summary
    print("\n" + "="*80)
    print("DISCUSSION COMPLETE")
    print(team.get_summary())
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
