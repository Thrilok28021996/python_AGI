"""
Example: Sequential Workflow
Agents work one after another, like a pipeline

Use case: Development workflow where each specialist completes their part
"""

from agent_team import AgentTeam


def main():
    # Define the project
    project_task = """
    Build a REST API for a task management system with the following features:
    - User authentication (JWT)
    - CRUD operations for tasks
    - Task categories and tags
    - Due dates and priorities
    - SQLite database
    """

    # Create a team with different specialists
    team_config = {
        "Sarah": "product_manager",    # Defines requirements
        "Mike": "lead_developer",       # Designs architecture
        "Alex": "backend_developer",    # Implements the API
        "Emma": "qa_tester",            # Tests the implementation
        "David": "devops"               # Sets up deployment
    }

    # Initialize the team
    team = AgentTeam(team_config)

    # Define the workflow order
    workflow_order = ["Sarah", "Mike", "Alex", "Emma", "David"]

    print("\n" + "="*80)
    print("SEQUENTIAL WORKFLOW EXAMPLE")
    print("Each agent completes their work before passing to the next")
    print("="*80 + "\n")

    # Run the sequential workflow
    results = team.sequential_workflow(
        task=project_task,
        agent_order=workflow_order,
        max_iterations=1  # One pass through the pipeline
    )

    # Print summary
    print("\n" + "="*80)
    print("WORKFLOW COMPLETE")
    print(team.get_summary())
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
