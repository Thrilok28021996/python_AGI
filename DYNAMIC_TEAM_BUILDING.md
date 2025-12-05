# 🏢 Dynamic Team Building - Documentation

## Overview

The system now **automatically builds teams based on project requirements** - just like a real company!

Instead of having a fixed 4-agent team, the system analyzes your project and assembles the right team:
- **Simple calculator**? → 1-2 agents
- **REST API**? → 3-5 agents
- **Full-stack e-commerce app**? → 6-8 agents

---

## 🎯 Why Dynamic Teams?

### The Problem (Before)
```python
# Every project got the same 4 agents:
agents = [Backend Dev, Frontend Dev, QA, DevOps]

# Problems:
- Simple calculator gets 4 agents (overkill!)
- Complex e-commerce app gets 4 agents (not enough!)
- No security expert for auth systems
- No data scientist for ML projects
```

### The Solution (Now)
```python
# Team adapts to project:

"Create a calculator"
→ Team: [Backend Dev] (1 agent)

"Build a todo API"
→ Team: [Lead Dev, Backend Dev, QA] (3 agents)

"Full-stack e-commerce with auth and payments"
→ Team: [Product Manager, Lead Dev, Backend Dev,
        Frontend Dev, Security Expert, QA, UI Designer] (7 agents)
```

---

## 🚀 How It Works

### 1. Project Analysis

The system analyzes your task description to determine:

#### Project Type
- `api` - REST/GraphQL API
- `web_app` - Web application
- `library` - Package/module/SDK
- `ml_model` - Machine learning project
- `mobile_app` - Mobile application
- `data_analysis` - Data analysis project

#### Complexity
- `simple` - Basic scripts, calculators (1-2 agents)
- `medium` - APIs, simple web apps (3-5 agents)
- `complex` - Full-stack apps, microservices (6-8 agents)

#### Requirements
- Requires security? (auth, payments, sensitive data)
- Requires UI? (user-facing application)
- Requires testing? (always true unless prototype)
- Requires data science? (ML, predictions, analysis)

### 2. Team Building

Based on analysis, the system selects optimal agents:

#### Core Team (Always)
- **Lead Developer** - for projects with 3+ agents
- **Product Manager** - for complex projects with 5+ agents

#### Domain Developers
- **Backend Developer** - APIs, servers, databases
- **Frontend Developer** - UI, React, Vue, Angular
- **Mobile Developer** - iOS, Android, React Native

#### Specialists
- **Security Expert** - authentication, payments, sensitive data
- **QA Tester** - testing, quality assurance
- **Data Scientist** - ML models, data analysis
- **DevOps Engineer** - deployment, infrastructure
- **UI Designer** - user interface design

### 3. Smart Scaling

Team size adapts to project complexity:

```
Simple Project (1-2 agents):
- 1 Backend Developer
- 1 QA Tester (if testing required)

Medium Project (3-5 agents):
- 1 Lead Developer
- 1-2 Core Developers (Backend/Frontend)
- 1 QA Tester
- Specialists as needed

Complex Project (6-8 agents):
- 1 Product Manager
- 1 Lead Developer
- 2-3 Core Developers
- 1-2 Specialists (Security, Data Science)
- 1 QA Tester
- Support roles (DevOps, UI Designer)
```

---

## 📝 Examples

### Example 1: Simple Calculator
```bash
python build_project.py "Create a simple calculator library with add, subtract, multiply, divide"
```

**Analysis**:
- Type: `library`
- Complexity: `simple`
- Domains: `backend`, `testing`
- Team size: 2

**Team Built**:
1. Backend Developer
2. QA Tester

---

### Example 2: REST API
```bash
python build_project.py "Create a REST API for managing todos with CRUD operations and PostgreSQL database"
```

**Analysis**:
- Type: `api`
- Complexity: `medium`
- Domains: `backend`, `database`, `testing`
- Team size: 3

**Team Built**:
1. Lead Developer
2. Backend Developer
3. QA Tester

---

### Example 3: Full-Stack E-Commerce
```bash
python build_project.py "Build a complete e-commerce web application with React frontend, Node.js backend, PostgreSQL database, user authentication, payment processing via Stripe, and admin dashboard"
```

**Analysis**:
- Type: `web_app`
- Complexity: `complex`
- Domains: `frontend`, `backend`, `database`, `security`, `testing`
- Requires security: YES (auth + payments)
- Requires UI: YES
- Team size: 7

