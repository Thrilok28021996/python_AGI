# LLM Selection Guide for Agents

**A comprehensive guide for choosing the right LLM model for each agent type**

---

## 📋 Table of Contents

1. [Introduction](#introduction)
2. [Model Categories](#model-categories)
3. [Agent-to-Model Mapping](#agent-to-model-mapping)
4. [Selection Criteria](#selection-criteria)
5. [Current Assignments](#current-assignments)
6. [Adding New Models](#adding-new-models)
7. [Performance Optimization](#performance-optimization)
8. [Future-Proofing](#future-proofing)

---

## Introduction

### Why Different Models for Different Agents?

Each agent role has unique requirements:
- **Code Generation** requires models trained on code
- **Strategic Planning** needs strong reasoning capabilities
- **Security Analysis** requires deep analytical thinking
- **Creative Design** benefits from higher temperature/creativity
- **Documentation** needs clarity and structure

Using specialized models for each agent improves:
- ✅ Output quality
- ✅ Task accuracy
- ✅ Resource efficiency
- ✅ Cost optimization
- ✅ Response speed

---

## Model Categories

### 1. Code-Specialized Models

**Purpose:** Writing, analyzing, and debugging code

**Characteristics:**
- Trained on billions of lines of code
- Understand programming patterns
- Generate syntactically correct code
- Support multiple languages
- Good at debugging and optimization

**Best For:**
- Backend Development
- Frontend Development
- DevOps scripting
- Code review

**Examples:**
- `qwen2.5-coder` (7B, 14B, 32B)
- `codellama` (7B, 13B, 34B)
- `deepseek-coder` (1.3B, 6.7B, 33B)
- `starcoder2` (3B, 7B, 15B)
- `wizardcoder` (various sizes)

**Recommended Temperature:** 0.2-0.4 (lower for deterministic code)

---

### 2. Reasoning & Analysis Models

**Purpose:** Deep thinking, planning, analysis

**Characteristics:**
- Strong logical reasoning
- Multi-step problem solving
- Complex decision making
- Abstract thinking
- Pattern recognition

**Best For:**
- Strategic Planning (CEO)
- Security Analysis
- Architecture Design
- Problem Diagnosis
- System Design

**Examples:**
- `deepseek-r1` (1.5B, 7B, 14B, 32B, 70B)
- `qwen2.5` (0.5B to 72B)
- `mistral` (7B)
- `mixtral` (8x7B, 8x22B)
- `llama3.2` (1B, 3B)
- `llama3.1` (8B, 70B, 405B)

**Recommended Temperature:** 0.2-0.5 (lower for analytical tasks)

---

### 3. General Purpose Models

**Purpose:** Versatile tasks, good all-rounders

**Characteristics:**
- Balanced performance
- Good instruction following
- Reasonable at most tasks
- Moderate resource usage
- Fast inference

**Best For:**
- Product Management
- Technical Writing
- QA Testing
- General coordination
- Communication

**Examples:**
- `llama3.2` (1B, 3B)
- `llama3.1` (8B, 70B)
- `gemma2` (2B, 9B, 27B)
- `phi3` (3.8B, 14B)
- `mistral` (7B)

**Recommended Temperature:** 0.5-0.7 (balanced)

---

### 4. Creative & Design Models

**Purpose:** Creative thinking, design, ideation

**Characteristics:**
- High creativity
- Diverse outputs
- Less constrained
- Good at brainstorming
- Understand aesthetics

**Best For:**
- UI/UX Design
- Marketing content
- Branding
- User experience
- Creative solutions

**Examples:**
- `llama3.2` with high temperature
- `mistral` with high temperature
- `gemma2` (creative variants)
- Any general model with temperature 0.7-0.9

**Recommended Temperature:** 0.7-0.9 (higher for creativity)

---

### 5. Fast & Lightweight Models

**Purpose:** Quick responses, simple tasks

**Characteristics:**
- Small model size (1B-3B)
- Fast inference
- Low resource usage
- Good for simple tasks
- Can run on limited hardware

**Best For:**
- Quick decisions
- Simple classifications
- Rapid iterations
- Resource-constrained environments
- High-frequency tasks

**Examples:**
- `phi3` (3.8B - Mini)
- `llama3.2` (1B, 3B)
- `gemma2` (2B)
- `qwen2.5` (0.5B, 1.5B, 3B)
- `deepseek-r1` (1.5B)

**Recommended Temperature:** 0.3-0.6

---

### 6. Large Context Models

**Purpose:** Processing large documents, codebases

**Characteristics:**
- Large context window (32K-128K+ tokens)
- Can process entire files
- Good at cross-referencing
- Understand large systems
- Expensive but thorough

**Best For:**
- Code review (entire files)
- Documentation review
- System architecture
- Large refactoring
- Multi-file analysis

**Examples:**
- `qwen2.5` (context: 32K-128K)
- `mistral` (context: 32K)
- `llama3.1` (context: 128K)
- `gemma2` (context: 8K-32K)

**Recommended Temperature:** 0.3-0.5

---

## Agent-to-Model Mapping

### Decision Matrix

| Agent Role | Primary Task | Model Category | Recommended Models | Temperature | Reasoning |
|------------|--------------|----------------|-------------------|-------------|-----------|
| **CEO** | Strategic planning, decisions | Reasoning | mistral, llama3.1-70B, deepseek-r1 | 0.6-0.7 | Needs strong reasoning, big picture thinking |
| **Product Manager** | Requirements, planning | General Purpose | llama3.2, mistral, gemma2 | 0.6-0.7 | Balance of creativity and structure |
| **Lead Developer** | Architecture, tech lead | Code + Reasoning | qwen2.5-coder-14B, deepseek-coder-33B | 0.4-0.5 | Needs both code and system design skills |
| **Backend Developer** | Server-side code | Code-Specialized | qwen2.5-coder, codellama, deepseek-coder | 0.2-0.3 | Pure code generation, low variance |
| **Frontend Developer** | UI code, components | Code-Specialized | qwen2.5-coder, codellama | 0.3-0.4 | Code + some design sense |
| **QA Tester** | Testing, quality | General Purpose | llama3.2, mistral | 0.3-0.5 | Systematic thinking, finding edge cases |
| **DevOps Engineer** | Infrastructure, deployment | Code + General | qwen2.5-coder, llama3.2 | 0.3-0.4 | Scripting + system understanding |
| **UI/UX Designer** | Design, user experience | Creative | llama3.2, mistral, gemma2 | 0.7-0.9 | High creativity for design ideas |
| **Security Expert** | Security, vulnerability | Reasoning | deepseek-r1, qwen2.5, mistral | 0.2-0.3 | Deep analysis, low false positives |
| **Tech Writer** | Documentation | General Purpose | llama3.2, mistral, gemma2 | 0.5-0.6 | Clear, structured writing |

---

## Selection Criteria

### How to Choose the Right Model

#### 1. Task Complexity
```
Simple Task (1-2 steps):      → Small model (1B-3B)
Medium Task (3-5 steps):      → Medium model (7B-14B)
Complex Task (5+ steps):      → Large model (30B-70B+)
```

#### 2. Response Speed vs Quality
```
Speed Critical:               → phi3, llama3.2-1B, qwen2.5-3B
Balanced:                     → llama3.2-3B, mistral-7B, qwen2.5-7B
Quality Critical:             → llama3.1-70B, qwen2.5-32B, deepseek-r1-70B
```

#### 3. Code Generation Quality
```
Basic Scripts:                → codellama-7B, qwen2.5-coder-7B
Production Code:              → qwen2.5-coder-14B, deepseek-coder-33B
Complex Systems:              → qwen2.5-coder-32B, codellama-34B
```

#### 4. Reasoning Depth
```
Simple Logic:                 → llama3.2, gemma2
Medium Analysis:              → mistral, qwen2.5-7B
Deep Reasoning:               → deepseek-r1, qwen2.5-32B+
```

#### 5. Creativity Level
```
Deterministic (Low):          → Temperature 0.2-0.3
Balanced:                     → Temperature 0.5-0.6
Creative (High):              → Temperature 0.7-0.9
```

---

## Current Assignments

### As of 2025-11-30

**Configuration File:** `multi_model_config.py`

```python
MODEL_ASSIGNMENTS = {
    "ceo": {
        "model": "mistral:latest",
        "temperature": 0.7,
        "reason": "Strategic thinking requires strong reasoning"
    },

    "product_manager": {
        "model": "llama3.2",
        "temperature": 0.6,
        "reason": "Balance of creativity and structure"
    },

    "lead_developer": {
        "model": "qwen2.5-coder:14b",
        "temperature": 0.4,
        "reason": "Advanced code + architecture"
    },

    "backend_developer": {
        "model": "qwen2.5-coder:latest",
        "temperature": 0.3,
        "reason": "Specialized code generation"
    },

    "frontend_developer": {
        "model": "qwen2.5-coder:latest",
        "temperature": 0.4,
        "reason": "Code + some design creativity"
    },

    "qa_tester": {
        "model": "llama3.2",
        "temperature": 0.3,
        "reason": "Systematic, thorough testing"
    },

    "devops": {
        "model": "llama3.2",
        "temperature": 0.3,
        "reason": "Infrastructure + scripting"
    },

    "ui_ux_designer": {
        "model": "llama3.2",
        "temperature": 0.8,
        "reason": "High creativity for design"
    },

    "security": {
        "model": "deepseek-r1:latest",
        "temperature": 0.2,
        "reason": "Deep security analysis"
    },

    "tech_writer": {
        "model": "llama3.2",
        "temperature": 0.5,
        "reason": "Clear, structured documentation"
    }
}
```

---

## Adding New Models

### When New Models Are Released

#### Step 1: Evaluate the Model

**Test for:**
1. Code generation quality (if applicable)
2. Reasoning ability
3. Instruction following
4. Response speed
5. Resource usage
6. Context window size

**Benchmark Tasks:**
```python
# Code Generation Test
"Write a Python function to sort a list using quicksort"

# Reasoning Test
"Design a scalable architecture for 1M users"

# Instruction Following Test
"Respond in exactly 3 bullet points about REST APIs"

# Creativity Test
"Design a logo concept for a tech startup"
```

#### Step 2: Categorize the Model

Determine which category:
- Code-Specialized
- Reasoning & Analysis
- General Purpose
- Creative & Design
- Fast & Lightweight
- Large Context

#### Step 3: Compare with Existing Models

**Comparison Criteria:**
- Quality vs current model
- Speed vs current model
- Resource usage
- Special capabilities
- Cost (if applicable)

#### Step 4: Update Configuration

**File:** `multi_model_config.py`

```python
# Add to MODEL_ASSIGNMENTS
"agent_type": {
    "model": "new_model_name:version",
    "temperature": 0.X,
    "reason": "Why this model is optimal for this agent"
}
```

#### Step 5: Document the Change

Update this guide with:
- Model name and versions
- Category
- Best use cases
- Comparison with alternatives
- When to use vs not use

---

## Performance Optimization

### Model Size vs Performance

```
┌─────────────────────────────────────────────────────────┐
│                   Model Performance                      │
├─────────────┬──────────┬──────────┬────────────────────┤
│ Model Size  │  Speed   │ Quality  │ Best For           │
├─────────────┼──────────┼──────────┼────────────────────┤
│ 1B-3B       │  ⚡⚡⚡⚡   │  ⭐⭐     │ Simple tasks       │
│ 7B-14B      │  ⚡⚡⚡    │  ⭐⭐⭐   │ Most tasks         │
│ 30B-40B     │  ⚡⚡     │  ⭐⭐⭐⭐  │ Complex tasks      │
│ 70B+        │  ⚡      │  ⭐⭐⭐⭐⚡ │ Critical tasks     │
└─────────────┴──────────┴──────────┴────────────────────┘
```

### Hardware Requirements

**Minimum Specs per Model Size:**

```
1B-3B Models:
- RAM: 4GB
- VRAM: 2GB (GPU optional)
- CPU: 4 cores
- Inference Speed: ~50 tokens/sec

7B Models:
- RAM: 8GB
- VRAM: 6GB (GPU recommended)
- CPU: 8 cores
- Inference Speed: ~30 tokens/sec

14B Models:
- RAM: 16GB
- VRAM: 12GB (GPU recommended)
- CPU: 16 cores
- Inference Speed: ~20 tokens/sec

30B+ Models:
- RAM: 32GB+
- VRAM: 24GB+ (GPU required)
- CPU: 32+ cores
- Inference Speed: ~10 tokens/sec
```

### Optimization Strategies

#### 1. Tiered Approach
```python
# Use fast model for initial draft
draft = small_model.generate(task)

# Use quality model for refinement
final = large_model.refine(draft)
```

#### 2. Task-Specific Routing
```python
if task_type == "simple":
    model = "phi3:3.8B"
elif task_type == "code":
    model = "qwen2.5-coder:14B"
elif task_type == "complex":
    model = "llama3.1:70B"
```

#### 3. Quantization
```
Full Precision (F16):     Best quality, slowest
Q8 Quantization:          Good quality, faster
Q4 Quantization:          Acceptable quality, very fast
Q2 Quantization:          Lower quality, extremely fast
```

---

## Future-Proofing

### Preparing for New Model Releases

#### 1. Model Naming Convention

**Standardize naming:**
```
model_name:version-size-quantization

Examples:
- llama3.2:3B
- qwen2.5-coder:14B-q4
- mistral:7B-v0.3
```

#### 2. Configuration Structure

**Make it easy to swap models:**

```python
# models.yaml (future config file)
agents:
  backend_developer:
    primary_model: "qwen2.5-coder:14B"
    fallback_model: "codellama:13B"
    min_model: "qwen2.5-coder:7B"  # If primary unavailable
    temperature: 0.3
    max_tokens: 4096

  security:
    primary_model: "deepseek-r1:32B"
    fallback_model: "qwen2.5:14B"
    min_model: "llama3.2:3B"
    temperature: 0.2
    max_tokens: 8192
```

#### 3. Model Registry

**Track available models:**

```python
# model_registry.py
AVAILABLE_MODELS = {
    "qwen2.5-coder": {
        "versions": ["7B", "14B", "32B"],
        "category": "code",
        "context_length": 32768,
        "updated": "2025-01"
    },
    "deepseek-r1": {
        "versions": ["1.5B", "7B", "14B", "32B", "70B"],
        "category": "reasoning",
        "context_length": 16384,
        "updated": "2025-01"
    }
}
```

#### 4. Automatic Model Selection

**Dynamic selection based on task:**

```python
def select_optimal_model(task_complexity, task_type, hardware_available):
    """
    Automatically select best model based on:
    - Task complexity (simple, medium, complex)
    - Task type (code, reasoning, creative, etc.)
    - Available hardware (RAM, GPU, etc.)
    """

    if task_type == "code":
        if hardware_available["vram"] >= 12:
            return "qwen2.5-coder:14B"
        else:
            return "qwen2.5-coder:7B"

    elif task_type == "reasoning":
        if task_complexity == "complex":
            return "deepseek-r1:32B"
        else:
            return "mistral:7B"

    # ... more logic
```

#### 5. Model Versioning

**Track model changes:**

```python
MODEL_CHANGELOG = {
    "2025-01": {
        "backend_developer": {
            "old": "codellama:13B",
            "new": "qwen2.5-coder:14B",
            "reason": "Better code quality, faster"
        }
    },
    "2025-02": {
        "security": {
            "old": "qwen2.5:14B",
            "new": "deepseek-r1:32B",
            "reason": "Superior reasoning for security analysis"
        }
    }
}
```

---

## Migration Guide

### How to Migrate to New Models

#### Step 1: Test New Model
```bash
# Pull new model
ollama pull new_model:version

# Test with agent
python test_agent.py --agent backend_developer --model new_model:version
```

#### Step 2: Compare Results
```python
# Compare old vs new
old_result = agent.run_with_model("old_model:version", task)
new_result = agent.run_with_model("new_model:version", task)

# Evaluate
compare_quality(old_result, new_result)
compare_speed(old_result, new_result)
```

#### Step 3: Update Configuration
```python
# multi_model_config.py
MODEL_ASSIGNMENTS = {
    "backend_developer": {
        "model": "new_model:version",  # Changed
        "temperature": 0.3,
        "reason": "Better performance on benchmarks"
    }
}
```

#### Step 4: Document & Rollback Plan
```python
# Keep old config for rollback
ROLLBACK_MODELS = {
    "backend_developer": "old_model:version"
}
```

---

## Best Practices

### Do's ✅

1. **Match Model to Task**
   - Use code models for coding
   - Use reasoning models for analysis
   - Use general models for versatile tasks

2. **Consider Resources**
   - Choose model size based on available hardware
   - Use quantization for faster inference
   - Cache model responses when possible

3. **Test Before Deploying**
   - Benchmark new models
   - Compare with current models
   - Validate on real tasks

4. **Monitor Performance**
   - Track response quality
   - Monitor inference speed
   - Measure resource usage

5. **Keep Updated**
   - Check for new model releases
   - Test improvements
   - Update configurations

### Don'ts ❌

1. **Don't Use Oversized Models**
   - 70B model for simple tasks = waste
   - Match model size to complexity

2. **Don't Ignore Temperature**
   - Low temperature for deterministic tasks
   - High temperature for creative tasks
   - Wrong temperature = poor results

3. **Don't Mix Incompatible Versions**
   - Ensure Ollama version supports model
   - Check model compatibility

4. **Don't Forget Fallbacks**
   - Always have backup model
   - Handle model unavailability

5. **Don't Skip Documentation**
   - Document why each model was chosen
   - Track performance changes
   - Keep migration history

---

## Quick Reference

### Model Selection Cheat Sheet

```
TASK: Write production backend code
→ USE: qwen2.5-coder:14B (temp: 0.3)

TASK: Strategic business planning
→ USE: mistral:7B or llama3.1:70B (temp: 0.6-0.7)

TASK: Security vulnerability analysis
→ USE: deepseek-r1:32B (temp: 0.2)

TASK: Creative UI design concepts
→ USE: llama3.2:3B (temp: 0.8-0.9)

TASK: Technical documentation
→ USE: llama3.2:3B or mistral:7B (temp: 0.5)

TASK: Quick code snippet
→ USE: phi3:3.8B or qwen2.5-coder:7B (temp: 0.3)

TASK: System architecture design
→ USE: qwen2.5:14B or deepseek-r1:14B (temp: 0.4)

TASK: Testing and QA
→ USE: llama3.2:3B (temp: 0.3-0.5)
```

---

## Resources

### Model Downloads

**Ollama Models Library:**
```bash
# List all available models
ollama list

# Search for models
ollama search coder
ollama search reasoning

# Pull specific model
ollama pull model_name:version
```

### Model Information

- **Ollama Library:** https://ollama.ai/library
- **Model Cards:** Check each model's documentation
- **Benchmarks:** https://huggingface.co/spaces/HuggingFaceH4/open_llm_leaderboard

### Community Resources

- Model comparison discussions
- Benchmark results
- Use case examples
- Performance tips

---

## Appendix

### Model Comparison Table

| Model | Size | Category | Speed | Quality | Best For | Context |
|-------|------|----------|-------|---------|----------|---------|
| phi3 | 3.8B | Fast | ⚡⚡⚡⚡ | ⭐⭐ | Quick tasks | 4K |
| llama3.2 | 1B-3B | General | ⚡⚡⚡⚡ | ⭐⭐⭐ | Balanced | 8K |
| mistral | 7B | General | ⚡⚡⚡ | ⭐⭐⭐⭐ | Reasoning | 32K |
| qwen2.5-coder | 7B-32B | Code | ⚡⚡⚡ | ⭐⭐⭐⭐ | Coding | 32K |
| codellama | 7B-34B | Code | ⚡⚡ | ⭐⭐⭐⭐ | Code gen | 16K |
| deepseek-r1 | 7B-70B | Reasoning | ⚡⚡ | ⭐⭐⭐⭐⭐ | Analysis | 16K |
| llama3.1 | 8B-405B | General | ⚡⚡ | ⭐⭐⭐⭐⭐ | Complex | 128K |
| gemma2 | 2B-27B | General | ⚡⚡⚡ | ⭐⭐⭐ | Balanced | 8K |

---

**Last Updated:** 2025-11-30
**Maintained By:** Python AGI Project
**Version:** 1.0
**Next Review:** When new major models are released

---

## Summary

This guide provides:
- ✅ Clear model categorization
- ✅ Agent-to-model mapping with reasoning
- ✅ Selection criteria and decision matrix
- ✅ Future-proofing strategies
- ✅ Migration guide for new models
- ✅ Best practices and quick reference

Use this guide when:
- Adding new agent types
- New models are released
- Optimizing performance
- Troubleshooting quality issues
- Planning upgrades
