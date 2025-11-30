"""
Quick Start: Multi-Agent System
A simple example to get you started with multi-agent collaboration
"""

from agent_team import AgentTeam
import colorama


def main():
    print(colorama.Fore.CYAN + """
╔═══════════════════════════════════════════════════════════════════════╗
║                   MULTI-AGENT SYSTEM - QUICK START                    ║
║                                                                       ║
║  This example shows 3 agents working together to build a project:    ║
║  - Product Manager: Defines requirements                             ║
║  - Developer: Implements the solution                                ║
║  - QA Tester: Tests and validates                                    ║
╚═══════════════════════════════════════════════════════════════════════╝
    """ + colorama.Style.RESET_ALL)

    # Step 1: Define your project
    project = """
    Create a simple Python script that:
    - Reads a CSV file of employee data
    - Calculates average salary by department
    - Exports results to a new CSV file
    - Includes error handling for missing files
    """

    print(colorama.Fore.YELLOW + "\n📋 PROJECT TASK:")
    print(project + colorama.Style.RESET_ALL)

    # Step 2: Create your team
    print(colorama.Fore.YELLOW + "\n👥 ASSEMBLING TEAM..." + colorama.Style.RESET_ALL)

    team = AgentTeam({
        "Sarah": "product_manager",
        "Alex": "backend_developer",
        "Jamie": "qa_tester"
    })

    print(colorama.Fore.GREEN + "✓ Team assembled!" + colorama.Style.RESET_ALL)
    print(f"  - Sarah (Product Manager)")
    print(f"  - Alex (Backend Developer)")
    print(f"  - Jamie (QA Tester)")

    # Step 3: Run the workflow
    print(colorama.Fore.YELLOW + "\n🚀 STARTING SEQUENTIAL WORKFLOW...\n" + colorama.Style.RESET_ALL)

    results = team.sequential_workflow(
        task=project,
        agent_order=["Sarah", "Alex", "Jamie"],
        max_iterations=1
    )

    # Step 4: Summary
    print(colorama.Fore.CYAN + "\n" + "="*75)
    print("✓ WORKFLOW COMPLETE!")
    print("="*75 + colorama.Style.RESET_ALL)

    print(f"\n📊 Results:")
    print(f"  - Total exchanges: {len(results)}")
    print(f"  - Agents participated: {len(team.agents)}")

    print(colorama.Fore.GREEN + f"\n✅ Project planning and development complete!")
    print(f"\nNext steps:")
    print(f"  1. Review the agent outputs above")
    print(f"  2. Try modifying the project task")
    print(f"  3. Explore other examples:")
    print(f"     - python example_collaborative.py")
    print(f"     - python example_hierarchical.py")
    print(f"     - python example_custom_workflow.py")
    print(f"\n📖 Read MULTI_AGENT_GUIDE.md for detailed documentation")
    print(colorama.Style.RESET_ALL)


if __name__ == "__main__":
    main()
