# Python AGI - Complete Tutorial

**A comprehensive guide to building multi-agent AI systems with Ollama**

---

## Table of Contents

1. [Introduction](#introduction)
2. [Architecture Overview](#architecture-overview)
3. [System Components](#system-components)
4. [Core Concepts](#core-concepts)
5. [Installation & Setup](#installation--setup)
6. [Quick Start Guide](#quick-start-guide)
7. [Advanced Features](#advanced-features)
8. [Code Reference](#code-reference)
9. [Best Practices](#best-practices)
10. [Troubleshooting](#troubleshooting)

---

## Introduction

### What is Python AGI?

Python AGI is a multi-agent system that simulates a software development company with specialized AI agents working together to solve complex tasks. Each agent has specific expertise (Backend Developer, QA Tester, Security Expert, etc.) and uses different Ollama models optimized for their role.

### Key Features

✅ **10+ Specialized Agent Types** - CEO, Product Manager, Developers, QA, DevOps, etc.
✅ **3 Workflow Patterns** - Sequential, Collaborative, Hierarchical
✅ **File-Aware Agents** - Create, read, and modify actual code files
✅ **Smart Auto-Stop** - Automatically detects when projects are complete
✅ **LLM-Powered Agent Selection** - AI chooses the best team for your task
✅ **Multiple Ollama Models** - Each agent uses the optimal model
✅ **No API Keys Required** - Everything runs locally with Ollama

---

## Architecture Overview

### System Layers

```
┌─────────────────────────────────────────────────────────────┐
│                     USER INTERFACE LAYER                     │
│   run_task.py  │  build_project.py  │  CLI Commands         │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                   COORDINATION LAYER                         │
│  auto_agent_router.py  │  llm_agent_selector.py             │
│  agent_team.py         │  file_aware_agent.py               │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                      AGENT LAYER                             │
│  specialized_agent.py  │  AGENT_CONFIGS                     │
│  camelagent.py        │  user_prompt.py                     │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                    INFRASTRUCTURE LAYER                      │
│  multi_model_config.py  │  LangChain  │  Ollama             │
└─────────────────────────────────────────────────────────────┘
```

### Three Main Systems

1. **Original CAMEL System** (`camel.py`)
   - Two agents collaborate on tasks
   - Perfect for learning agent interaction

2. **Multi-Agent Company** (`agent_team.py`)
   - 10+ specialized agents
   - Multiple workflow patterns
   - Team coordination

3. **File-Aware Project Builder** (`file_aware_agent.py`)
   - Agents create real code files
   - Iterative improvement cycles
   - Like Claude Code but with multiple agents

---

## System Components

### 1. Core Files

#### `specialized_agent.py`
**Purpose:** Base agent implementation with role specialization

**Key Classes:**
- `SpecializedAgent` - Main agent class with expertise and model assignment

**Agent Types:**
- CEO, Product Manager, Lead Developer
- Backend/Frontend Developers
- QA Tester, DevOps Engineer
- UI/UX Designer, Security Expert
- Technical Writer

#### `agent_team.py`
**Purpose:** Coordinate multiple agents in workflows

**Workflows:**
- `sequential_workflow()` - Agents work one after another
- `collaborative_workflow()` - All agents discuss together
- `hierarchical_workflow()` - Manager directs team

#### `file_aware_agent.py`
**Purpose:** Agents that work with actual files

**Key Classes:**
- `FileManager` - Handles file operations (create, read, update)
- `FileAwareAgent` - Agent that can manipulate files
- `create_project_workflow()` - Complete project building workflow

### 2. Selection Systems

#### `auto_agent_router.py`
**Purpose:** Keyword-based agent selection

**How it works:**
1. Analyzes task description for keywords
2. Scores agents based on keyword matches
3. Selects best agents and workflow
4. Fast but simple

#### `llm_agent_selector.py`
**Purpose:** AI-powered agent selection

**How it works:**
1. Uses Mistral/DeepSeek to analyze task
2. Intelligently selects optimal team
3. Chooses best workflow pattern
4. Slower but much smarter

### 3. User Interfaces

#### `run_task.py`
**Purpose:** Quick task execution

**Usage:**
```bash
python run_task.py "Your task description"
python run_task.py "Your task" --llm
```

#### `build_project.py`
**Purpose:** Build complete projects with files

**Usage:**
```bash
python build_project.py "Create a REST API" --llm
python build_project.py "Task" --iterations 5 --no-auto-stop
```

### 4. Configuration

#### `multi_model_config.py`
**Purpose:** Model assignments for each agent type

Maps agent roles to optimal Ollama models:
- Code tasks → qwen2.5-coder
- Strategy → mistral
- Analysis → deepseek-r1
- Fast tasks → phi3

---

## Core Concepts

### 1. Agent Specialization

Each agent has:
- **Role** - Their job title (Backend Developer, QA Tester, etc.)
- **Expertise** - Specific skills (["Python", "FastAPI", "Databases"])
- **Model** - Optimal Ollama model for their work
- **Temperature** - Creativity level (0.2-0.8)

Example:
```python
backend_dev = SpecializedAgent(
    role="Backend Developer",
    name="Alice",
    expertise=["Python", "FastAPI", "Databases"],
    model_name="qwen2.5-coder:latest",
    temperature=0.3  # Low for deterministic code
)
```

### 2. Workflow Patterns

**Sequential (Pipeline):**
```
PM → Developer → QA → DevOps
```
Each agent builds on previous work. Like an assembly line.

**Collaborative (Discussion):**
```
All agents discuss → Reach consensus
```
Agents share ideas and debate solutions.

**Hierarchical (Management):**
```
Manager assigns → Team executes → Manager reviews
```
CEO/Manager coordinates and makes final decisions.

### 3. File Operations

Agents use special syntax to work with files:

**Create file:**
````
```filename: src/main.py
def hello():
    print("Hello World")
```
````

**Update file:**
````
```update: src/main.py
def hello(name):
    print(f"Hello {name}")
```
````

**Read file:**
````
```read: src/main.py```
````

### 4. Smart Completion Detection

System automatically stops when agents agree project is complete:

1. Agents signal completion in their responses
2. System tracks completion signals
3. If 70%+ agree, stops early
4. Saves time on simple tasks

---

## Installation & Setup

### Prerequisites

1. **Install Ollama**
   ```bash
   # macOS
   brew install ollama

   # Or download from https://ollama.ai
   ```

2. **Pull Models**
   ```bash
   ollama pull llama3.2
   ollama pull qwen2.5-coder
   ollama pull mistral
   ollama pull deepseek-r1
   ```

3. **Verify Ollama**
   ```bash
   ollama list
   # Should show installed models
   ```

### Install Python Dependencies

1. **Create Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Mac/Linux
   # or
   venv\Scripts\activate     # Windows
   ```

2. **Install Requirements**
   ```bash
   pip install -r requirements.txt
   ```

### Environment Configuration (Optional)

```bash
cp example.env .env
# Edit .env if needed
```

---

## Quick Start Guide

### Level 1: Simple Task Execution

**Run a quick task with automatic agent selection:**

```bash
python run_task.py "Build a REST API for user management"
```

**With AI selection (better):**
```bash
python run_task.py "Build a REST API for user management" --llm
```

### Level 2: Build Real Projects

**Create a complete project with actual code files:**

```bash
python build_project.py "Create a FastAPI REST API for a blog" --llm
```

**Result:** Complete project in `./generated_projects/` with:
- Python files
- Tests
- Requirements.txt
- README.md
- All working code!

### Level 3: Manual Team Building

**Create a custom team:**

```python
from agent_team import AgentTeam

team = AgentTeam({
    "Alice": "product_manager",
    "Bob": "backend_developer",
    "Charlie": "qa_tester"
})

team.sequential_workflow(
    task="Build user authentication API",
    agent_order=["Alice", "Bob", "Charlie"]
)
```

### Level 4: Original CAMEL System

**Two agents collaborating:**

```bash
python camel.py
```

Edit the `task` variable in `camel.py` to change what they work on.

---

## Advanced Features

### 1. Custom Agent Selection

**Specify exact agents:**
```bash
python build_project.py "Task" \
  --agents backend_developer frontend_developer qa_tester \
  --iterations 3
```

### 2. Control Iterations

**Set maximum iterations:**
```bash
python build_project.py "Task" --iterations 10
```

**Auto-stop when complete:**
```bash
python build_project.py "Task" --iterations 10 --min-iterations 2
# Will stop early if agents agree it's done
```

**Force all iterations:**
```bash
python build_project.py "Task" --iterations 5 --no-auto-stop
# Always runs all 5 iterations
```

### 3. Custom Model Selection

**Edit `multi_model_config.py`:**
```python
MODEL_ASSIGNMENTS = {
    "backend_developer": {
        "model": "codellama:latest",  # Change this
        "temperature": 0.3
    }
}
```

### 4. Custom Workflows

**Create complex patterns:**
```python
# Planning phase
result1 = team.collaborative_workflow(
    task="Design system architecture",
    agents=["Lead Dev", "Backend", "Frontend", "DevOps"]
)

# Implementation phase
result2 = team.sequential_workflow(
    task=f"Implement: {result1}",
    agent_order=["Backend", "Frontend"]
)

# Review phase
result3 = team.hierarchical_workflow(
    task=f"Review and approve: {result2}",
    manager="Lead Dev",
    team=["Security", "QA"]
)
```

---

## Code Reference

### Key Functions

#### `run_task.py`
```python
# Automatic task execution
auto_solve(task, max_iterations=1, verbose=True)
llm_solve(task, model="mistral:latest", max_iterations=1, verbose=True)
```

#### `build_project.py`
```python
# Build complete project
create_project_workflow(
    project_name="my_api",
    task="Create REST API",
    agents=[{"type": "backend_developer", "name": "Alice"}],
    output_dir="./generated_projects",
    max_iterations=5,
    stop_on_complete=True,
    min_iterations=2
)
```

#### `agent_team.py`
```python
# Create team
team = AgentTeam({
    "Alice": "backend_developer",
    "Bob": "qa_tester"
})

# Run workflows
team.sequential_workflow(task, agent_order)
team.collaborative_workflow(task, agents)
team.hierarchical_workflow(task, manager, team)
```

### Agent Configuration

```python
AGENT_CONFIGS = {
    "agent_type": {
        "role": "Job Title",
        "expertise": ["Skill 1", "Skill 2"],
        "model": "ollama_model_name",
        "temperature": 0.0-1.0
    }
}
```

---

## Best Practices

### 1. Task Descriptions

**Good:**
```
"Create a REST API for user management with CRUD operations,
authentication using JWT, and proper error handling"
```

**Bad:**
```
"Make an API"
```

### 2. Agent Selection

- Use `--llm` for complex tasks (AI selects best team)
- Manually select for simple, specific tasks
- Include QA Tester for production code
- Include Security Expert for auth/payment features

### 3. Iteration Strategy

- Simple tasks: 2-3 iterations
- Medium tasks: 3-5 iterations
- Complex tasks: 5-10 iterations
- Use auto-stop to save time

### 4. Model Selection

- **Code generation**: qwen2.5-coder, codellama
- **Strategy/Planning**: mistral, llama3.2
- **Deep analysis**: deepseek-r1
- **Fast responses**: phi3

---

## Troubleshooting

### Ollama Not Running

```bash
# Check if Ollama is running
ollama list

# If not, start Ollama
# macOS: Should auto-start
# Linux: systemctl start ollama
```

### Model Not Found

```bash
# Pull the missing model
ollama pull model_name

# Example:
ollama pull qwen2.5-coder
```

### Import Errors

```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Agents Not Following Format

- Check prompts in `user_prompt.py` and `assistant_prompt.py`
- Ensure agents have clear format requirements
- Try different models (some follow instructions better)

### Files Not Being Created

- Check `./generated_projects/` directory
- Verify write permissions
- Review agent responses in output

---

## Example Use Cases

### 1. REST API Development
```bash
python build_project.py "Create FastAPI REST API for task management" --llm
```

### 2. Full-Stack Application
```bash
python build_project.py "Build todo app with React frontend and FastAPI backend" \
  --llm --iterations 6
```

### 3. Security Audit
```bash
python run_task.py "Review authentication system for security vulnerabilities" --llm
```

### 4. Documentation
```bash
python run_task.py "Write comprehensive API documentation" \
  --agents tech_writer backend_developer
```

### 5. Architecture Design
```bash
python run_task.py "Design microservices architecture for e-commerce platform" \
  --llm
```

---

## Next Steps

1. **Try the Quick Start examples** - Get familiar with basic usage
2. **Read the specialized guides**:
   - [MULTI_AGENT_GUIDE.md](MULTI_AGENT_GUIDE.md) - Multi-agent systems
   - [PROJECT_BUILDER_GUIDE.md](PROJECT_BUILDER_GUIDE.md) - File-aware agents
   - [AUTO_ROUTER_GUIDE.md](AUTO_ROUTER_GUIDE.md) - Agent selection
3. **Experiment with workflows** - Try different agent combinations
4. **Build real projects** - Use for actual development tasks
5. **Customize agents** - Add your own agent types and models

---

## Summary

**Python AGI** gives you:
- Multiple specialized AI agents working as a team
- Real code file generation and iteration
- Smart agent selection and workflow coordination
- Local execution with Ollama (no API keys)

**Get started in 3 commands:**
```bash
ollama pull llama3.2
pip install -r requirements.txt
python build_project.py "Your project idea" --llm
```

Happy coding! 🚀
