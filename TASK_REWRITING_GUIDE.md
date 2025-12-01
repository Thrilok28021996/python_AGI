# Task Rewriting Guide

## 🎯 Overview

The **Task Rewriter** analyzes your project descriptions and rewrites them to be **clearer**, **more detailed**, and **better structured** while preserving the original meaning. This helps agents better understand what to build.

---

## 🤔 Why Rewrite Tasks?

### The Problem

Users often describe projects briefly:
- ❌ "Create a todo app"
- ❌ "Build an API"
- ❌ "Make a calculator"

These are **too vague** for agents to understand:
- What features should the todo app have?
- What endpoints should the API include?
- What operations should the calculator support?

### The Solution

The Task Rewriter **expands and clarifies** while **preserving your intent**:

✅ "Create a todo app" becomes:
```
# Project Goal
Build a todo list application with create, read, update, delete functionality

# Core Requirements
- Add new todo items with title and description
- Mark todos as complete/incomplete
- Delete todos
- List all todos
- Persist data

# Technical Specifications
- Use appropriate data storage (file, database, or in-memory)
- Include error handling for invalid inputs
- Provide user-friendly interface

# Success Criteria
- Users can manage their todo items
- Data persists between sessions
- All CRUD operations work correctly
```

---

## 🚀 How to Use

### Method 1: Automatic (Default)

By default, tasks are **automatically clarified** before agents start:

```bash
python build_project.py "Create a calculator"
```

Output:
```
🔄 Analyzing and clarifying task requirements...
✓ Task clarified and enhanced
```

The agents receive the **enhanced version** automatically!

### Method 2: Interactive (Review Before Use)

Use `--rewrite-task` to **see the comparison** and approve:

```bash
python build_project.py "Create a calculator" --rewrite-task
```

Output:
```
🔄 Analyzing and clarifying task requirements...

================================================================================
TASK COMPARISON
================================================================================

📝 ORIGINAL TASK:
Create a calculator

✨ REWRITTEN TASK:
# Project Goal
Build a calculator application with basic arithmetic operations

# Core Requirements
- Addition (+)
- Subtraction (-)
- Multiplication (*)
- Division (/)
- Handle edge cases (division by zero, invalid inputs)

# Technical Specifications
- Implement as a class or module
- Include input validation
- Provide clear error messages

# Success Criteria
- All arithmetic operations work correctly
- Edge cases handled appropriately
- Code is tested and functional

================================================================================

✅ Use rewritten task? (y/n) [y]:
```

Press `y` to use the enhanced version, or `n` to use the original.

### Method 3: Disable Rewriting

Use `--no-rewrite` to skip task clarification entirely:

```bash
python build_project.py "Create a calculator" --no-rewrite
```

The agents will receive your **exact original task**.

---

## 📊 Examples

### Example 1: Vague Task → Clear Requirements

**Original:**
```
Build an API
```

**Rewritten:**
```
# Project Goal
Create a REST API with standard CRUD endpoints

# Core Requirements
- RESTful API design
- Endpoint for creating resources (POST)
- Endpoint for reading resources (GET)
- Endpoint for updating resources (PUT/PATCH)
- Endpoint for deleting resources (DELETE)
- Input validation
- Error handling and appropriate HTTP status codes

# Technical Specifications
- Use appropriate framework (FastAPI, Flask, Express, etc.)
- Include request/response validation
- Implement proper error responses
- Add basic logging

# Success Criteria
- All CRUD operations functional
- Returns correct HTTP status codes
- Handles errors gracefully
- API is testable
```

### Example 2: Ambiguous Requirements → Specific Details

**Original:**
```
Create a user management system
```

**Rewritten:**
```
# Project Goal
Build a user management system with authentication and authorization

# Core Requirements
- User registration with email/username and password
- User login with credential validation
- User profile management (view, edit profile)
- Password reset functionality
- User roles and permissions
- Session management

# Technical Specifications
- Secure password hashing (bcrypt, argon2, etc.)
- Session tokens or JWT for authentication
- Input validation for user data
- Protection against common attacks (SQL injection, XSS)
- Database for user storage

# Success Criteria
- Users can register and login securely
- Passwords are hashed and never stored in plaintext
- Role-based access control works
- Session management is secure
- All security best practices followed
```

