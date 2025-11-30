## FILE-AWARE PROJECT BUILDER GUIDE

Build real projects with AI agents that create actual code files, analyze them, and improve iteratively - just like Claude Code!

---

## 🎯 What This Does

Instead of just generating text responses, agents now:
1. ✅ **Create actual code files** in a project directory
2. ✅ **Read and analyze** existing files
3. ✅ **Critique and fix** issues they find
4. ✅ **Iterate multiple times** to improve code quality
5. ✅ **Work as a team** with each agent contributing their expertise

**Result:** A complete, working project with real files you can run!

---

## 🚀 Quick Start

### Simple Command
```bash
python build_project.py "Create a REST API for user management"
```

### With AI Team Selection
```bash
python build_project.py "Create a REST API for user management" --llm
```

### Custom Settings
```bash
python build_project.py "Build a blog website" --llm --iterations 5 --name my_blog
```

### With Auto-Stop (Default)
```bash
# Agents will automatically stop when they agree the project is complete
python build_project.py "Create a REST API" --llm

# Force all iterations even if agents think it's complete
python build_project.py "Create a REST API" --llm --no-auto-stop

# Require minimum 3 iterations before checking completion
python build_project.py "Create a REST API" --llm --min-iterations 3
```

---

## 📚 How It Works

### Phase 1: Initial Creation (Iteration 1)
```
Backend Developer → Creates main.py, models.py, routes.py
QA Tester → Creates tests/test_api.py
DevOps → Creates Dockerfile, requirements.txt
```

### Phase 2: Review & Improve (Iteration 2)
```
Backend Developer → Reads all files, improves error handling
QA Tester → Reviews tests, adds more test cases
Security → Reviews auth code, fixes vulnerabilities
```

### Phase 3: Final Polish (Iteration 3)
```
Backend Developer → Optimizes performance
QA Tester → Ensures 100% test coverage
Tech Writer → Creates README.md with documentation
```

**Output:** Complete project in `./generated_projects/your_project/`

---

## 💡 Usage Examples

### Example 1: REST API Project
```bash
python build_project.py "Create a FastAPI REST API for a blog with user authentication"
```

**Generated files:**
```
generated_projects/create_a_fastapi_rest_api/
├── main.py                 # FastAPI application
├── models.py               # Database models
├── routes/
│   ├── auth.py            # Authentication routes
│   └── posts.py           # Blog post routes
├── requirements.txt        # Dependencies
├── tests/
│   └── test_api.py        # API tests
└── README.md              # Documentation
```

---

### Example 2: Full Stack Web App (with AI selection)
```bash
python build_project.py "Build a todo list app with React and Python" --llm --iterations 4
```

**AI selects:** Product Manager, Backend Dev, Frontend Dev, QA Tester

**Generated files:**
```
generated_projects/todo_list_app/
├── backend/
│   ├── main.py
│   ├── database.py
│   └── models.py
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── components/
│   │   └── api.js
│   └── package.json
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

### Example 3: Specific Team
```bash
python build_project.py "Authentication microservice" \
  --agents backend_developer security qa_tester devops \
  --iterations 3 \
  --name auth_service
```

---

## 🛠️ Command Line Options

| Option | Description | Example |
|--------|-------------|---------|
| `task` | Project description (required) | `"Create a REST API"` |
| `--name` | Custom project name | `--name my_api` |
| `--output` | Output directory | `--output ./my_projects` |
| `--iterations` | Number of improvement cycles (max) | `--iterations 5` |
| `--agents` | Specific agents to use | `--agents backend_developer qa_tester` |
| `--llm` | Use AI to select agents | `--llm` |
| `--no-auto-stop` | Disable auto-stop on completion | `--no-auto-stop` |
| `--min-iterations` | Minimum iterations before checking completion | `--min-iterations 3` |

---

## 🎯 Smart Completion Detection (Auto-Stop)

**NEW FEATURE:** The system automatically detects when agents believe the project is complete and stops early!

### How It Works

1. **Agents Signal Completion**: After minimum iterations, agents can signal when they think the project is done
2. **Consensus Check**: If 70%+ of agents agree the project is complete, the system stops early
3. **Saves Time**: No need to run unnecessary iterations when work is already done

### Example Output

```
════════════════════════════════════════════════════════════════
ITERATION 2/5
════════════════════════════════════════════════════════════════

>>> Backend Dev (Backend Developer) working...

