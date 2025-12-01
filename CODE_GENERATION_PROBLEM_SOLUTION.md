# Code Generation Problem & Solutions

**Issue:** Agents discuss what to build but don't actually write code

**Status:** ✅ **FIXED!** (as of 2025-11-30)

---

## 🎉 Fixed in Latest Version

The collaborative workflow has been updated to enforce code generation:

**✅ What Was Fixed:**
1. Developer agents now receive explicit code requirements in their system messages
2. Collaborative workflow prompts now demand code from developers
3. Added validation function that checks if developers produced code
4. Warning messages displayed when developers don't provide code

**📁 Files Modified:**
- `agent_team.py` - Lines 174-187 (collaborative workflow prompt)
- `agent_team.py` - Lines 348-371 (code validation function)
- `agent_team.py` - Lines 153-155 (validation check)
- `specialized_agent.py` - Lines 54-73 (developer system message)

---

## 🐛 Problem Description

### What's Happening

When using collaborative workflows with developer agents, you get:
- ✅ Good discussions about what to build
- ✅ Ideas and suggestions
- ✅ Architecture proposals
- ❌ **NO ACTUAL CODE**

### Example Output
```
Backend Developer: "We should implement a REST API with FastAPI..."
Frontend Developer: "I agree, and we'll use React for the UI..."
Lead Developer: "Good idea, let's make sure to include authentication..."

Result: ❌ No code files created, just discussions
```

### Why This Happens

**Root Causes:**

1. **Prompts Encourage Discussion**
   - Current: "Based on the discussion above, provide your next input"
   - Agents think they should continue discussing

2. **No Code Requirement Enforcement**
   - Prompts say "write code" but don't enforce it
   - Agents can complete task by just talking

3. **Wrong Workflow Choice**
   - Collaborative = Good for planning
   - Collaborative = Bad for code generation

4. **No Output Validation**
   - System doesn't check if code was produced
   - Agents get credit for discussion alone

---

## ✅ Solutions

### Solution 1: Use Sequential Workflow for Code Generation ⭐ BEST

**Why Sequential Works Better:**
- Each agent **must produce** before next agent starts
- Clear handoff of artifacts (code)
- No discussion loops
- Natural development flow

**Example:**
```python
from agent_team import AgentTeam

team = AgentTeam({
    "PM": "product_manager",
    "Backend": "backend_developer",
    "Frontend": "frontend_developer",
    "QA": "qa_tester"
})

# Use SEQUENTIAL for code generation
result = team.sequential_workflow(
    task="Build a REST API for user management with CRUD operations",
    agent_order=["PM", "Backend", "Frontend", "QA"]
)
```

**What Happens:**
1. PM creates requirements → **actual document**
2. Backend receives requirements → **writes API code**
3. Frontend receives API → **writes UI code**
4. QA receives code → **writes tests**

**Result:** ✅ Real code at each step

---

### Solution 2: Use File-Aware Agents for Real Projects ⭐ BEST

**Why File-Aware Works:**
- Agents **must** create actual files
- System validates files are created
- Iterative improvement cycles
- Like Claude Code but with multiple agents

**Example:**
```bash
python build_project.py "Create REST API for user management" --llm
```

**What Happens:**
1. Agents selected automatically
2. Each agent creates real `.py` files
3. Files saved to `./generated_projects/`
4. Code can be run immediately

**Result:** ✅ Complete working project with actual files

---

### Solution 3: Enforce Code in Collaborative Workflow

**Modify collaborative workflow prompts to require code:**

**File:** `agent_team.py` line 174

**Current (causes discussions):**
```python
context_parts.append("\nBased on the discussion above, provide your next input:")
```

**Better (enforces code):**
```python
if "developer" in agent.role.lower():
    context_parts.append("""
\nBased on the discussion above, you MUST now provide:
1. Actual working code (not pseudocode)
2. Code wrapped in ```language blocks
3. Explanations of your code

DO NOT just discuss - WRITE THE CODE.
""")
else:
    context_parts.append("\nBased on the discussion above, provide your next input:")
```

**Result:** ✅ Developers write code, others can still discuss

---

### Solution 4: Add Code Validation

**Check if developers produced code:**

```python
def validate_developer_output(agent_role: str, response: str) -> bool:
    """Check if developer agent produced actual code"""
    if "developer" not in agent_role.lower():
        return True  # Non-developers don't need code

    # Check for code blocks
    has_code_blocks = "```" in response
    has_substantial_code = response.count("\n") > 10  # More than just comments

    return has_code_blocks and has_substantial_code

# In collaborative_workflow:
response = agent.step(message)

if not validate_developer_output(agent.role, response.content):
    print(f"⚠️ {agent.name} didn't provide code. Prompting again...")
    # Re-prompt with stronger requirement
```

**Result:** ✅ System catches and corrects discussion-only responses

---

### Solution 5: Update Agent System Messages

**Make developer agents know they MUST code:**

**File:** `specialized_agent.py` system message

**Add to developer prompts:**

```python
if "developer" in self.role.lower():
    content += """