**Team Built**:
1. Product Manager (project coordinator)
2. Lead Developer (architecture)
3. Backend Developer (API, database)
4. Frontend Developer (React UI)
5. Security Expert (auth, payments)
6. QA Tester (testing)
7. UI Designer (user interface)

---

### Example 4: ML Project
```bash
python build_project.py "Analyze sales data and build predictive ML models for forecasting quarterly revenue"
```

**Analysis**:
- Type: `ml_model`
- Complexity: `medium`
- Domains: `data_science`, `testing`
- Requires data science: YES
- Team size: 3

**Team Built**:
1. Lead Developer
2. Data Scientist
3. QA Tester

---

### Example 5: Mobile App
```bash
python build_project.py "Build a mobile app for iOS with user authentication and real-time chat"
```

**Analysis**:
- Type: `mobile_app`
- Complexity: `medium`
- Domains: `mobile`, `backend`, `security`, `testing`
- Requires security: YES (auth)
- Requires UI: YES
- Team size: 5

**Team Built**:
1. Lead Developer
2. Frontend Developer (mobile)
3. Backend Developer (chat API)
4. Security Expert (authentication)
5. QA Tester

---

## 🎛️ Control Options

### Use Dynamic Team (Default)
```bash
# Automatically builds optimal team
python build_project.py "Create a web app"
```

### Set Maximum Team Size
```bash
# Limit team to max 4 agents (cost/time constraint)
python build_project.py "Build e-commerce app" --max-team-size 4
```

**What happens**: System prioritizes essential roles
1. Keep: Lead Developer, Product Manager
2. Keep: Core developers (Backend/Frontend)
3. Keep: QA if testing required
4. Keep: Critical specialists (Security if auth, Data Scientist if ML)
5. Drop: Support roles (DevOps, UI Designer)

### Disable Dynamic Teams (Manual)
```bash
# Use default 3-agent team
python build_project.py "Create API" --no-auto-team

# Specify exact agents
python build_project.py "Create API" --agents backend_developer qa_tester
```

---

## 🧠 Analysis Methods

### 1. LLM-Based Analysis (Preferred)
Uses AI model to understand nuanced requirements:
```python
"Build a social media app"
→ Understands: needs real-time features, scalability, moderation
→ Adds: Backend Dev, Frontend Dev, Security Expert, QA
```

**Requires**: Ollama running locally

### 2. Rule-Based Analysis (Fallback)
Keyword matching when LLM unavailable:
```python
"Create REST API with authentication"
→ Detects: 'rest api' → backend needed
→ Detects: 'authentication' → security needed
→ Adds: Backend Dev, Security Expert, QA
```

**Always works**: No external dependencies

---

## 📊 Team Composition Rules

### Always Include
- QA Tester (unless explicitly "no testing" or "prototype")
- At least 1 core developer

### Include If Needed
- **Lead Developer**: if 3+ agents total
- **Product Manager**: if 5+ agents total (complex projects)
- **Security Expert**: if keywords like "auth", "login", "payment", "secure"
- **Data Scientist**: if keywords like "ML", "predict", "forecast", "data analysis"
- **UI Designer**: if user-facing app + "design" mentioned
- **DevOps Engineer**: if "deploy", "docker", "kubernetes", "CI/CD"

### Priority Order (When Limiting Team Size)
1. Lead Developer / Product Manager (leadership)
2. Core Developers (Backend, Frontend)
3. QA Tester (if testing required)
4. Critical Specialists (Security for auth, Data Scientist for ML)
5. Support Roles (DevOps, UI Designer)

---

## 🔬 Technical Implementation

### Analysis Flow
```
1. User provides task description
   ↓
2. DynamicTeamBuilder.analyze_project_requirements(task)
   ↓
3. Try LLM analysis (ChatOllama with qwen2.5-coder)
   ├─ Success: detailed, nuanced analysis
   └─ Fail: fallback to rule-based analysis
   ↓
4. Returns analysis dict:
   {
     "project_type": "web_app",
     "complexity": "complex",
     "domains": ["frontend", "backend", "security"],
     "estimated_team_size": 6,
     "requires_security": true,
     "requires_ui": true,
     "requires_testing": true,
     "requires_data_science": false
   }
```

### Team Building Flow
```
1. Based on analysis, start with empty team
   ↓
2. Add core team (Lead Dev, Product Manager if needed)
   ↓
3. Add domain developers (Backend, Frontend)
   ↓
4. Add specialists (Security, Data Scientist, etc.)
   ↓
5. Add QA Tester if testing required
   ↓
6. If max_team_size specified, prioritize and reduce
   ↓
7. Return list of agent configs
```

