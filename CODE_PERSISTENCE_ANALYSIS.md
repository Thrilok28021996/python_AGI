# Code Persistence Analysis

**Question:** Is code generated in conversations stored and accessible to agents when they need it?

**Answer:** It depends on which system you're using!

---

## 📊 Summary Table

| System | Code Stored in Memory? | Code Saved to Files? | Agents Can Access? | Best For |
|--------|----------------------|---------------------|-------------------|----------|
| **Collaborative Workflow** | ✅ Yes (in context) | ❌ No | ⚠️ Within same conversation only | Planning & Discussion |
| **Sequential Workflow** | ✅ Yes (in context) | ❌ No | ⚠️ Within same conversation only | Code generation |
| **Hierarchical Workflow** | ✅ Yes (in context) | ❌ No | ⚠️ Within same conversation only | Code review |
| **File-Aware Agents** | ✅ Yes | ✅ **YES - Real files!** | ✅ **Yes - Persistent!** | **Real projects** |

---

## 🔍 Detailed Analysis

### 1. Agent Memory System (All Workflows)

**How It Works:**

```python
class SpecializedAgent:
    def __init__(self):
        self.stored_messages = [self.system_message]  # Agent's memory

    def step(self, input_message):
        messages = self.update_messages(input_message)  # Add to memory
        output_message = self.model.invoke(messages)    # LLM sees full history
        self.update_messages(output_message)            # Store response
        return output_message
```

**What Gets Stored:**
- ✅ System message (role, responsibilities)
- ✅ All input messages received
- ✅ All responses generated
- ✅ **Code blocks in responses** (as part of message content)

**Access Pattern:**
```
Round 1:
  Backend: Writes code → Stored in backend.stored_messages
  Frontend: Can't see backend's code yet

Round 2:
  Context includes: "Backend Developer said: [code]"
  Frontend: Now sees backend's code in context
  Frontend: Can reference/use backend's code
```

**Limitation:** ⚠️ Code is only stored **during the conversation**
- When workflow ends, agent memory persists
- But no files are created
- Code only exists in Python objects

---

### 2. Collaborative Workflow

**File:** `agent_team.py` - `collaborative_workflow()`

**Code Storage:**

```python
# Line 166: Stored in conversation history
self.conversation_history.append(result)

# Line 176: Passed to next round
context_parts.append(f"\n{agent.name} ({agent.role}) said:\n{response}\n")
```

**How Agents Access Previous Code:**

```
Round 1:
├─ Backend writes: ```python code here ```
└─ Stored in: conversation_history + agent.stored_messages

Round 2:
├─ Context built: "Backend Developer said: ```python code ```"
├─ Frontend receives full context
└─ Frontend can see and reference backend's code
```

**Example:**
```python
# Round 1
Backend: "Here's the API: ```python\n@app.post('/users')\ndef create()...\n```"

# Round 2 - Frontend receives:
"""
Backend Developer said:
Here's the API: ```python
@app.post('/users')
def create():
    ...
```

Now create the frontend...
"""

Frontend: "I'll call the /users endpoint: ```javascript\nfetch('/users')...\n```"
```

**✅ Pros:**
- Agents see each other's code within the conversation
- Context grows with each round
- LLM has full history

**❌ Cons:**
- Code NOT saved to actual files
- Lost when Python process ends
- Can't run the code
- Can't import/use across workflows

---

### 3. Sequential Workflow

**File:** `agent_team.py` - `sequential_workflow()`

**Code Storage:**

```python
# Line 93: Each agent receives previous output
message = HumanMessage(content=f"{task}\n\nPrevious work:\n{output}")
```

**How Agents Access Previous Code:**

```
PM → Writes requirements
      ↓ (output passed)
Backend → Sees requirements, writes code
      ↓ (code passed)
QA → Sees code, writes tests
```

**Example:**
```python
# Step 1: PM
PM output: "Requirements: User registration with email/password"

# Step 2: Backend (receives PM output)
Input: "Requirements: User registration..."
Backend output: "```python\nclass User:\n    email: str..."