CRITICAL REQUIREMENT FOR DEVELOPERS:
- You MUST write actual, working code in EVERY response
- Use proper code blocks: ```python, ```javascript, etc.
- Provide complete, runnable code (not pseudocode)
- Include comments explaining your code
- If discussing: keep it brief, then WRITE CODE

DO NOT just talk about code - WRITE IT!
"""
```

**Result:** ✅ Developers know their primary job is coding, not discussing

---

## 🎯 Recommended Approach

### For Different Use Cases

| Use Case | Best Solution | Why |
|----------|---------------|-----|
| **Build complete project** | File-Aware Agents (`build_project.py`) | Creates real files, iterative |
| **Generate code** | Sequential Workflow | Forces actual production |
| **Planning only** | Collaborative Workflow | Discussion is appropriate |
| **Code review** | Hierarchical Workflow | Manager reviews real code |
| **Quick prototypes** | Sequential with 2-3 agents | Fast, produces code |

### Quick Decision Tree

```
Do you need actual code files?
├─ YES → Use build_project.py (File-Aware Agents)
│
└─ NO, just code snippets?
   ├─ Multiple steps → Sequential Workflow
   └─ Discussion needed → Collaborative (but expect discussions)
```

---

## 📝 Implementation Guide

### Step 1: Choose Right Tool

**For Real Projects (Recommended):**
```bash
# This ALWAYS produces actual code files
python build_project.py "Your project idea" --llm --iterations 3
```

**For Code Snippets:**
```python
# Use sequential workflow
team.sequential_workflow(
    task="Implement user authentication",
    agent_order=["backend_developer", "qa_tester"]
)
```

### Step 2: If Using Collaborative, Modify Prompts

**Edit:** `agent_team.py` line 174

**Add code enforcement:**
```python
# After line 173
developer_agents = [a for a in agents if "developer" in self.get_agent(a).role.lower()]

if developer_agents:
    context_parts.append("""
\n⚠️ DEVELOPERS: You must provide actual code in ```language blocks.
Based on the discussion above, write the code now:
""")
else:
    context_parts.append("\nBased on the discussion above, provide your next input:")
```

### Step 3: Validate Output

**Add validation after agent responds:**
```python
# After line 151
response = agent.step(message)

# Validate if developer
if "developer" in agent.role.lower():
    if "```" not in response.content:
        print(f"⚠️ {agent.name} didn't provide code blocks!")
        # Could re-prompt here
```

### Step 4: Use Correct Temperature

**Code generation needs LOW temperature:**

**Edit:** `multi_model_config.py`

```python
MODEL_ASSIGNMENTS = {
    "backend_developer": {
        "model": "qwen2.5-coder:latest",
        "temperature": 0.2,  # ← LOW for deterministic code
    },
    "product_manager": {
        "model": "llama3.2",
        "temperature": 0.6,  # ← MEDIUM for balanced discussion
    }
}
```

---

## 🔧 Quick Fixes

### Fix 1: Force Code in Next Iteration

**Immediate solution without code changes:**

When running collaborative workflow, **add explicit code requirement** to task:

**Before:**
```python
task = "Build a REST API"
```

**After:**
```python
task = """Build a REST API

REQUIREMENTS FOR DEVELOPERS:
- Provide COMPLETE, WORKING code in ```python blocks
- Include all imports
- Add comments
- Make it runnable
- NO pseudocode or outlines
"""
```

### Fix 2: Use Fewer Rounds

**Collaborative workflows with many rounds = more discussion**

**Change:**
```python
# Instead of:
team.collaborative_workflow(task, agents, max_rounds=5)

