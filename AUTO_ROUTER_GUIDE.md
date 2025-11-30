# Auto-Agent Router Guide

## 🎯 One Command to Rule Them All!

The Auto-Agent Router automatically selects the best agents for your task. Just describe what you want, and it intelligently assigns the right specialists!

---

## 🚀 Quick Start

### Method 1: Simple Command Line (Easiest!)

```bash
python run_task.py "Build a REST API for user management"
```

That's it! The system will:
1. ✅ Analyze your task
2. ✅ Select the best agents automatically
3. ✅ Choose the optimal workflow
4. ✅ Execute and return results

### Method 2: Interactive Mode

```bash
python run_task.py
```

Then enter your task when prompted, or press Enter to see examples.

### Method 3: In Python Code

```python
from auto_agent_router import auto_solve

# One line - that's all you need!
result = auto_solve("Create a secure authentication system")
```

---

## 📊 How It Works

### 1. Task Analysis

The router analyzes your task description for keywords:

```
Task: "Build a REST API with authentication and deploy to AWS"

Keywords detected:
- "api", "rest" → Backend Developer
- "authentication" → Security Expert
- "deploy", "AWS" → DevOps Engineer

Selected: Backend Developer, Security Expert, DevOps
```

### 2. Workflow Selection

Based on task type and number of agents:

| Agents | Task Type | Workflow |
|--------|-----------|----------|
| 1 agent | Any | Single Agent |
| 2-3 agents | Development | Sequential |
| 2-3 agents | Planning | Collaborative |
| 4+ agents | Development | Sequential |
| 4+ agents | With CEO/PM | Hierarchical |

### 3. Agent Ordering

Agents are ordered in logical workflow sequence:

```
CEO → Product Manager → Designer → Lead Dev → Backend Dev →
Frontend Dev → DevOps → QA → Security → Tech Writer
```

Only the agents needed for your task are included.

---

## 📚 Examples

### Example 1: Web Application Development

```bash
python run_task.py "Build a todo list web app with React frontend and Python backend"
```

**Auto-selected agents:**
- Product Manager (defines features)
- Frontend Developer (React UI)
- Backend Developer (Python API)
- QA Tester (tests everything)

**Workflow:** Sequential

---

### Example 2: Security Audit

```bash
python run_task.py "Review our authentication code for security vulnerabilities"
```

**Auto-selected agents:**
- Security Expert (security analysis)
- Lead Developer (code review)

**Workflow:** Collaborative

---

### Example 3: Full Project

```bash
python run_task.py "Design and implement a scalable e-commerce platform with payment integration, admin panel, and CI/CD pipeline"
```

**Auto-selected agents:**
- CEO (project direction)
- Product Manager (requirements)
- Lead Developer (architecture)
- Backend Developer (implementation)
- Frontend Developer (UI)
- Security Expert (payment security)
- DevOps (CI/CD)
- QA Tester (quality assurance)

**Workflow:** Hierarchical (CEO manages team)

---

### Example 4: Documentation

```bash
python run_task.py "Write comprehensive API documentation with examples"
```

**Auto-selected agents:**
- Technical Writer (documentation)
- Backend Developer (API details)

**Workflow:** Sequential

---

## 🎯 Task Type Detection

The router automatically detects task types:

| Type | Keywords | Example |
|------|----------|---------|
| **Development** | build, create, implement, code | "Build a REST API" |
| **Planning** | plan, design, architect, strategy | "Design system architecture" |
| **Review** | review, audit, analyze, assess | "Review code for bugs" |
| **Documentation** | document, explain, guide | "Write user manual" |
| **Testing** | test, verify, validate | "Test authentication flow" |
| **Deployment** | deploy, launch, release | "Deploy to production" |

---

## 🔑 Keyword Reference

### Agent Selection Keywords

**CEO:**
- strategy, decision, approve, budget, roadmap, vision, goal

**Product Manager:**
- requirements, features, user story, specification, backlog, sprint

**Lead Developer:**
- architecture, design pattern, system design, scalability, framework

**Backend Developer:**
- api, rest, database, server, backend, python, fastapi, sql

**Frontend Developer:**
- ui, frontend, react, vue, javascript, css, component, website

**QA Tester:**
- test, testing, quality, qa, bug, validation, verify, unit test

**DevOps:**
- deploy, deployment, ci/cd, docker, kubernetes, cloud, aws, pipeline

**Designer:**
- design, ui/ux, wireframe, mockup, prototype, layout, visual

**Security:**
- security, secure, encryption, authentication, vulnerability, audit

**Technical Writer:**
- documentation, docs, readme, guide, tutorial, manual, api docs

---

## 💡 Advanced Usage

### Control Workflow Iterations

```python
from auto_agent_router import auto_solve

# More iterations for complex tasks
result = auto_solve(
    "Build complex microservices architecture",
    max_iterations=3,      # For sequential/hierarchical
    max_rounds=5           # For collaborative
)
```

### Access Individual Components

```python
from auto_agent_router import TaskRouter

router = TaskRouter()

# Just analyze, don't execute
analysis = router.analyze_task("Build a REST API")

print(f"Recommended agents: {analysis['recommended_agents']}")
print(f"Workflow type: {analysis['workflow']}")
print(f"Task type: {analysis['task_type']}")
```

### Custom Team After Analysis

```python
router = TaskRouter()
analysis = router.analyze_task("Your task here")

# Modify the agent selection
custom_agents = analysis['recommended_agents'][:3]  # Only first 3

# Execute with custom selection
result = router.auto_execute("Your task", verbose=True)
```

