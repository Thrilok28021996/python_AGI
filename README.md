# Python AGI

Build intelligent multi-agent systems where specialized AI agents work together like a real company team.

## 🚀 New to Python AGI? Start Here!

👉 **Read the [COMPLETE_TUTORIAL.md](COMPLETE_TUTORIAL.md)** for a comprehensive guide covering installation, usage, and all features.

**Quick 3-Step Start:**
```bash
ollama pull llama3.2                          # 1. Get AI model
pip install -r requirements.txt               # 2. Install dependencies
python build_project.py "Your idea" --llm     # 3. Build a project!
```

---

## 🎯 What's Inside

This project includes two powerful agent systems:

### 1. **CAMEL Agent System** (Original)
Two agents collaborate on tasks through structured dialogue - perfect for learning agent interaction patterns.

### 2. **Multi-Agent Company System** (New! ⭐)
Build complete "AI companies" with specialized roles:
- 10+ pre-built agent types (CEO, Developer, QA, Designer, etc.)
- 3 workflow patterns (Sequential, Collaborative, Hierarchical)
- Support for multiple Ollama models
- Production-ready architecture

## Prerequisites

1. Install [Ollama](https://ollama.ai) on your system
2. Pull the llama3.2 model:
   ```bash
   ollama pull llama3.2
   ```
3. Verify Ollama is running:
   ```bash
   ollama list
   ```

## Install the necessary packages

Create an environment using anaconda or python venv and then run the below command:

```bash
pip install -r requirements.txt
```

**Note:** This project uses Ollama (local LLM), not OpenAI. No API keys required for basic usage.

---

## 🚀 Quick Start

### ⭐ NEW: Build Real Projects with Code Files! (Like Claude Code!)

**Agents create actual code files, analyze them, and improve iteratively!**

```bash
# One command creates a complete project with real files!
python build_project.py "Create a REST API for user management" --llm

# Result: Complete project with actual Python files, tests, README, etc.
# Saved to: ./generated_projects/your_project/
```

**Features:**
- ✅ Agents create real code files (not just text)
- ✅ Multiple improvement iterations
- ✅ Smart auto-stop when project is complete
- ✅ Code review and bug fixes
- ✅ Complete working projects
- ✅ Just like Claude Code, but with multiple specialist agents!

**Read the guide:** [PROJECT_BUILDER_GUIDE.md](PROJECT_BUILDER_GUIDE.md)

---

### 🌟 Auto-Agent Router (Quick Tasks)

**Just describe your task - agents are selected automatically!**

```bash
# One command - that's it!
python run_task.py "Build a REST API for user management"

# With AI selection (smarter!)
python run_task.py "Create a secure authentication system" --llm
```

The system automatically:
- ✅ Analyzes your task
- ✅ Selects the best agents
- ✅ Chooses optimal workflow
- ✅ Executes and returns results

**Read the guide:** [AUTO_ROUTER_GUIDE.md](AUTO_ROUTER_GUIDE.md)

### Option 1: Multi-Agent System (Manual Selection)

Build a team of specialized agents working together:

```bash
# Quick start with 3 agents
python quick_start_multi_agent.py

# Try different workflows
python example_sequential.py      # Pipeline workflow
python example_collaborative.py   # Team discussion
python example_hierarchical.py    # Manager + team
python example_custom_workflow.py # Advanced patterns
```

**Read the complete guide:** [MULTI_AGENT_GUIDE.md](MULTI_AGENT_GUIDE.md)

### Option 2: Original CAMEL Agent

Two agents collaborating on a task:

```bash
python camel.py
```

To customize the task, edit the `task` variable in `camel.py`.

---

## 📚 Multi-Agent System Overview

### Available Agent Roles

- **CEO** - Strategic planning and decision making
- **Product Manager** - Requirements and user stories
- **Lead Developer** - Architecture and technical leadership
- **Backend Developer** - Server-side implementation
- **Frontend Developer** - UI implementation
- **QA Tester** - Testing and quality assurance
- **DevOps Engineer** - Deployment and infrastructure
- **UI/UX Designer** - Design and user experience
- **Security Expert** - Security audits and best practices
- **Technical Writer** - Documentation

### Workflow Patterns

**1. Sequential (Pipeline)**
```
Product Manager → Developer → QA → DevOps
```
Agents work one after another like an assembly line.

**2. Collaborative (Discussion)**
```
All agents discuss together → Reach consensus
```
Multiple agents discuss to find the best solution.

**3. Hierarchical (Management)**
```
CEO/Manager assigns → Team executes → Manager reviews
```
Manager directs and coordinates team members.

### Simple Example

```python
from agent_team import AgentTeam

# Create your team
team = AgentTeam({
    "Alice": "product_manager",
    "Bob": "backend_developer",
    "Charlie": "qa_tester"
})

# Run a workflow
team.sequential_workflow(
    task="Build a REST API for user management",
    agent_order=["Alice", "Bob", "Charlie"]
)
```

### Using Different Ollama Models

Different agents can use different models:

```python
from specialized_agent import SpecializedAgent

# Backend dev uses CodeLlama (if installed)
backend = SpecializedAgent(
    role="Backend Developer",
    name="Bob",
    expertise=["Python", "FastAPI"],
    model_name="codellama",  # Specialized code model
    temperature=0.3
)

# Designer uses higher creativity
designer = SpecializedAgent(
    role="UI/UX Designer",
    name="Alice",
    expertise=["UI Design", "UX"],
    model_name="llama3.2",
    temperature=0.8  # More creative
)
```

Install additional models:
```bash
ollama pull codellama  # For coding tasks
ollama pull mixtral    # For complex reasoning
ollama pull phi        # For fast responses
```

---

## 📖 Documentation

### 📚 Essential Reading

- **[DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md)** - 🆕 **Navigate all documentation** - Find what you need fast!
- **[COMPLETE_TUTORIAL.md](COMPLETE_TUTORIAL.md)** - 🆕 **START HERE!** Complete tutorial covering everything
- **[CODE_REVIEW_REPORT.md](CODE_REVIEW_REPORT.md)** - 🆕 Comprehensive code quality analysis
- **[CODEBASE_SUMMARY.md](CODEBASE_SUMMARY.md)** - 🆕 Complete codebase overview

### Feature-Specific Guides

- **[MULTI_AGENT_GUIDE.md](MULTI_AGENT_GUIDE.md)** - Complete multi-agent system guide
- **[PROJECT_BUILDER_GUIDE.md](PROJECT_BUILDER_GUIDE.md)** - File-aware project builder guide
- **[AUTO_ROUTER_GUIDE.md](AUTO_ROUTER_GUIDE.md)** - Agent selection guide
- **[LLM_SELECTION_GUIDE.md](LLM_SELECTION_GUIDE.md)** - 🆕 **Which LLM for which agent** - Model selection guide
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - System architecture overview

### Code Reference

- **[specialized_agent.py](specialized_agent.py)** - Agent implementation
- **[agent_team.py](agent_team.py)** - Team coordination
- **[multi_model_config.py](multi_model_config.py)** - Model configuration

---

## 🎓 Examples Included

| Example | Description | Agents | Pattern |
|---------|-------------|--------|---------|
| `quick_start_multi_agent.py` | Simple 3-agent project | 3 | Sequential |
| `example_sequential.py` | Development pipeline | 5 | Sequential |
| `example_collaborative.py` | Architecture discussion | 4 | Collaborative |
| `example_hierarchical.py` | CEO managing team | 5 | Hierarchical |
| `example_custom_workflow.py` | Code review & sprint planning | Various | Custom |
| `camel.py` | Original CAMEL agents | 2 | CAMEL |

---

## 🛠️ Configuration

### Using Different Models

Edit `multi_model_config.py` to assign different models to roles:

```python
MODEL_ASSIGNMENTS = {
    "backend_developer": {
        "model": "codellama",  # Change this
        "temperature": 0.3
    },
    # ... more roles
}
```

### Environment Variables (Optional)

```bash
cp example.env .env
# Edit .env to customize OLLAMA_MODEL or OLLAMA_BASE_URL
```

---

## 🎯 Use Cases

- **Software Development:** Complete projects with specialized dev team
- **Code Review:** Multiple experts review code simultaneously
- **Sprint Planning:** PM and team plan and estimate work
- **Architecture Design:** Team discusses and decides on architecture
- **Documentation:** Generate comprehensive project docs
- **Quality Assurance:** Systematic testing and bug finding
- **Learning:** Understand how AI agents can collaborate

---

## 🤝 Contributing

Feel free to:
- Add new agent roles
- Create new workflow patterns
- Improve existing examples
- Add support for more Ollama models

---

## 📝 License

This project is for educational and research purposes.

---

## 🚦 Getting Started Checklist

- [ ] Install Ollama
- [ ] Pull llama3.2 model (`ollama pull llama3.2`)
- [ ] Install Python dependencies (`pip install -r requirements.txt`)
- [ ] Run quick start (`python quick_start_multi_agent.py`)
- [ ] Read [MULTI_AGENT_GUIDE.md](MULTI_AGENT_GUIDE.md)
- [ ] Try the examples
- [ ] Build your own multi-agent project!

**Questions?** Check the [troubleshooting section](MULTI_AGENT_GUIDE.md#troubleshooting) in the guide.