# Do:
team.collaborative_workflow(task, agents, max_rounds=1)
```

**Result:** Less time to discuss, more pressure to produce

### Fix 3: Remove Non-Developers from Code Tasks

**For code generation, ONLY include developers:**

**Before:**
```python
agents = ["product_manager", "backend_developer", "frontend_developer", "tech_writer"]
```

**After:**
```python
agents = ["backend_developer", "frontend_developer"]  # Only coders
```

**Result:** No one to discuss with, must write code

---

## 🎓 Best Practices

### DO ✅

1. **Use file-aware agents for projects**
   ```bash
   python build_project.py "Your idea" --llm
   ```

2. **Use sequential for code generation**
   ```python
   team.sequential_workflow(task, ["backend", "frontend", "qa"])
   ```

3. **Be specific in task descriptions**
   ```python
   task = "Write a FastAPI endpoint for /users/create with POST method,
           validation, and database insert. Include complete code."
   ```

4. **Use low temperature for developers**
   ```python
   temperature = 0.2-0.3  # Deterministic code
   ```

5. **Validate code was produced**
   ```python
   if "```" not in response:
       print("No code produced!")
   ```

### DON'T ❌

1. **Don't use collaborative for code generation**
   - Collaborative = discussions
   - Sequential = production

2. **Don't mix many roles in code tasks**
   - Keep to developers + QA
   - Remove PM, designers for code phase

3. **Don't use high temperatures for code**
   - 0.7+ = creative but inconsistent
   - 0.2-0.3 = reliable code

4. **Don't expect code from first collaborative round**
   - First round = planning
   - Use sequential or file-aware instead

5. **Don't skip task specificity**
   - "Build API" = vague → discussions
   - "Write FastAPI POST /users code" = specific → code

---

## 📊 Comparison Table

| Approach | Code Quality | Speed | Real Files | Best For |
|----------|-------------|-------|------------|----------|
| **File-Aware** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ✅ Yes | Complete projects |
| **Sequential** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ❌ No | Code snippets |
| **Collaborative** | ⭐⭐ | ⭐⭐ | ❌ No | Planning/Discussion |
| **Hierarchical** | ⭐⭐⭐ | ⭐⭐⭐ | ❌ No | Code review |

---

## 🚀 Examples

### Example 1: Wrong Way (Discussions Only)

```python
# ❌ This will produce discussions, not code
team.collaborative_workflow(
    task="Build a REST API",
    agents=["product_manager", "backend_developer", "frontend_developer"],
    max_rounds=3
)

# Result: Agents discuss architecture, no code written
```

### Example 2: Right Way (Actual Code)

```python
# ✅ This produces actual code
team.sequential_workflow(
    task="""Write a FastAPI REST API with these endpoints:
    - POST /users (create user)
    - GET /users/{id} (get user)
    - PUT /users/{id} (update user)
    - DELETE /users/{id} (delete user)

    Include: validation, error handling, database models.
    Provide COMPLETE runnable code in Python.""",

    agent_order=["backend_developer", "qa_tester"]
)

# Result: Backend writes API code, QA writes tests
```

### Example 3: Best Way (Real Project)

```bash
# ✅ This creates complete working project with files
python build_project.py \
  "Create a FastAPI REST API for user management with CRUD operations.
   Include SQLite database, Pydantic models, and error handling." \
  --llm \
  --iterations 3

# Result: Complete project in ./generated_projects/ with:
# - main.py (FastAPI app)
# - models.py (Pydantic models)
# - database.py (DB connection)
# - requirements.txt
# - README.md
# - tests/
```

---

## 🔍 Debugging

### How to Check if Agents Produced Code

**After workflow completes:**

```python
result = team.sequential_workflow(task, agent_order)

# Check each response
for response in result:
    agent_name = response['agent']
    content = response['response']

    has_code = "```" in content
    print(f"{agent_name}: {'✅ Has code' if has_code else '❌ No code'}")
```

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Only discussions | Using collaborative workflow | Use sequential or file-aware |
| Pseudocode only | Not specific enough in task | Add "complete runnable code" to task |
| Incomplete code | High temperature | Lower to 0.2-0.3 |
| No files created | Not using file-aware agents | Use build_project.py |
| Code stops mid-function | Model context limit | Use smaller models or split task |

---

## 📖 Summary

### The Core Problem

**Collaborative workflows encourage discussion over production.**

### The Solutions

1. **Best:** Use file-aware agents (`build_project.py`)
2. **Good:** Use sequential workflow for code
3. **Fix:** Modify collaborative prompts to enforce code
4. **Validate:** Check that developers actually produced code

### Quick Action

**If you want code RIGHT NOW:**

```bash
# Use this command - it ALWAYS produces code files:
python build_project.py "Your project description" --llm --iterations 3

# Result: Working code in ./generated_projects/
```

**If you want code snippets:**

```python
# Use sequential workflow with ONLY developers:
team.sequential_workflow(
    task="Very specific code task with 'write complete code' instruction",
    agent_order=["backend_developer"]  # Just one developer
)
```

---

## 🎯 Action Items

### For Codebase Maintainers

1. ☐ Update `agent_team.py` collaborative workflow prompt (line 174)
2. ☐ Add code validation function
3. ☐ Update `specialized_agent.py` developer system messages
4. ☐ Document "use sequential for code" in guides
5. ☐ Add examples showing sequential vs collaborative

### For Users

1. ☐ Use `build_project.py` for real projects (recommended)
2. ☐ Use sequential workflow for code generation
3. ☐ Reserve collaborative for planning only
4. ☐ Be very specific in task descriptions
5. ☐ Include "write complete code" in developer tasks

---

**Status:** Problem identified and solutions provided
**Severity:** Medium (affects code generation quality)
**Quick Fix:** Use `build_project.py` or sequential workflow
**Permanent Fix:** Update collaborative workflow prompts

---

**Last Updated:** 2025-11-30
**Related Docs:** MULTI_AGENT_GUIDE.md, PROJECT_BUILDER_GUIDE.md