---

## 🎯 Benefits

### For Users
1. **No manual team selection** - System does it automatically
2. **Right-sized teams** - No overkill or underkill
3. **Cost-effective** - Small projects get small teams
4. **Comprehensive** - Complex projects get full teams
5. **Flexible** - Can override with manual selection

### For Quality
1. **Security expert for sensitive features** - Auth, payments get proper review
2. **Data scientist for ML projects** - Proper expertise for ML
3. **UI designer for user-facing apps** - Better user experience
4. **QA always included** - Quality assurance by default

### For Scalability
1. **Adapts to project size** - 1 agent to 8 agents
2. **Respects constraints** - Can limit team size
3. **Intelligent prioritization** - Keeps essential roles when limiting

---

## 🧪 Testing Results

### Test Case 1: Simple Calculator
```
Input: "Create a simple calculator library"
Output: 2 agents (Backend Dev, QA)
✅ Correct: No overkill for simple project
```

### Test Case 2: REST API
```
Input: "Create a REST API for managing todos"
Output: 3 agents (Lead Dev, Backend Dev, QA)
✅ Correct: Appropriate for medium complexity
```

### Test Case 3: E-Commerce
```
Input: "Complete e-commerce with auth and payments"
Output: 7 agents (PM, Lead, Backend, Frontend, Security, QA, UI)
✅ Correct: Full team for complex project
```

### Test Case 4: ML Project
```
Input: "Build ML models for forecasting"
Output: 3 agents (Lead Dev, Data Scientist, QA)
✅ Correct: Includes Data Scientist specialist
```

---

## 🔧 Integration

### In `build_project.py`
```python
# Default behavior (auto-team enabled)
python build_project.py "Create a web app"
→ Calls analyze_task_and_build_team(task)
→ Returns optimal team

# User override (manual agents)
python build_project.py "Create app" --agents backend:Alice qa:Bob
→ Uses specified agents
→ Skips dynamic team building
```

### Fallback Behavior
```python
1. Try dynamic team building
   ↓
2. If exception → use default team
   [Lead Developer, Backend Developer, QA Tester]
   ↓
3. Always ensure minimum viable team
```

---

## 📚 Keyword Detection

### Project Types
- **API**: "api", "rest", "graphql", "endpoint"
- **Web App**: "web app", "website", "react", "vue", "angular", "frontend"
- **Library**: "library", "package", "module", "sdk"
- **ML Model**: "machine learning", "ml model", "predict", "forecast"
- **Mobile**: "mobile", "ios", "android", "flutter", "react native"

### Complexity
- **Simple**: "simple", "basic", "calculator", "hello world", "script"
- **Complex**: "complete", "full-stack", "e-commerce", "payment", "microservices", "dashboard"

### Security
- **Triggers**: "auth", "login", "password", "payment", "secure", "jwt", "oauth"

### Database
- **Triggers**: "database", "sql", "postgresql", "mongodb", "crud", "store", "persist"

---

## 🎓 Best Practices

### When to Use Dynamic Teams (Default)
```bash
# Let system decide - recommended for most cases
python build_project.py "Your project description here"
```

### When to Use Manual Teams
```bash
# Very specific requirements
python build_project.py "Create API" --agents backend:Alice backend:Bob qa:Charlie

# Testing/development
python build_project.py "Prototype" --agents backend:Dev
```

### When to Limit Team Size
```bash
# Budget constraints
python build_project.py "Build web app" --max-team-size 3

# Time constraints (fewer agents = faster decision-making)
python build_project.py "Quick MVP" --max-team-size 2
```

---

## 🚀 Future Enhancements

### Possible Additions
1. **Dynamic scaling during execution** - Add specialists mid-project if issues found
2. **Team performance tracking** - Learn which team compositions work best
3. **Cost optimization** - Balance team size vs. quality vs. cost
4. **Skill-based matching** - Match specific tech stacks to agent expertise
5. **Inter-team collaboration** - Multiple teams for very large projects

---

## ✅ Summary

### Before
- Fixed 4-agent team for every project
- Manual team selection required
- No adaptation to project needs

### After
- **Dynamic team** building based on requirements
- **1-8 agents** depending on complexity
- **Automatic** specialist assignment
- **Intelligent** role prioritization
- **Fallback** to rule-based when LLM unavailable
- **Like a real company** - right team for the job!

---

**Status**: ✅ Fully Implemented and Tested
**Default**: Enabled for all new projects
**Override**: Available via CLI flags
**Fallback**: Always ensures minimum viable team