### Example 3: Technical Task → Structured Approach

**Original:**
```
Make a REST API for blog posts
```

**Rewritten:**
```
# Project Goal
Create a RESTful API for managing blog posts with full CRUD operations

# Core Requirements
Blog Post Model:
- Title (required, max 200 chars)
- Content (required, text)
- Author (required)
- Created/Updated timestamps
- Published status (draft/published)

API Endpoints:
- POST /posts - Create new post
- GET /posts - List all posts (with pagination)
- GET /posts/:id - Get single post
- PUT /posts/:id - Update post
- DELETE /posts/:id - Delete post

# Technical Specifications
- RESTful API design principles
- Input validation using schema validation
- Database for data persistence (PostgreSQL, MongoDB, etc.)
- Proper HTTP status codes (200, 201, 400, 404, 500)
- Error handling middleware
- Request logging
- API documentation (Swagger/OpenAPI)

# Success Criteria
- All CRUD operations work correctly
- Pagination works for listing posts
- Validation prevents invalid data
- Errors return meaningful messages
- API is well-documented
- Tests verify all endpoints
```

---

## 🎨 What Gets Improved?

### 1. Structure

**Before:**
```
Create a todo app with tests
```

**After:**
```
# Project Goal
[Clear one-sentence description]

# Core Requirements
- [Specific features]

# Technical Specifications
- [How to build it]

# Success Criteria
- [How to know it's done]
```

### 2. Clarity

**Before:** "Build an API" (What kind? For what?)

**After:** "Create a REST API for user management with authentication endpoints"

### 3. Details

**Before:** "Todo app"

**After:** Specifies CRUD operations, data persistence, error handling, testing

### 4. Technical Specs

**Before:** No technical guidance

**After:** Suggests frameworks, patterns, best practices

### 5. Success Criteria

**Before:** Unclear when done

**After:** Clear criteria for completion

---

## 🔧 Advanced Usage

### Programmatic Usage

```python
from task_rewriter import TaskRewriter

# Create rewriter
rewriter = TaskRewriter(model_name="llama3.2", temperature=0.3)

# Rewrite a task
original = "Create a calculator"
result = rewriter.rewrite_task(original, project_type="library")

print(result["rewritten"])

# With agent context
result = rewriter.rewrite_with_context(
    original_task="Build REST API",
    agents_selected=["backend_developer", "qa_tester", "security"],
    tech_stack=["FastAPI", "PostgreSQL", "JWT"]
)
```

### Interactive Mode

```python
from task_rewriter import interactive_task_rewrite

# Run interactive mode
task = interactive_task_rewrite()
# User enters task, sees comparison, approves
```

---

## 📋 CLI Flags

### `--rewrite-task`
Show comparison and ask for approval before using rewritten task

```bash
python build_project.py "Create API" --rewrite-task
```

### `--no-rewrite`
Skip task rewriting entirely, use original as-is

```bash
python build_project.py "Create API" --no-rewrite
```

### Default Behavior (No Flag)
Automatically rewrite and use enhanced task (silent mode)

```bash
python build_project.py "Create API"
# Automatically enhanced in background
```

---

## ✅ What Doesn't Change

The Task Rewriter **NEVER changes your intent**:

✅ **Preserves:**
- Original goal and purpose
- All requested features
- Core functionality requirements
- User's vision

❌ **Does NOT add:**
- Features you didn't ask for
- Different functionality
- Unrelated requirements
- New technologies (unless implicit)

### Example

**Original:** "Create a calculator with add and subtract"

**Rewritten:** ✅ Adds details about add/subtract, error handling, testing
**Rewritten:** ❌ Does NOT add multiply, divide, or other operations

---

