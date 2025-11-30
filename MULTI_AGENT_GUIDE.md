# Multi-Agent System Guide

A complete guide to building multi-agent systems where specialized agents work together like a company team.

## 📋 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Quick Start](#quick-start)
- [Agent Types](#agent-types)
- [Workflow Patterns](#workflow-patterns)
- [Using Multiple Ollama Models](#using-multiple-ollama-models)
- [Examples](#examples)
- [Advanced Usage](#advanced-usage)
- [Best Practices](#best-practices)

## 🎯 Overview

This multi-agent system allows you to create teams of AI agents that work together on projects, just like a real software development company. Each agent has:

- **Specialized role** (CEO, Developer, Tester, etc.)
- **Domain expertise** (Python, Security, UI Design, etc.)
- **Unique personality** based on their role
- **Ability to use different Ollama models**

### Key Features

✅ **10+ Pre-built Agent Types** (CEO, Developer, QA, DevOps, etc.)
✅ **3 Workflow Patterns** (Sequential, Collaborative, Hierarchical)
✅ **Multi-Model Support** (Different agents can use different Ollama models)
✅ **Flexible Architecture** (Easy to create custom workflows)
✅ **Production Ready** (Error handling, logging, conversation history)

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      AgentTeam                              │
│  (Coordinates multiple agents working together)             │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ manages
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                  SpecializedAgent                           │
│  - Role (CEO, Developer, etc.)                              │
│  - Expertise (Python, Security, etc.)                       │
│  - Ollama Model (llama3.2, codellama, etc.)                │
│  - Conversation History                                     │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ uses
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    ChatOllama                               │
│  (LangChain Ollama integration)                             │
└─────────────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Ensure Ollama is Running

```bash
ollama list
# Should show llama3.2 or other models
```

### 3. Run Your First Multi-Agent Project

```python
from agent_team import AgentTeam

# Create a team
team_config = {
    "Alice": "ceo",
    "Bob": "backend_developer",
    "Charlie": "qa_tester"
}

team = AgentTeam(team_config)

# Run a simple workflow
results = team.sequential_workflow(
    task="Build a simple REST API for user management",
    agent_order=["Alice", "Bob", "Charlie"],
    max_iterations=1
)
```

### 4. Try the Examples

```bash
# Sequential workflow (pipeline)
python example_sequential.py

# Collaborative workflow (discussion)
python example_collaborative.py

# Hierarchical workflow (manager + team)
python example_hierarchical.py

# Custom workflows
python example_custom_workflow.py
```

## 👥 Agent Types

### Available Roles

| Role | Expertise | Best For | Temperature |
|------|-----------|----------|-------------|
| **CEO** | Strategic Planning, Decision Making | High-level direction | 0.7 |
| **Product Manager** | Requirements, User Stories | Feature planning | 0.7 |
| **Lead Developer** | Architecture, Code Review | Technical leadership | 0.5 |
| **Backend Developer** | Python, APIs, Databases | Server-side code | 0.4 |
| **Frontend Developer** | React, JavaScript, CSS | UI implementation | 0.5 |
| **QA Tester** | Testing, Quality Assurance | Finding bugs | 0.6 |
| **DevOps Engineer** | CI/CD, Infrastructure | Deployment | 0.5 |
| **UI/UX Designer** | Design, Wireframes | Visual design | 0.8 |
| **Security Expert** | Security Audits | Vulnerability analysis | 0.3 |
| **Technical Writer** | Documentation | Writing docs | 0.6 |

### Creating Agents

```python
from specialized_agent import create_agent

# Method 1: Use factory function
agent = create_agent("backend_developer", "Bob")

# Method 2: Create custom agent
from specialized_agent import SpecializedAgent

agent = SpecializedAgent(
    role="Backend Developer",
    name="Bob",
    expertise=["Python", "FastAPI", "PostgreSQL"],
    model_name="llama3.2",
    temperature=0.4
)
```

## 🔄 Workflow Patterns

### 1. Sequential Workflow (Pipeline)

Agents work one after another, like an assembly line.

**Use Case:** Development pipeline where each specialist completes their part

```python
team.sequential_workflow(
    task="Build a REST API",
    agent_order=["product_manager", "developer", "tester", "devops"],
    max_iterations=1
)
```

**Flow:**
```
Product Manager → Developer → Tester → DevOps
     ↓               ↓          ↓         ↓
Requirements    Implementation Tests  Deployment
```

### 2. Collaborative Workflow (Discussion)

Multiple agents discuss together to reach consensus.

**Use Case:** Architecture decisions, design discussions

```python
team.collaborative_workflow(
    task="Design a scalable chat system",
    agents=["lead_dev", "backend_dev", "devops", "security"],
    max_rounds=3
)
```

**Flow:**
```
Round 1: All agents share initial thoughts
Round 2: Agents respond to each other
Round 3: Reach consensus
```

### 3. Hierarchical Workflow (Manager + Team)

A manager directs team members.

**Use Case:** Complete project development with oversight

```python
team.hierarchical_workflow(
    task="Build e-commerce website",
    manager="ceo",
    team=["backend_dev", "frontend_dev", "designer", "qa"],
    max_iterations=2
)
```

**Flow:**
```
CEO assigns tasks
     ↓
Team members work
     ↓
CEO reviews
     ↓
Team revises (if needed)
```

## 🤖 Using Multiple Ollama Models

### Model Assignment

Different agents can use different Ollama models based on their needs:

```python
from multi_model_config import MODEL_ASSIGNMENTS, print_model_assignments

# View current assignments
print_model_assignments()

# Update a specific role to use a different model
from multi_model_config import update_model_assignment

update_model_assignment("backend_developer", "codellama", 0.3)
```

### Recommended Models

**For Coding Tasks:**
- `codellama` - Best for code generation
- `llama3.2` - Good general purpose

**For Analysis:**
- `mixtral` - Complex reasoning
- `llama3.2` - Balanced performance

**For Creative Tasks:**
- `neural-chat` - Conversational and creative
- `llama3.2` with higher temperature

**For Speed:**
- `phi` - Fast responses
- Smaller models for simple tasks

### Installing Additional Models

```bash
# Code-focused model
ollama pull codellama

# Advanced reasoning
ollama pull mixtral

# Fast and efficient
ollama pull phi

# Check what's installed
ollama list
```

### Mixing Models in a Team

```python
from specialized_agent import SpecializedAgent

team = {
    "Alice": SpecializedAgent("CEO", "Alice", ["Strategy"], "llama3.2", 0.7),
    "Bob": SpecializedAgent("Backend Developer", "Bob", ["Python"], "codellama", 0.3),
    "Charlie": SpecializedAgent("Designer", "Charlie", ["UI/UX"], "neural-chat", 0.8)
}
```

## 📚 Examples

### Example 1: Build a Web App

```python
from agent_team import AgentTeam

team = AgentTeam({
    "PM": "product_manager",
    "Backend": "backend_developer",
    "Frontend": "frontend_developer",
    "Designer": "designer",
    "QA": "qa_tester"
})

# Sequential development
team.sequential_workflow(
    task="Build a todo list web application",
    agent_order=["PM", "Designer", "Backend", "Frontend", "QA"]
)
```

### Example 2: Code Review

```python
# One developer writes, multiple review
from langchain_core.messages import HumanMessage

dev = team.get_agent("Developer")
code = dev.step(HumanMessage(content="Write authentication code"))

# Parallel reviews
reviewers = ["Lead", "Security", "QA"]
for reviewer_name in reviewers:
    reviewer = team.get_agent(reviewer_name)
    review = reviewer.step(HumanMessage(content=f"Review: {code.content}"))
    print(review.content)
```

### Example 3: Sprint Planning

```python
team.hierarchical_workflow(
    task="Plan sprint with 5 user stories",
    manager="product_manager",
    team=["backend_dev", "frontend_dev", "designer"]
)
```

## 🔧 Advanced Usage

### Custom Agent Roles

Create your own specialized agent:

```python
from specialized_agent import SpecializedAgent

data_scientist = SpecializedAgent(
    role="Data Scientist",
    name="Dr. Smith",
    expertise=["Machine Learning", "Statistics", "Python", "TensorFlow"],
    model_name="llama3.2",
    temperature=0.5
)
```

### Custom Workflows

Mix and match different patterns:

```python
from agent_team import AgentTeam
from langchain_core.messages import HumanMessage

team = AgentTeam({...})

# Phase 1: Collaborative planning
team.collaborative_workflow(
    task="Design architecture",
    agents=["lead_dev", "devops"],
    max_rounds=2
)

# Phase 2: Sequential implementation
team.sequential_workflow(
    task="Implement the plan",
    agent_order=["backend", "frontend", "qa"]
)

# Phase 3: Manager review
ceo = team.get_agent("CEO")
review = ceo.step(HumanMessage(content="Review all work and approve"))
```

### Conversation History

```python
# Access agent's conversation history
agent = team.get_agent("Developer")
print(f"Messages: {len(agent.stored_messages)}")

# Reset specific agent
agent.reset()

# Reset all agents
team.reset_all()
```

### Error Handling

```python
try:
    results = team.sequential_workflow(...)
except RuntimeError as e:
    print(f"Agent failed: {e}")
    # Handle gracefully
```

## ✅ Best Practices

### 1. Choose the Right Workflow

- **Sequential:** Linear tasks with clear dependencies
- **Collaborative:** Need consensus or multiple perspectives
- **Hierarchical:** Complex projects needing coordination

### 2. Assign Appropriate Models

- **Coding tasks:** Use `codellama` if available
- **Security analysis:** Use low temperature (0.3)
- **Creative tasks:** Use higher temperature (0.7-0.8)
- **Production:** Pin model versions in config

### 3. Manage Context

- Reset agents between unrelated tasks
- Limit conversation history for long workflows
- Use clear, specific task descriptions

### 4. Team Composition

- **Small teams (2-3 agents):** Faster, more focused
- **Large teams (5+ agents):** More comprehensive but slower
- **Balance roles:** Mix strategic, technical, and QA

### 5. Iteration Limits

- **Sequential:** 1-2 iterations usually sufficient
- **Collaborative:** 3-5 rounds for consensus
- **Hierarchical:** 2-3 management cycles

### 6. Performance Optimization

```python
# Use smaller models for simple tasks
quick_qa = create_agent("qa_tester", "QuickQA")
# Override with faster model
quick_qa.model = ChatOllama(model="phi", temperature=0.6)

# Parallel execution for independent agents
import concurrent.futures

def run_agent(agent_name, task):
    return team.get_agent(agent_name).step(HumanMessage(content=task))

with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = [
        executor.submit(run_agent, name, task)
        for name in ["Dev1", "Dev2", "Dev3"]
    ]
```

## 🎓 Learning Path

1. **Start Simple:** Run `example_sequential.py`
2. **Try Collaboration:** Run `example_collaborative.py`
3. **Add Management:** Run `example_hierarchical.py`
4. **Experiment:** Modify examples with your own tasks
5. **Build Custom:** Create your own workflows in `example_custom_workflow.py`
6. **Production:** Build a real project with the system

## 🐛 Troubleshooting

### "Model not found"
```bash
ollama list  # Check available models
ollama pull llama3.2  # Install missing model
```

### "Agent not responding"
- Check Ollama is running: `ollama list`
- Verify model name is correct
- Check temperature (too low = repetitive, too high = random)

### "Out of memory"
- Use smaller models (`phi` instead of `mixtral`)
- Reset agents periodically: `team.reset_all()`
- Reduce max_iterations/max_rounds

### "Agents not following instructions"
- Make tasks more specific
- Lower temperature for precision
- Use appropriate role (e.g., `security` for security tasks)

## 🚀 Next Steps

- Explore the source code in `specialized_agent.py` and `agent_team.py`
- Create your own custom agent roles
- Build a real project using the system
- Contribute improvements to the codebase

## 📝 Summary

You now have a complete multi-agent system that can:
- ✅ Create specialized agents with different roles
- ✅ Use different Ollama models for different tasks
- ✅ Run sequential, collaborative, or hierarchical workflows
- ✅ Build custom workflows for specific needs
- ✅ Scale from 2 to 10+ agents working together

Start with the examples and build amazing things! 🎉
