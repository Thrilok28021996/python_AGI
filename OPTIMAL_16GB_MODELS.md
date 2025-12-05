# Optimal Models for 16GB RAM - Multi-Agent System

**Date**: 2025-12-03
**Target**: 16GB RAM system
**Goal**: Minimum models, maximum performance for 11 agent roles

---

## 🎯 The Perfect 16GB Setup

### Strategy: 3 Models for ALL 11 Roles

Using **efficient model reuse** across roles:

---

## 📦 Required Models (Only 3!)

### 1. **deepseek-r1:8b** ✅ (Already installed)
- **Size**: 5.2 GB RAM when loaded
- **Disk**: 5.2 GB
- **Use**: CEO
- **Why**: Best reasoning model (90.2% MATH, O3-level)
- **Status**: ✅ Already have it!

### 2. **deepseek-coder-v2:16b** 🔥 (NEED TO DOWNLOAD)
- **Size**: 9-10 GB RAM when loaded
- **Disk**: ~9.9 GB
- **Use**: Lead Developer, Backend Dev, Frontend Dev, Security Expert, DevOps, QA Tester, Data Scientist (7 roles)
- **Why**:
  - 90% HumanEval (top coding performance)
  - 128K context window
  - Excellent for architecture, security, all coding tasks
  - Best all-around coder

### 3. **qwen3:8b** ⚠️ (NEED TO VERIFY/UPDATE)
- **Size**: 5-6 GB RAM when loaded
- **Disk**: 5.2 GB
- **Use**: Product Manager, Tech Writer, Designer (3 roles)
- **Why**:
  - Latest generation reasoning
  - Good for documentation, planning, creative work
  - 40K context (sufficient for docs)
- **Status**: You have "qwen3:latest" - verify it's the 8b version

---

## 📊 RAM Usage Analysis

### Single Agent (Sequential):
- **Largest model**: deepseek-coder-v2:16b = 10 GB
- **System overhead**: 2-3 GB
- **Available**: 16 GB
- **Status**: ✅ Comfortable fit

### Two Agents (Concurrent):
- **deepseek-r1:8b** (5 GB) + **deepseek-coder-v2:16b** (10 GB) = 15 GB
- **System overhead**: 2-3 GB
- **Total**: ~17-18 GB
- **Status**: ⚠️ Tight but workable (use swap)

### Recommendation:
Run agents **sequentially** for best performance on 16GB RAM.

---

## 🎯 Agent Role Assignments

| Role | Model | RAM | Why |
|------|-------|-----|-----|
| **CEO** | deepseek-r1:8b | 5GB | O3-level reasoning |
| **Product Manager** | qwen3:8b | 6GB | Planning, requirements |
| **Lead Developer** | deepseek-coder-v2:16b | 10GB | Architecture, code review |
| **Backend Dev** | deepseek-coder-v2:16b | 10GB | APIs, databases |
| **Frontend Dev** | deepseek-coder-v2:16b | 10GB | UI, React, JS |
| **QA Tester** | deepseek-coder-v2:16b | 10GB | Test generation |
| **DevOps** | deepseek-coder-v2:16b | 10GB | CI/CD, Docker |
| **Designer** | qwen3:8b | 6GB | UI/UX, creative |
| **Security** | deepseek-coder-v2:16b | 10GB | Security analysis |
| **Tech Writer** | qwen3:8b | 6GB | Documentation |
| **Data Scientist** | deepseek-coder-v2:16b | 10GB | ML, data analysis |

**Total Unique Models**: 3
**Total Disk Space**: ~20 GB
**Peak RAM**: 10 GB (single agent)

---

## 🚀 Installation Commands

### Step 1: Verify what you have
```bash
ollama list
```

### Step 2: Download missing model
```bash
# CRITICAL - Best all-around coder
ollama pull deepseek-coder-v2:16b
```

### Step 3: Verify/Update Qwen3
```bash
# Check if your qwen3:latest is the 8b version
ollama show qwen3:latest

# If it's an older version, pull the latest 8b
ollama pull qwen3:8b
```

### Step 4: Verify DeepSeek-R1
```bash
# You already have this, just verify
ollama show deepseek-r1:latest
```

---

## 🗑️ Models to REMOVE (Save Space)

After verifying the new setup works:

```bash
# Remove old Qwen2.5-coder models (superseded by deepseek-coder-v2)
ollama rm qwen2.5-coder:7b       # Save 4.7 GB
ollama rm qwen2.5-coder:14b      # Save 9.0 GB

# Remove if not needed
ollama rm qwen2.5vl:latest       # Save 6.0 GB (vision, not used)
ollama rm phi3:latest            # Save 2.2 GB (outdated)
ollama rm mistral:latest         # Save 4.4 GB (not assigned)
ollama rm llama3.2:latest        # Save 2.0 GB (fallback)

# Keep embeddings (needed for semantic search)
# Keep: mxbai-embed-large, nomic-embed-text
```

**Space to reclaim**: ~28 GB!

---

## 💾 Before vs After

### BEFORE:
```
Installed: 11 models
Disk usage: ~42 GB
Many overlapping coding models
Missing critical deepseek-coder-v2
```

### AFTER:
```
Core models: 3 (deepseek-r1:8b, deepseek-coder-v2:16b, qwen3:8b)
Embeddings: 2 (mxbai-embed-large, nomic-embed-text)
Total: 5 models
Disk usage: ~22 GB
Space saved: ~20 GB
Performance: Optimized
```

---

## 🎯 Why This Configuration?

### 1. **Efficient Model Reuse**
- deepseek-coder-v2:16b handles 7 roles
- qwen3:8b handles 3 roles
- deepseek-r1:8b handles 1 role (CEO)

### 2. **Best Performance**
- **Coding**: 90% HumanEval (deepseek-coder-v2)
- **Reasoning**: 90.2% MATH (deepseek-r1)
- **Latest**: Qwen3:8b (latest generation)

### 3. **16GB RAM Optimized**
- Peak single agent: 10 GB
- System headroom: 6 GB
- Can run 2 concurrent agents if needed

### 4. **128K Context**
- deepseek-coder-v2: 128K tokens
- Can process large codebases
- Better than qwen2.5-coder (32K)

---

## ✅ Summary

### Download NOW:
```bash
ollama pull deepseek-coder-v2:16b   # CRITICAL
ollama pull qwen3:8b                # VERIFY/UPDATE
```

### Keep:
- deepseek-r1:latest (already have)
- mxbai-embed-large (embeddings)
- nomic-embed-text (embeddings)

### Remove after testing:
- qwen2.5-coder:7b
- qwen2.5-coder:14b
- qwen2.5vl:latest
- phi3:latest
- mistral:latest
- llama3.2:latest

### Result:
- ✅ 3 core models (5 total with embeddings)
- ✅ ~22 GB disk usage (save 20 GB!)
- ✅ 90% HumanEval coding
- ✅ 128K context
- ✅ Perfect for 16GB RAM
- ✅ All 11 roles covered

---

**Next Step**: Run the installation commands above and test!