Backend Dev creating/updating files:
  ↻ Updated: main.py
  Updated 1 files
  ✓ Backend Dev signals: Project looks complete

>>> QA Tester (QA Tester) working...

QA Tester creating/updating files:
  ↻ Updated: tests/test_api.py
  Updated 1 files
  ✓ QA Tester signals: Project looks complete

📊 Completion Status: 2/2 agents signal complete (100%)

🎉 Majority of agents agree project is complete!
   Stopping after iteration 2/5
```

### Configuration

```bash
# Default: Auto-stop enabled with minimum 2 iterations
python build_project.py "Task" --llm

# Disable auto-stop (always run all iterations)
python build_project.py "Task" --llm --no-auto-stop

# Require 3 iterations before checking completion
python build_project.py "Task" --llm --min-iterations 3 --iterations 10
```

### Completion Criteria

Agents signal completion when they detect:
- "Project is complete"
- "Task is complete"
- "All requirements met"
- "No further improvements needed"
- "Ready for deployment"
- And many other completion keywords

---

## 🔍 File Format for Agents

Agents create files using this special syntax:

### Creating a New File
````
```filename: src/main.py
def hello():
    print("Hello World!")
```
````

### Updating an Existing File
````
```update: src/main.py
def hello(name):
    print(f"Hello {name}!")
```
````

### Reading a File
````
```read: src/main.py```
````

---

## 🎯 Agent Workflow

### Iteration 1: Creation
Each agent creates their initial files:

**Backend Developer:**
- Creates API endpoints
- Sets up database models
- Implements business logic

**Frontend Developer:**
- Creates React components
- Sets up API calls
- Implements UI

**QA Tester:**
- Creates test files
- Writes test cases

---

### Iteration 2+: Review & Improve
Each agent:
1. Reads ALL existing files
2. Analyzes code quality
3. Finds issues/improvements
4. Updates files with fixes

**Backend Developer might:**
- Add better error handling
- Optimize database queries
- Improve code structure

**QA Tester might:**
- Add missing test cases
- Improve test coverage
- Add integration tests

**Security Expert might:**
- Fix authentication bugs
- Add input validation
- Improve security headers

---

## 📊 Real Example Output

```bash
$ python build_project.py "Create a simple REST API for a todo list" --llm

╔═══════════════════════════════════════════════════════════════════════╗
║              FILE-AWARE PROJECT BUILDER                               ║
╚═══════════════════════════════════════════════════════════════════════╝

📁 Project: create_a_simple_rest_api_for_a_todo_list
📋 Task: Create a simple REST API for a todo list

🤖 Using AI to select optimal agents...

Selected 3 agents: backend_developer, qa_tester, tech_writer
Workflow: sequential

👥 Team: Backend Developer, QA Tester, Tech Writer

════════════════════════════════════════════════════════════════
ITERATION 1/3
════════════════════════════════════════════════════════════════

>>> Backend Developer (Backend Developer) working...

Backend Developer creating/updating files:
  ✓ Created: main.py
  ✓ Created: models.py
  ✓ Created: requirements.txt
  Created 3 files

>>> QA Tester (QA Tester) working...

QA Tester creating/updating files:
  ✓ Created: tests/test_api.py
  Created 1 files

>>> Tech Writer (Technical Writer) working...

Tech Writer creating/updating files:
  ✓ Created: README.md
  Created 1 files

════════════════════════════════════════════════════════════════
ITERATION 2/3
════════════════════════════════════════════════════════════════

>>> Backend Developer (Backend Developer) working...

Backend Developer creating/updating files:
  ↻ Updated: main.py
  ↻ Updated: models.py
  Updated 2 files

>>> QA Tester (QA Tester) working...

QA Tester creating/updating files:
  ↻ Updated: tests/test_api.py
  ✓ Created: tests/conftest.py
  Updated 1 files, Created 1 files

... [iteration 3] ...

════════════════════════════════════════════════════════════════
✅ PROJECT COMPLETE!
════════════════════════════════════════════════════════════════

📁 Project created at: ./generated_projects/create_a_simple_rest_api_for_a_todo_list

Project Structure:
  ├── main.py
  ├── models.py
  ├── requirements.txt
  ├── README.md
  ├── tests
  │   ├── test_api.py
  │   └── conftest.py

📊 Total files created: 6
```

---

## 🎓 Advanced Usage

### Custom Project Structure
```bash
python build_project.py "E-commerce API with payment integration" \
  --llm \
  --iterations 4 \
  --output ./production_projects \
  --name shop_api
