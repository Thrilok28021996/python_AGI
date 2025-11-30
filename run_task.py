#!/usr/bin/env python3
"""
Simple One-Command Task Executor
Just describe your task and let the system choose the best agents automatically!

Usage:
    python run_task.py "Your task description here"
    python run_task.py "Your task" --llm          # Use AI to select agents (better!)
    python run_task.py "Your task" --llm mistral  # Specify which AI model

    Or run interactively:
    python run_task.py
"""

import sys
import colorama
from auto_agent_router import auto_solve
from llm_agent_selector import llm_solve

colorama.init(autoreset=True)


def main():
    print(colorama.Fore.CYAN + """
╔═══════════════════════════════════════════════════════════════════════╗
║                     AUTOMATIC TASK EXECUTOR                           ║
║                                                                       ║
║  Describe your task and we'll automatically assign the best agents!  ║
║  Use --llm for AI-powered agent selection (recommended!)             ║
╚═══════════════════════════════════════════════════════════════════════╝
    """ + colorama.Style.RESET_ALL)

    # Parse arguments
    use_llm = False
    llm_model = "mistral:latest"  # Default
    task_parts = []

    for i, arg in enumerate(sys.argv[1:]):
        if arg == "--llm":
            use_llm = True
            # Check if next arg is a model name
            if i + 2 < len(sys.argv) and not sys.argv[i + 2].startswith("--"):
                llm_model = sys.argv[i + 2]
        elif arg.startswith("--"):
            continue
        elif i > 0 and sys.argv[i] == llm_model and use_llm:
            continue  # Skip model name
        else:
            task_parts.append(arg)

    # Get task
    if task_parts:
        task = " ".join(task_parts)
    elif len(sys.argv) > 1 and "--llm" in sys.argv:
        # Interactive with LLM mode
        print(colorama.Fore.YELLOW + f"\n📝 Enter your task (AI will select agents using {llm_model}):" + colorama.Style.RESET_ALL)
        task = input("> ").strip()
        if not task:
            show_examples()
            return
    else:
        # Interactive mode
        print(colorama.Fore.YELLOW + "\n📝 Enter your task (or press Enter for examples):" + colorama.Style.RESET_ALL)
        print(colorama.Fore.CYAN + "💡 Tip: Use --llm flag for AI-powered agent selection!" + colorama.Style.RESET_ALL)
        task = input("> ").strip()

        if not task:
            show_examples()
            return

    # Show selection method
    if use_llm:
        print(colorama.Fore.MAGENTA + f"\n🤖 Using AI ({llm_model}) to select agents..." + colorama.Style.RESET_ALL)
    else:
        print(colorama.Fore.YELLOW + "\n🔍 Using keyword matching to select agents..." + colorama.Style.RESET_ALL)
        print(colorama.Fore.CYAN + "💡 Tip: Use --llm for smarter AI-based selection!" + colorama.Style.RESET_ALL)

    # Execute the task
    print(colorama.Fore.GREEN + f"\n🚀 Processing task...\n" + colorama.Style.RESET_ALL)

    if use_llm:
        result = llm_solve(task, model=llm_model, max_iterations=1, verbose=True)
        agents_used = result['selection']['agents']
        workflow = result['selection']['workflow']
        total_exchanges = len(result['results']) if result['results'] else 0
    else:
        result = auto_solve(task, max_iterations=1, verbose=True)
        agents_used = result['analysis']['recommended_agents']
        workflow = result['analysis']['workflow']
        total_exchanges = len(result['results'])

    print(colorama.Fore.GREEN + "\n\n" + "="*80)
    print("✅ TASK COMPLETED!")
    print("="*80 + colorama.Style.RESET_ALL)

    print(f"\nAgents used: {', '.join(agents_used)}")
    print(f"Workflow: {workflow}")
    print(f"Total exchanges: {total_exchanges}")


def show_examples():
    """Show example tasks"""
    print(colorama.Fore.YELLOW + "\n📚 EXAMPLE TASKS:\n" + colorama.Style.RESET_ALL)

    examples = [
        {
            "title": "Web Development",
            "task": "Build a REST API for user authentication with JWT tokens",
            "agents": "Backend Developer, Security Expert, QA Tester"
        },
        {
            "title": "Full Stack App",
            "task": "Create a task management web app with React frontend and Python backend",
            "agents": "Product Manager, Frontend Dev, Backend Dev, QA, DevOps"
        },
        {
            "title": "Security Audit",
            "task": "Review our authentication system for security vulnerabilities",
            "agents": "Security Expert, Lead Developer"
        },
        {
            "title": "Documentation",
            "task": "Write comprehensive API documentation for our REST endpoints",
            "agents": "Technical Writer, Backend Developer"
        },
        {
            "title": "Architecture Design",
            "task": "Design a scalable microservices architecture for e-commerce",
            "agents": "Lead Developer, DevOps, Security, Backend Dev"
        },
        {
            "title": "Testing Strategy",
            "task": "Create a comprehensive testing plan with unit and integration tests",
            "agents": "QA Tester, Backend Developer, DevOps"
        }
    ]

    for i, example in enumerate(examples, 1):
        print(colorama.Fore.CYAN + f"\n{i}. {example['title']}" + colorama.Style.RESET_ALL)
        print(f"   Task: {example['task']}")
        print(colorama.Fore.GREEN + f"   Auto-selected agents: {example['agents']}" + colorama.Style.RESET_ALL)

    print(colorama.Fore.YELLOW + "\n\n💡 To run an example:" + colorama.Style.RESET_ALL)
    print(f'   python run_task.py "{examples[0]["task"]}"')

    print(colorama.Fore.YELLOW + "\n💡 Or try your own task:" + colorama.Style.RESET_ALL)
    print('   python run_task.py "Your custom task description"')

    print(colorama.Fore.MAGENTA + "\n🤖 NEW: Use AI to select agents (smarter!):" + colorama.Style.RESET_ALL)
    print(f'   python run_task.py "{examples[0]["task"]}" --llm')
    print('   python run_task.py "Your task" --llm mistral')
    print('   python run_task.py "Your task" --llm deepseek-r1')


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(colorama.Fore.YELLOW + "\n\n⚠️  Task cancelled by user" + colorama.Style.RESET_ALL)
        sys.exit(0)
    except Exception as e:
        print(colorama.Fore.RED + f"\n\n❌ Error: {str(e)}" + colorama.Style.RESET_ALL)
        sys.exit(1)
