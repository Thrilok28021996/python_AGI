#!/usr/bin/env python3
"""
Build Project - Create Real Code Files
Uses AI agents to build actual projects with code files that can be analyzed and improved iteratively

Usage:
    python build_project.py "Create a REST API for user management"
    python build_project.py --help
"""

import sys
import argparse
import colorama
from file_aware_agent import create_project_workflow
from llm_agent_selector import LLMAgentSelector

colorama.init(autoreset=True)


def main():
    parser = argparse.ArgumentParser(
        description="Build a real project with AI agents creating actual code files"
    )
    parser.add_argument(
        "task",
        nargs="?",
        help="Project description"
    )
    parser.add_argument(
        "--name",
        default=None,
        help="Project name (default: auto-generated)"
    )
    parser.add_argument(
        "--output",
        default="./generated_projects",
        help="Output directory (default: ./generated_projects)"
    )
    parser.add_argument(
        "--iterations",
        type=int,
        default=3,
        help="Number of improvement cycles (default: 3)"
    )
    parser.add_argument(
        "--agents",
        nargs="+",
        default=None,
        help="Specific agents to use (e.g., backend_developer qa_tester)"
    )
    parser.add_argument(
        "--llm",
        action="store_true",
        help="Use LLM to select agents automatically"
    )
    parser.add_argument(
        "--no-auto-stop",
        action="store_true",
        help="Disable auto-stop (always run all iterations even if agents signal completion)"
    )
    parser.add_argument(
        "--min-iterations",
        type=int,
        default=2,
        help="Minimum iterations before checking for completion (default: 2)"
    )

    args = parser.parse_args()

    # Show header
    print(colorama.Fore.CYAN + """
╔═══════════════════════════════════════════════════════════════════════╗
║                    AI PROJECT BUILDER                                 ║
║                                                                       ║
║  Agents create real code files, analyze them, and improve iteratively║
╚═══════════════════════════════════════════════════════════════════════╝
    """ + colorama.Style.RESET_ALL)

    # Get task description
    if args.task:
        task = args.task
    else:
        print(colorama.Fore.YELLOW + "📝 Describe your project:" + colorama.Style.RESET_ALL)
        task = input("> ").strip()

        if not task:
            print(colorama.Fore.RED + "❌ No project description provided" + colorama.Style.RESET_ALL)
            show_examples()
            return

    # Generate project name if not provided
    if args.name:
        project_name = args.name
    else:
        # Auto-generate from task
        import re
        project_name = re.sub(r'[^a-z0-9]+', '_', task.lower()[:50])
        project_name = project_name.strip('_')

    print(colorama.Fore.CYAN + f"\n📁 Project Name: {project_name}")
    print(f"📋 Description: {task}")
    print(f"🔄 Iterations: {args.iterations}\n" + colorama.Style.RESET_ALL)

    # Select agents
    if args.agents:
        # Use specified agents
        agents = [{"type": agent, "name": agent.capitalize()} for agent in args.agents]
        print(colorama.Fore.YELLOW + f"👥 Using specified agents: {', '.join(args.agents)}\n" + colorama.Style.RESET_ALL)

    elif args.llm:
        # Use LLM to select agents
        print(colorama.Fore.MAGENTA + "🤖 Using AI to select optimal agents...\n" + colorama.Style.RESET_ALL)

        selector = LLMAgentSelector(model_name="mistral:latest")
        selection = selector.select_agents(task, min_agents=2, max_agents=6, verbose=True)

        agents = [
            {"type": agent_type, "name": agent_type.replace("_", " ").title()}
            for agent_type in selection["agents"]
        ]

    else:
        # Default team for development projects
        print(colorama.Fore.YELLOW + "👥 Using default development team\n" + colorama.Style.RESET_ALL)
        agents = [
            {"type": "backend_developer", "name": "Backend Dev"},
            {"type": "qa_tester", "name": "QA Tester"},
        ]

    # Build the project
    print(colorama.Fore.GREEN + "\n🚀 Starting project build...\n" + colorama.Style.RESET_ALL)

    result = create_project_workflow(
        project_name=project_name,
        task=task,
        agents=agents,
        output_dir=args.output,
        max_iterations=args.iterations,
        stop_on_complete=not args.no_auto_stop,
        min_iterations=args.min_iterations
    )

    # Final output
    completion_info = ""
    if result.get('stopped_early'):
        completion_info = f"\n✅ Auto-stopped: Agents agreed project was complete!\n"

    iterations_completed = len(set(op['iteration'] for op in result['operations']))

    print(colorama.Fore.GREEN + f"""

╔═══════════════════════════════════════════════════════════════════════╗
║                     PROJECT BUILD COMPLETE!                           ║
╚═══════════════════════════════════════════════════════════════════════╝

📁 Project Location: {result['project_path']}
📊 Files Created: {len(result['files'])}
🔄 Iterations Completed: {iterations_completed}/{args.iterations}{completion_info}
📂 Project Structure:
{chr(10).join('   ' + f for f in result['files'])}

💡 Next Steps:
   1. Review the generated code in: {result['project_path']}
   2. Test the implementation
   3. Run the project
   4. Iterate further if needed

    """ + colorama.Style.RESET_ALL)


def show_examples():
    """Show example project descriptions"""
    print(colorama.Fore.YELLOW + "\n📚 EXAMPLE PROJECTS:\n" + colorama.Style.RESET_ALL)

    examples = [
        {
            "name": "REST API",
            "cmd": 'python build_project.py "Create a REST API for user management with FastAPI"'
        },
        {
            "name": "Web App",
            "cmd": 'python build_project.py "Build a todo list web app with React frontend and Python backend"'
        },
        {
            "name": "CLI Tool",
            "cmd": 'python build_project.py "Create a command-line tool for file organization"'
        },
        {
            "name": "Microservice",
            "cmd": 'python build_project.py "Build a microservice for authentication with JWT tokens"'
        }
    ]

    for i, example in enumerate(examples, 1):
        print(colorama.Fore.CYAN + f"\n{i}. {example['name']}" + colorama.Style.RESET_ALL)
        print(f"   {example['cmd']}")

    print(colorama.Fore.MAGENTA + "\n\n💡 Pro Tips:" + colorama.Style.RESET_ALL)
    print("   • Use --llm to let AI select the best team")
    print("   • Use --iterations 5 for more refinement")
    print("   • Use --agents backend_developer frontend_developer qa_tester for specific team")
    print("   • Auto-stop is enabled by default - agents will stop when task is complete")
    print("   • Use --no-auto-stop to force all iterations")
    print("   • Use --min-iterations 3 to require minimum iterations before checking completion")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(colorama.Fore.YELLOW + "\n\n⚠️  Build cancelled by user" + colorama.Style.RESET_ALL)
        sys.exit(0)
    except Exception as e:
        print(colorama.Fore.RED + f"\n\n❌ Error: {str(e)}" + colorama.Style.RESET_ALL)
        import traceback
        traceback.print_exc()
        sys.exit(1)