```

### Microservices Architecture
```bash
python build_project.py "Microservices system with API gateway, auth service, and user service" \
  --agents lead_developer backend_developer backend_developer devops \
  --iterations 5
```

### Complete Full-Stack App
```bash
python build_project.py "Full-stack social media app with posts, comments, likes" \
  --llm \
  --iterations 6
```

---

## 📂 Project Output Structure

All projects are saved to `./generated_projects/` by default:

```
generated_projects/
├── my_api/
│   ├── main.py
│   ├── models.py
│   ├── tests/
│   └── README.md
├── my_webapp/
│   ├── backend/
│   ├── frontend/
│   └── docker-compose.yml
└── another_project/
    └── ...
```

Each project is self-contained and ready to run!

---

## 🔧 How Agents Collaborate

### Example: Todo API Project

**Backend Developer (Iteration 1):**
```python
# Creates: main.py
from fastapi import FastAPI
app = FastAPI()

@app.get("/todos")
def get_todos():
    return []  # Simple implementation
```

**QA Tester (Iteration 1):**
```python
# Creates: tests/test_api.py
def test_get_todos():
    # Found issue: No proper response model
    pass
```

**Backend Developer (Iteration 2):**
Reads QA's test, sees the issue, updates:
```python
# Updates: main.py
from pydantic import BaseModel

class Todo(BaseModel):
    id: int
    title: str
    completed: bool

@app.get("/todos", response_model=List[Todo])
def get_todos():
    return []  # Now with proper typing!
```

**QA Tester (Iteration 2):**
```python
# Updates: tests/test_api.py
def test_get_todos():
    response = client.get("/todos")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
```

This continues for each iteration, improving quality!

---

## ✨ Key Benefits

### 1. Real, Runnable Code
- Not just text responses
- Actual files you can execute
- Complete project structure

### 2. Iterative Improvement
- Agents review each other's work
- Code gets better each iteration
- Issues are found and fixed automatically

### 3. Team Collaboration
- Each agent focuses on their expertise
- Backend, Frontend, QA, DevOps all contribute
- Realistic development workflow

### 4. Quality Assurance
- QA Tester writes actual tests
- Security Expert reviews for vulnerabilities
- Code is validated through multiple passes

---

## 🎯 Best Practices

### 1. Start with Clear Requirements
```bash
# Good
python build_project.py "REST API for book library with CRUD operations, user auth, and search"

# Too Vague
python build_project.py "Make an API"
```

### 2. Use Enough Iterations
- **1-2 iterations:** Basic implementation
- **3-4 iterations:** Good quality, reviewed code
- **5-6 iterations:** Production-ready with docs and tests

### 3. Let AI Select Team for Complex Projects
```bash
# For complex projects, use --llm
python build_project.py "Full microservices e-commerce platform" --llm --iterations 5
```

### 4. Review Generated Code
Always review the generated code before using in production!

---

## 🚀 Quick Reference

```bash
# Basic project
python build_project.py "Your project description"

# With AI team selection
python build_project.py "Your project" --llm

# Custom iterations and name
python build_project.py "Your project" --iterations 5 --name my_proj

# Specific team
python build_project.py "Your project" --agents backend_developer qa_tester

# Full control
python build_project.py "Your project" --llm --iterations 6 --name prod_app --output ./production
```

---

## 📖 Comparison to Claude Code

| Feature | Claude Code | Our System |
|---------|------------|------------|
| Creates real files | ✅ | ✅ |
| Reads existing files | ✅ | ✅ |
| Iterative improvement | ✅ | ✅ |
| Multiple specialists | ❌ | ✅ (Multiple agents!) |
| Automatic team selection | ❌ | ✅ (with --llm) |
| Reviews and critiques | ✅ | ✅ |
| Auto-fixes issues | ✅ | ✅ |

**Advantage:** Multiple specialized agents working together!

---

## 🎉 Summary

### What You Can Do:

```bash
# Create a complete project
python build_project.py "REST API for user management" --llm

# Result: Real, working code in ./generated_projects/
```

### What Happens:
1. ✅ AI selects best team
2. ✅ Agents create initial files
3. ✅ Agents review each other's code
4. ✅ Issues are found and fixed
5. ✅ Code improves each iteration
6. ✅ Final project is production-ready

### Get Started:
```bash
python build_project.py "Your amazing project idea here" --llm
```

**That's it!** Your agents will build it with real, working code files! 🚀