# Step 3: QA (receives Backend output)
Input: "```python\nclass User:..."
QA output: "```python\ndef test_user_creation()..."
```

**✅ Pros:**
- Each agent builds on previous work
- Clear pipeline
- Previous code always included

**❌ Cons:**
- Still no file creation
- Code only in memory
- Lost after workflow ends

---

### 4. File-Aware Agents ⭐ **BEST FOR CODE PERSISTENCE**

**File:** `file_aware_agent.py`

**Code Storage:**

```python
class FileManager:
    def create_file(self, file_path: str, content: str):
        full_path = self.project_path / file_path
        with open(full_path, 'w') as f:
            f.write(content)  # ← ACTUAL FILE CREATED!

    def read_file(self, file_path: str):
        with open(full_path, 'r') as f:
            return f.read()  # ← READS REAL FILE!
```

**How Agents Access Code:**

```
Iteration 1:
├─ Backend creates: ./project/api.py (real file)
├─ Frontend creates: ./project/ui.js (real file)
└─ Files saved to disk

Iteration 2:
├─ Backend reads: ./project/api.py (from disk!)
├─ Frontend reads: ./project/ui.js (from disk!)
├─ Both can see and modify each other's files
└─ Updated files saved back to disk

Result: Real project in ./generated_projects/
```

**Example:**

```python
# Iteration 1
Backend: "```filename: src/api.py\nfrom fastapi import FastAPI..."
→ File created: ./generated_projects/my_project/src/api.py

# Iteration 2
Frontend: "I need to call the API..."
→ Reads: ./generated_projects/my_project/src/api.py
→ Sees: Backend's actual code
→ Creates: ./generated_projects/my_project/src/ui.js

# Later iterations
QA: "Let me test this..."
→ Reads BOTH files
→ Creates: ./generated_projects/my_project/tests/test_api.py
```

**✅ Pros:**
- ✅ Real files created on disk
- ✅ Persistent (survives process restart)
- ✅ Can be run, tested, deployed
- ✅ Agents read actual files
- ✅ Iterative improvement
- ✅ Version controlled (via git)

**❌ Cons:**
- None for production use!

---

## 🎯 Key Insights

### Memory-Based Workflows (Collaborative, Sequential, Hierarchical)

**What Happens:**

```python
# During workflow
agent_team.collaborative_workflow(task, agents)

