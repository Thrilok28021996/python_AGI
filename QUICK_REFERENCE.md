# Quick Reference Guide - AI Company System

## 🚀 Quick Start

```bash
# Build a simple project
python build_project.py "Create a REST API for todo management"

# Build with specific options
python build_project.py "Build a web app" --iterations 5 --tdd

# Build complex project (auto-builds large team)
python build_project.py "Build e-commerce platform with React, Node.js, PostgreSQL, payments, auth"
```

---

## 📊 What Features Are Enabled by Default?

| Feature | Status | Disable With |
|---------|--------|--------------|
| Dynamic Team Building | ✅ Enabled | `--no-auto-team` |
| PM Coordination | ✅ Enabled | N/A (always on) |
| Collaborative Review | ✅ Enabled | `--no-collaborative-review` |
| Security Scanning | ✅ Enabled | `--no-security-scan` |
| Automated Testing | ✅ Enabled | `--no-testing` |
| Conflict Resolution | ✅ Enabled | N/A (always on) |
| Auto Documentation | ✅ Enabled | N/A (always on) |
| Performance Analytics | ✅ Enabled | N/A (always on) |
| Task Rewriting | ✅ Enabled | N/A (always on) |

---

## 🏢 How Teams Are Built

### Simple Projects (1-2 agents)
**Example**: "Create a calculator function"
- Backend Developer
- QA Tester

### Medium Projects (3-5 agents)
**Example**: "Build a REST API with auth and database"
- Lead Developer
- Backend Developer
- Security Expert
- QA Tester

### Complex Projects (6-8 agents)
**Example**: "Build e-commerce platform with frontend, backend, database, payments"
- Product Manager
- Lead Developer
- Backend Developer
- Frontend Developer
- Security Expert
- QA Tester
- UI Designer
- Data Scientist (if ML needed)

---

## 🔄 How the Workflow Works

```
1. User provides project description
   ↓
2. Task Rewriter clarifies requirements
   ↓
3. Dynamic Team Builder assigns agents (1-8)
   ↓
4. Project Manager plans Iteration 1
   - Assigns specific tasks to each agent
   - Identifies dependencies
   - Sets priorities
   ↓
5. Agents work on assigned tasks
   - Create/update code files
   - Follow PM's plan
   ↓
6. Performance tracker records contributions
   ↓
7. Collaborative Review (peer feedback)
   - Other agents review code
   - Author addresses feedback
   ↓
8. Conflict Resolution (if needed)
   - Detects disagreements
   - Makes technical decisions
   ↓
9. Automated Testing
   - Runs test suite
   - Reports failures
   ↓
10. Security Scanning
    - Finds vulnerabilities
    - Reports critical issues
    ↓
11. PM plans next iteration (repeat 4-10)
    ↓
12. Documentation Generation
    - Creates README.md
    - Documents tech stack
    ↓
13. Performance Analytics
    - Shows contributions
    - Ranks by quality
    ↓
14. PM Retrospective
    - What went well
    - What to improve
    ↓
15. Project Complete!
```

---

## 📁 Output Structure

After building a project, you'll get:

```
generated_projects/
└── your_project_name/
    ├── README.md                    ← Auto-generated documentation
    ├── main.py                      ← Main application
    ├── requirements.txt             ← Dependencies
    ├── tests/
    │   └── test_main.py            ← Automated tests
    ├── api/                         ← Backend code
    │   └── routes.py
    └── [other project files]
```

Plus in terminal:
- 📊 Test results
- 🔒 Security scan results
- 👥 Collaborative review summary
- 📈 Performance analytics report
- 🔄 PM retrospective

---

## 🎯 Common Use Cases

### 1. Web API
```bash
python build_project.py "Create a REST API for user management with FastAPI, PostgreSQL, JWT auth"
```
**Team**: Lead, Backend, Security, QA (4 agents)

### 2. Full-Stack Web App
```bash
python build_project.py "Build a todo app with React frontend and Python backend"
```
**Team**: PM, Lead, Backend, Frontend, QA, UI (6 agents)

### 3. Machine Learning Project
```bash
python build_project.py "Create a sentiment analysis model with training pipeline and API"
```
**Team**: PM, Lead, Backend, Data Scientist, QA (5 agents)

### 4. CLI Tool
```bash
python build_project.py "Create a command-line tool for file organization"
```
**Team**: Backend, QA (2 agents)

### 5. Microservice
```bash
python build_project.py "Build a payment processing microservice with Stripe integration"
```
**Team**: Lead, Backend, Security, QA (4 agents)

---

## 🛠️ CLI Options

