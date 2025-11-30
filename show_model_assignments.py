"""
Display Model Assignments
Shows which Ollama models are assigned to which agent roles
"""

import colorama
from multi_model_config import MODEL_ASSIGNMENTS, DOWNLOADED_MODELS, EMBEDDING_MODELS

colorama.init(autoreset=True)


def main():
    print(colorama.Fore.CYAN + """
╔════════════════════════════════════════════════════════════════════════╗
║             OPTIMIZED MODEL ASSIGNMENTS FOR YOUR SYSTEM                ║
║                                                                        ║
║  Your agents now use the best Ollama models for their specific roles  ║
╚════════════════════════════════════════════════════════════════════════╝
    """ + colorama.Style.RESET_ALL)

    # Group by model
    models_usage = {}
    for role, config in MODEL_ASSIGNMENTS.items():
        model = config["model"]
        if model not in models_usage:
            models_usage[model] = []
        models_usage[model].append({
            "role": role,
            "temperature": config["temperature"],
            "description": config["description"]
        })

    print(colorama.Fore.YELLOW + "\n📊 MODEL ASSIGNMENTS BY MODEL:\n" + colorama.Style.RESET_ALL)
    print("=" * 100)

    for model, roles in sorted(models_usage.items()):
        # Get model size if available
        size_info = ""
        for model_name, info in DOWNLOADED_MODELS.items():
            if model_name == model:
                size_info = f" [{info['size']}]"
                break

        print(colorama.Fore.GREEN + f"\n🤖 {model}{size_info}" + colorama.Style.RESET_ALL)
        print("-" * 100)

        for role_info in roles:
            print(f"  → {role_info['role']:20} (temp: {role_info['temperature']})  |  {role_info['description']}")

    print("\n" + "=" * 100)

    # Show by role category
    print(colorama.Fore.YELLOW + "\n📋 ASSIGNMENTS BY ROLE CATEGORY:\n" + colorama.Style.RESET_ALL)

    categories = {
        "Strategic Roles": ["ceo", "product_manager"],
        "Development Roles": ["lead_developer", "backend_developer", "frontend_developer", "devops"],
        "Quality & Security": ["qa_tester", "security"],
        "Creative & Documentation": ["designer", "tech_writer"]
    }

    for category, roles in categories.items():
        print(colorama.Fore.CYAN + f"\n{category}:" + colorama.Style.RESET_ALL)
        print("-" * 100)
        for role_key in roles:
            if role_key in MODEL_ASSIGNMENTS:
                config = MODEL_ASSIGNMENTS[role_key]
                print(f"  {role_key:20} → {config['model']:25} (temp: {config['temperature']})")

    # Show unused models
    print(colorama.Fore.YELLOW + "\n\n📦 DOWNLOADED BUT NOT CURRENTLY ASSIGNED:\n" + colorama.Style.RESET_ALL)
    print("-" * 100)

    assigned_models = set(config["model"] for config in MODEL_ASSIGNMENTS.values())
    for model_name, info in DOWNLOADED_MODELS.items():
        if model_name not in assigned_models and model_name not in EMBEDDING_MODELS:
            print(f"  • {model_name:30} ({info['size']:8}) - {info['strengths']}")
            print(f"    Available for custom use")

    # Show excluded models
    if EMBEDDING_MODELS:
        print(colorama.Fore.YELLOW + "\n\n🚫 MODELS EXCLUDED (Not for text generation):\n" + colorama.Style.RESET_ALL)
        print("-" * 100)
        for model_name, reason in EMBEDDING_MODELS.items():
            print(f"  • {model_name:30} - {reason}")

    # Summary
    print(colorama.Fore.GREEN + f"""

╔════════════════════════════════════════════════════════════════════════╗
║                           SUMMARY                                      ║
╠════════════════════════════════════════════════════════════════════════╣
║  Total Agent Roles: {len(MODEL_ASSIGNMENTS):2}                                                  ║
║  Unique Models Used: {len(models_usage):2}                                                ║
║  Total Models Downloaded: {len(DOWNLOADED_MODELS):2}                                           ║
║                                                                        ║
║  ✅ All agents optimized for their specific roles!                     ║
╚════════════════════════════════════════════════════════════════════════╝

🎯 KEY OPTIMIZATIONS:
  • Code tasks → Qwen2.5-Coder (specialized code model)
  • Strategic thinking → Mistral (best reasoning)
  • Security analysis → DeepSeek-R1 (deep analysis)
  • Fast tasks → Phi3 (efficient and quick)
  • Creative work → Gemma (creative capabilities)

💡 TIP: Run 'python quick_start_multi_agent.py' to test the optimized agents!

    """ + colorama.Style.RESET_ALL)


if __name__ == "__main__":
    main()