# Code is in:
- agent.stored_messages (each agent's memory)
- self.conversation_history (team-level)
- Current context (passed between rounds)

# After workflow ends
results = {...}  # Contains all responses with code
# But no files created!
```

**Code Accessibility:**

| When | Accessible? | How? |
|------|------------|------|
| During same workflow | ✅ Yes | Via context & agent memory |
| Next round in same workflow | ✅ Yes | Included in context |
| After workflow ends | ⚠️ In results object only | `results[0]['response']` |
| Next workflow run | ❌ No | Would need to manually pass |
| From disk | ❌ No | Never written to files |

### File-Aware Workflow

**What Happens:**

```python
# During workflow
build_project.py "Create API"

# Code is in:
- agent.stored_messages (memory)
- Actual files on disk! ← KEY DIFFERENCE
- ./generated_projects/project_name/

# After workflow ends
# Files still exist!
# Can be:
- Opened in editor
- Run with python
- Tested
- Version controlled
- Deployed
```

**Code Accessibility:**

| When | Accessible? | How? |
|------|------------|------|
| During workflow | ✅ Yes | FileManager.read_file() |
| Between iterations | ✅ Yes | Read from disk |
| After workflow ends | ✅ Yes | Files persist on disk |
| Next workflow run | ✅ Yes | Can read existing project |
| From anywhere | ✅ Yes | Standard file system |

---

## 💡 Practical Examples

### Example 1: Collaborative Workflow (Code in Memory Only)

```python
from agent_team import AgentTeam

team = AgentTeam({
    "Backend": "backend_developer",
    "Frontend": "frontend_developer"
})

result = team.collaborative_workflow(
    task="Build user registration",
    agents=["Backend", "Frontend"],
    max_rounds=2
)

# Can agents access code?
# Round 1: Backend writes API code
#   ✅ Stored in: result[0]['response']
#   ✅ Stored in: backend_agent.stored_messages
#   ❌ NOT on disk

# Round 2: Frontend needs API code
#   ✅ YES! Frontend receives:
#      "Backend Developer said: [code]"
#   ✅ Frontend can reference it

# After workflow:
#   ✅ Code in: result list
#   ❌ No files created
#   ❌ Can't run it
#   ❌ Lost if Python exits

# To use the code:
backend_code = result[0]['response']
print(backend_code)  # Can see it
# But would need to manually save to file
```

### Example 2: File-Aware Workflow (Code in Files)

```bash
python build_project.py "Build user registration API" --llm
```

```python
# What happens:

# Iteration 1:
Backend creates → ./generated_projects/user_reg_api/src/main.py
Frontend creates → ./generated_projects/user_reg_api/src/ui.html

# Iteration 2:
Backend reads main.py (from disk!)
Backend updates → main.py (saved to disk!)
Frontend reads ui.html
Frontend updates → ui.html

# After workflow:
# Files exist: ./generated_projects/user_reg_api/
#   ├── src/
#   │   ├── main.py        ← Real file!
#   │   └── ui.html        ← Real file!
#   ├── tests/
#   │   └── test_api.py    ← Real file!
#   └── README.md          ← Real file!

# Can now:
cd ./generated_projects/user_reg_api/
python src/main.py  # ← Actually runs!
```

---

## 🔧 Solutions & Recommendations

### If You Want Code Persistence

**✅ RECOMMENDED: Use File-Aware Agents**

```bash
python build_project.py "Your project" --llm
```

**Why:**
- Creates real files
- Agents can read/modify files
- Code persists forever
- Can run, test, deploy
- Just like a real project

### If Using Memory-Based Workflows

**Option 1: Extract and Save Code Manually**

```python
result = team.collaborative_workflow(task, agents)

# Extract code from results
for response in result:
    content = response['response']
    # Parse code blocks
    if "```python" in content:
        code = extract_code_blocks(content)
        # Save to file
        with open(f"{response['agent']}.py", 'w') as f:
            f.write(code)
```

**Option 2: Use Sequential for Better Code Flow**

```python
# Sequential ensures each agent sees previous code
result = team.sequential_workflow(
    task="Build API",
    agent_order=["backend", "qa"]
)

# QA automatically sees backend's code
```

**Option 3: Create Helper to Save Code**

```python
def save_code_from_workflow(results, output_dir):
    """Extract and save code blocks from workflow results"""
    import re
    import os

    os.makedirs(output_dir, exist_ok=True)

    for result in results:
        agent = result['agent']
        content = result['response']

        # Find code blocks
        pattern = r'```(\w+)\n(.*?)```'
        matches = re.findall(pattern, content, re.DOTALL)

        for i, (lang, code) in enumerate(matches):
            ext = {'python': 'py', 'javascript': 'js', 'html': 'html'}.get(lang, 'txt')
            filename = f"{output_dir}/{agent}_{i}.{ext}"

            with open(filename, 'w') as f:
                f.write(code)

            print(f"Saved: {filename}")

# Usage:
result = team.collaborative_workflow(task, agents)
save_code_from_workflow(result, "./output_code")
```

---

## 📋 Decision Guide

### When to Use Each System

```
Need real, runnable project?
└─ YES → Use build_project.py (File-Aware)

Need code snippets to copy?
└─ YES → Use sequential_workflow + manual extraction

Need planning/discussion?
└─ YES → Use collaborative_workflow (code in results)

Need to modify existing project?
└─ YES → Use File-Aware agents with existing directory
```

---

## ✅ Summary

### Code Storage by System

| System | During Workflow | After Workflow | Agents Can Access | Files Created |
|--------|----------------|----------------|-------------------|---------------|
| Collaborative | In memory | In results object | Within rounds | ❌ No |
| Sequential | In memory | In results object | Each step | ❌ No |
| Hierarchical | In memory | In results object | Via manager | ❌ No |
| **File-Aware** | **In memory + files** | **Persistent files** | **Anytime** | **✅ Yes** |

### Recommendations

**For Production/Real Projects:**
```bash
# ALWAYS use file-aware agents
python build_project.py "Your project" --llm
```

**For Quick Code Generation:**
```python
# Use sequential, then extract code manually
result = team.sequential_workflow(task, agents)
# Parse and save code blocks
```

**For Planning Only:**
```python
# Collaborative is fine - no code needed
team.collaborative_workflow(task, agents)
```

---

**Key Takeaway:**

- **Memory-based workflows:** Code exists in conversation but not on disk
- **File-aware agents:** Code saved to real files that persist ⭐ **RECOMMENDED**

For actual code you want to run/deploy, **always use `build_project.py`**!