### Basic Options
```bash
--name PROJECT_NAME              # Custom project name
--output ./my_projects           # Output directory
--iterations 5                   # Number of improvement cycles (default: 3)
```

### Team Control
```bash
--auto-team                      # Auto-build team (default: on)
--no-auto-team                   # Use default 3-agent team
--max-team-size 5                # Limit team to 5 agents
--agents backend qa              # Specify exact agents
```

### Feature Toggles
```bash
--collaborative-review           # Enable peer review (default: on)
--no-collaborative-review        # Disable peer review
--security-scan                  # Enable security scan (default: on)
--no-security-scan              # Disable security scan
--tdd                           # Use Test-Driven Development
```

### Testing Options
```bash
--no-testing                     # Disable automated testing
--test-command "pytest -v"       # Custom test command
```

### Advanced Options
```bash
--min-iterations 2               # Minimum iterations before auto-stop
--no-auto-stop                   # Always run all iterations
--show-rewrite                   # Show task rewrite comparison
```

---

## 📊 Understanding the Output

### Performance Report
```
🏆 Top Contributors:
  1. Alice (Backend Developer): 15 contributions
  2. Bob (QA Tester): 8 contributions

⭐ Quality Leaders:
  1. Alice: 9.2/10.0 quality score
  2. Bob: 8.5/10.0 quality score
```

### Test Summary
```
📊 Test Summary:
  Total Tests: 12
  Passed: 12
  Failed: 0
  Success Rate: 100%
```

### Security Results
```
🔒 Security: No vulnerabilities detected
```

### Retrospective
```
✅ What Went Well:
  • All tests passing
  • No security issues
  • Code improved through peer review

❌ What Didn't Go Well:
  • Had some initial test failures

💡 Improvements:
  • Better initial test coverage
```

---

## 🧪 Testing Your Setup

Run the integration test:
```bash
python test_full_integration.py
```

Expected output:
```
🎉 ALL INTEGRATION TESTS PASSED!
This is a complete AI software company! 🏢
```

---

## 🔍 Troubleshooting

### Issue: No agents being assigned
**Solution**: Check that Ollama is running:
```bash
ollama list
```

### Issue: Tests not running
**Solution**: Ensure pytest is installed:
```bash
pip install pytest
```

### Issue: LLM errors
**Solution**: System falls back to rule-based logic automatically. No action needed.

### Issue: Import errors
**Solution**: Ensure all files are in the same directory:
```bash
ls *.py
```

---

## 📚 File Reference

| File | Purpose | Size |
|------|---------|------|
| `build_project.py` | CLI entry point | ~370 lines |
| `file_aware_agent.py` | Main workflow | ~990 lines |
| `project_coordination.py` | PM coordination | ~510 lines |
| `company_enhancements.py` | Conflict/Docs/Analytics | ~589 lines |
| `dynamic_team_builder.py` | Team sizing | ~400 lines |
| `collaborative_review.py` | Peer review | ~300 lines |
| `security_scanner.py` | Vulnerability scan | ~200 lines |
| `test_executor.py` | Automated testing | ~250 lines |
| `tdd_mode.py` | Test-Driven Dev | ~200 lines |
| `specialized_agent.py` | Agent definitions | ~500 lines |
| `task_rewriter.py` | Task clarification | ~200 lines |

---

## 💡 Pro Tips

1. **Start Simple**: Test with a simple project first
2. **Let Auto-Team Work**: The system is smart about team sizing
3. **Trust the Process**: Multiple iterations improve quality
4. **Read the Retrospective**: PM provides valuable insights
5. **Check README**: Auto-generated docs are comprehensive
6. **Review Analytics**: See which agents contributed most

---

## 🎯 What Makes This Different?

### Traditional AI Code Generation:
- ❌ Single agent
- ❌ One-shot generation
- ❌ No review process
- ❌ No testing
- ❌ No documentation
- ❌ No iteration

### This System:
- ✅ Dynamic teams (1-8 agents)
- ✅ Multiple improvement cycles
- ✅ Peer code review
- ✅ Automated testing
- ✅ Security scanning
- ✅ Auto-documentation
- ✅ Performance tracking
- ✅ PM coordination
- ✅ Conflict resolution
- ✅ Continuous improvement

---

## 🚀 Ready to Build!

```bash
# Try it now!
python build_project.py "Your project idea here"
```

The AI company will:
1. Build the right team
2. Plan the work
3. Create the code
4. Review each other
5. Test everything
6. Scan for security
7. Generate docs
8. Track performance
9. Hold retrospective
10. Deliver production-ready code

**Welcome to the future of software development!** 🎉

---

**Last Updated**: 2025-12-02
**Version**: 1.0 (Production)
**Status**: ✅ Fully Operational