---

## 📝 Writing Good Task Descriptions

### ✅ Good Task Descriptions

```python
# Specific, includes relevant keywords
"Build a REST API for user authentication with JWT tokens and PostgreSQL database"

# Mentions technologies and requirements
"Create a React dashboard with real-time updates using WebSockets"

# Clear about what needs to be done
"Review the payment processing code for security vulnerabilities and PCI compliance"
```

### ❌ Poor Task Descriptions

```python
# Too vague
"Make something"

# No context
"Fix it"

# Unclear requirements
"Do the thing we discussed"
```

**Tip:** Include specific technologies, actions, and requirements in your task description!

---

## 🎓 Tips for Best Results

### 1. Be Specific About Technologies

```python
# Good
"Build a FastAPI backend with PostgreSQL"

# Better
"Build a FastAPI REST API with PostgreSQL database, JWT authentication, and Docker deployment"
```

### 2. Mention All Aspects

```python
# Include everything needed
"Design, implement, test, and deploy a user management system"
# This will select: Product Manager, Developer, QA, DevOps
```

### 3. Use Industry Terms

```python
# Use standard terminology
"Implement CI/CD pipeline"  # Will select DevOps
"Add authentication"        # Will select Security Expert
"Write unit tests"          # Will select QA Tester
```

---

## 🔍 How Agent Selection Works

### Scoring System

Each agent gets a score based on keyword matches:

```python
Task: "Build a secure REST API with authentication and tests"

Scores:
- backend_developer: 2 points (api, rest)
- security: 2 points (secure, authentication)
- qa_tester: 1 point (tests)

Selected agents: [backend_developer, security, qa_tester]
Ordered by: workflow sequence
```

### Minimum Threshold

- Agents need at least 1 keyword match to be selected
- If no keywords match, defaults to: Product Manager, Backend Developer, QA Tester

---

## 🚦 Workflow Decision Logic

```
if agents == 1:
    → Single Agent

elif task_type == "development" and agents >= 3:
    → Sequential (pipeline)

elif task_type in ["planning", "review"] and agents >= 2:
    → Collaborative (discussion)

elif agents >= 4:
    → Hierarchical (managed)

else:
    → Sequential (default)
```

---

## 📊 Output Structure

```python
result = auto_solve("Your task")

# Access different parts
result['analysis']  # Task analysis details
result['results']   # Agent responses
result['team']      # AgentTeam instance

# Analysis contains
result['analysis']['agents']              # All matched agents with scores
result['analysis']['task_type']           # Detected task type
result['analysis']['workflow']            # Selected workflow
result['analysis']['recommended_agents']  # Ordered agent list
```

---

## 🎯 Real-World Examples

### Startup MVP

```bash
python run_task.py "Build an MVP for a food delivery app with user registration, restaurant listings, order placement, and payment integration"
```

**Selects:** Product Manager, Backend Dev, Frontend Dev, Security, QA

---

### Code Review

```bash
python run_task.py "Review this authentication system for security issues and suggest improvements"
```

**Selects:** Security Expert, Lead Developer

---

### Documentation Sprint

```bash
python run_task.py "Create complete documentation including README, API docs, user guide, and deployment instructions"
```

**Selects:** Technical Writer, Backend Dev, DevOps

---

### Infrastructure Setup

```bash
python run_task.py "Set up Kubernetes cluster with monitoring, logging, and CI/CD pipeline"
```

**Selects:** DevOps, Lead Developer

---

## 🔧 Customization

### Add Custom Agent Keywords

Edit `auto_agent_router.py`:

```python
AGENT_KEYWORDS = {
    "data_scientist": [
        "machine learning", "ml", "data analysis", "prediction",
        "model", "training", "dataset"
    ],
    # ... other agents
}
```

### Add Custom Task Patterns

```python
TASK_PATTERNS = {
    "data_science": ["analyze", "predict", "model", "train"],
    # ... other patterns
}
```

---

## ⚡ Performance Tips

1. **Short Tasks:** Use fewer iterations
   ```python
   auto_solve(task, max_iterations=1)
   ```

2. **Complex Projects:** Allow more rounds
   ```python
   auto_solve(task, max_iterations=3, max_rounds=5)
   ```

3. **Quick Validation:** Disable verbose mode
   ```python
   auto_solve(task, verbose=False)
   ```

---

## 🎉 Summary

### One-Line Usage

```bash
# That's all you need!
python run_task.py "Your task description"
```

### Or in Python

```python
from auto_agent_router import auto_solve
result = auto_solve("Your task")
```

### What Happens Automatically

1. ✅ Task is analyzed for keywords
2. ✅ Best agents are selected
3. ✅ Optimal workflow is chosen
4. ✅ Agents are ordered logically
5. ✅ Task is executed
6. ✅ Results are returned

**No manual configuration needed!** 🚀

---

## 📖 See Also

- [MULTI_AGENT_GUIDE.md](MULTI_AGENT_GUIDE.md) - Complete multi-agent system guide
- [MODEL_OPTIMIZATION_SUMMARY.md](MODEL_OPTIMIZATION_SUMMARY.md) - Model assignments
- [README.md](README.md) - Main documentation

---

**Ready to try it?**

```bash
python run_task.py "Build a REST API for a blog with user authentication"
```

Watch as the perfect team is assembled automatically! 🎯
