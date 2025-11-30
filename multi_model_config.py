"""
Multi-Model Configuration
Allows different agents to use different Ollama models

OPTIMIZED FOR YOUR DOWNLOADED MODELS:
- qwen2.5-coder:14b (9.0 GB) - Best for coding tasks
- qwen2.5-coder:latest (4.7 GB) - Good for coding tasks
- mistral:latest (4.4 GB) - Best for reasoning and strategy
- deepseek-r1:latest (5.2 GB) - Best for analysis and reasoning
- phi3:latest (2.2 GB) - Fast, efficient for simpler tasks
- llama3.2:latest (2.0 GB) - General purpose, lightweight
- gemma3n:latest (7.5 GB) - General purpose
- qwen3:latest (5.2 GB) - General purpose
"""

# Model recommendations for different agent types
# Optimized based on your downloaded Ollama models

MODEL_ASSIGNMENTS = {
    # Strategic/Creative roles - use reasoning models
    "ceo": {
        "model": "mistral:latest",  # Best for strategic thinking
        "temperature": 0.7,
        "description": "Strategic thinking and decision making (using Mistral)"
    },
    "product_manager": {
        "model": "mistral:latest",  # Good for planning and reasoning
        "temperature": 0.7,
        "description": "Product planning and user stories (using Mistral)"
    },
    "designer": {
        "model": "gemma3n:latest",  # Creative tasks
        "temperature": 0.8,
        "description": "Creative design work (using Gemma)"
    },

    # Technical roles - use code-specialized models
    "lead_developer": {
        "model": "qwen2.5-coder:14b",  # Advanced code model for architecture
        "temperature": 0.4,
        "description": "Architecture and technical leadership (using Qwen2.5 Coder 14B)"
    },
    "backend_developer": {
        "model": "qwen2.5-coder:latest",  # Specialized for code generation
        "temperature": 0.3,
        "description": "Backend code implementation (using Qwen2.5 Coder)"
    },
    "frontend_developer": {
        "model": "qwen2.5-coder:latest",  # Specialized for code generation
        "temperature": 0.4,
        "description": "Frontend code implementation (using Qwen2.5 Coder)"
    },

    # Analysis/Testing roles - use reasoning models
    "qa_tester": {
        "model": "phi3:latest",  # Fast and efficient for testing tasks
        "temperature": 0.5,
        "description": "Quality assurance and testing (using Phi3 for speed)"
    },
    "security": {
        "model": "deepseek-r1:latest",  # Best for deep analysis
        "temperature": 0.2,
        "description": "Security analysis and reasoning (using DeepSeek-R1)"
    },

    # Operations roles
    "devops": {
        "model": "qwen2.5-coder:latest",  # Good for scripting and configs
        "temperature": 0.4,
        "description": "Infrastructure and deployment (using Qwen2.5 Coder)"
    },

    # Documentation roles
    "tech_writer": {
        "model": "phi3:latest",  # Fast and clear for documentation
        "temperature": 0.6,
        "description": "Documentation writing (using Phi3)"
    }
}


# YOUR DOWNLOADED MODELS - Reference Guide
DOWNLOADED_MODELS = {
    "qwen2.5-coder:14b": {
        "size": "9.0 GB",
        "best_for": ["lead_developer"],
        "strengths": "Advanced code generation, architecture design",
        "current_usage": "Lead Developer (architecture)"
    },
    "qwen2.5-coder:latest": {
        "size": "4.7 GB",
        "best_for": ["backend_developer", "frontend_developer", "devops"],
        "strengths": "Code generation and scripting",
        "current_usage": "Backend/Frontend Developers, DevOps"
    },
    "mistral:latest": {
        "size": "4.4 GB",
        "best_for": ["ceo", "product_manager"],
        "strengths": "Strategic thinking, complex reasoning",
        "current_usage": "CEO, Product Manager"
    },
    "deepseek-r1:latest": {
        "size": "5.2 GB",
        "best_for": ["security"],
        "strengths": "Deep analysis and reasoning",
        "current_usage": "Security Expert"
    },
    "phi3:latest": {
        "size": "2.2 GB",
        "best_for": ["qa_tester", "tech_writer"],
        "strengths": "Fast, efficient, good quality",
        "current_usage": "QA Tester, Technical Writer"
    },
    "gemma3n:latest": {
        "size": "7.5 GB",
        "best_for": ["designer"],
        "strengths": "Creative tasks, general purpose",
        "current_usage": "UI/UX Designer"
    },
    "llama3.2:latest": {
        "size": "2.0 GB",
        "best_for": ["fallback"],
        "strengths": "Lightweight, general purpose",
        "current_usage": "Fallback/default model"
    },
    "qwen3:latest": {
        "size": "5.2 GB",
        "best_for": ["alternative"],
        "strengths": "General purpose",
        "current_usage": "Not currently assigned (available for custom use)"
    }
}

# Models NOT used for text generation (excluded from assignments)
EMBEDDING_MODELS = {
    "mxbai-embed-large:latest": "Text embeddings only",
    "nomic-embed-text:latest": "Text embeddings only",
    "qwen2.5vl:latest": "Vision model (not for text-only tasks)"
}


def get_model_for_role(role_key: str) -> dict:
    """
    Get the recommended model configuration for a role

    Args:
        role_key: The role key (e.g., "backend_developer")

    Returns:
        Dict with model, temperature, and description
    """
    return MODEL_ASSIGNMENTS.get(role_key, {
        "model": "llama3.2",
        "temperature": 0.7,
        "description": "Default model"
    })


def update_model_assignment(role_key: str, model_name: str, temperature: float = None):
    """
    Update the model assignment for a specific role

    Args:
        role_key: The role key to update
        model_name: The Ollama model name to use
        temperature: Optional temperature override
    """
    if role_key in MODEL_ASSIGNMENTS:
        MODEL_ASSIGNMENTS[role_key]["model"] = model_name
        if temperature is not None:
            MODEL_ASSIGNMENTS[role_key]["temperature"] = temperature
    else:
        raise ValueError(f"Unknown role: {role_key}")


def print_model_assignments():
    """Print all current model assignments"""
    print("\nCurrent Model Assignments:")
    print("=" * 80)
    for role, config in MODEL_ASSIGNMENTS.items():
        print(f"{role:20} -> {config['model']:15} (temp: {config['temperature']}) - {config['description']}")
    print("=" * 80)


def get_available_models_info():
    """
    Get information about alternative models
    This is informational - you need to have these models installed in Ollama
    """
    return ALTERNATIVE_MODELS


# Example: How to use different models for different roles
"""
Usage Examples:

1. Use default models:
   from specialized_agent import create_agent
   agent = create_agent("backend_developer", "Bob")
   # Uses llama3.2 with temp 0.4

2. Override with a specific model:
   from specialized_agent import SpecializedAgent
   agent = SpecializedAgent(
       role="Backend Developer",
       name="Bob",
       expertise=["Python", "FastAPI"],
       model_name="codellama",  # Use CodeLlama instead
       temperature=0.3
   )

3. Update model assignment globally:
   from multi_model_config import update_model_assignment
   update_model_assignment("backend_developer", "codellama", 0.3)
   # Now all backend developers will use codellama

4. Check what models are recommended:
   from multi_model_config import print_model_assignments
   print_model_assignments()
"""