## 🎯 Benefits

### 1. Better Agent Understanding
- Agents get clear, structured requirements
- Less ambiguity = better code
- Fewer iterations needed

### 2. More Complete Projects
- Implicit requirements made explicit
- Edge cases considered upfront
- Success criteria defined

### 3. Better Code Quality
- Technical specs guide implementation
- Best practices suggested
- Testing requirements clear

### 4. Saved Time
- Fewer back-and-forth clarifications
- Agents start with complete picture
- Less rework needed

---

## 🧪 Testing

### Test the Rewriter

```bash
# Run the example script
python task_rewriter.py
```

This runs examples showing:
1. Simple task rewrite
2. Rewrite with agent context
3. Interactive mode (commented out)

---

## 🔍 How It Works

### Technical Details

1. **LLM Analysis:**
   - Uses Ollama (llama3.2 by default)
   - Temperature: 0.3 (focused, not creative)
   - Analyzes user intent and requirements

2. **Structured Output:**
   - Formats as sections (Goal, Requirements, Specs, Criteria)
   - Breaks down complex ideas into lists
   - Makes implicit needs explicit

3. **Meaning Preservation:**
   - Explicit instructions to preserve intent
   - Never add features not requested
   - Only clarify and expand on existing ideas

4. **Improvement Analysis:**
   - Compares original vs rewritten
   - Lists improvements made
   - Shows why rewriting helped

---

## 📊 Comparison: Original vs Rewritten

| Aspect | Original Task | Rewritten Task |
|--------|---------------|----------------|
| **Length** | 1-2 sentences | Structured document |
| **Structure** | Unformatted | Sections with headers |
| **Details** | Vague | Specific features |
| **Tech Specs** | None | Framework suggestions |
| **Success Criteria** | Unclear | Well-defined |
| **Clarity** | Ambiguous | Explicit |

---

## 💡 Tips for Best Results

### 1. Start Simple
Let the rewriter add details. Just describe what you want:
```bash
"Create a todo app"
```

### 2. Mention Key Features
If you have specific needs, mention them:
```bash
"Create a todo app with categories and due dates"
```

### 3. Review If Unsure
Use `--rewrite-task` to see what changed:
```bash
python build_project.py "Your idea" --rewrite-task
```

### 4. Trust the Process
The rewriter is trained to preserve your meaning while adding clarity.

---

## 🚨 When to Use `--no-rewrite`

Use `--no-rewrite` when:
- Your task is already very detailed
- You have a specific format agents need to see
- You want exact control over phrasing
- You're testing something specific

Example:
```bash
python build_project.py "$(cat detailed_requirements.txt)" --no-rewrite
```

---

## 🎓 Learning More

### Related Documentation
- **build_project.py** - Main build tool with rewriter integration
- **task_rewriter.py** - Core rewriting implementation
- **llm_agent_selector.py** - Agent selection system

### Example Workflow

```bash
# 1. Describe your project (brief is fine)
python build_project.py "Create a blog API"

# The system will:
# → Rewrite task for clarity
# → Select appropriate agents
# → Build the project with clear requirements

# 2. Or review the rewrite first
python build_project.py "Create a blog API" --rewrite-task

# 3. Or skip rewriting
python build_project.py "$(cat my_detailed_spec.md)" --no-rewrite
```

---

## ✅ Summary

### Key Points

1. **Default Behavior:** Tasks are automatically enhanced (silent)
2. **Interactive Mode:** Use `--rewrite-task` to review changes
3. **Skip Rewriting:** Use `--no-rewrite` for original task
4. **Preserves Meaning:** Never changes your intent
5. **Adds Clarity:** Makes implicit requirements explicit
6. **Better Results:** Agents understand tasks better

### Quick Reference

```bash
# Auto-enhance (default)
python build_project.py "Your idea"

# Review before using
python build_project.py "Your idea" --rewrite-task

# Use original as-is
python build_project.py "Your idea" --no-rewrite
```

---

Happy building with clearer requirements! 🚀
