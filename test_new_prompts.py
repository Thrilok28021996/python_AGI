#!/usr/bin/env python3
"""
Test New Agent Prompts - Verify Industry-Standard Prompts Work

Tests:
1. All agent types can be created
2. System messages contain new prompt structures
3. No "Questions/Concerns" in prompts
4. Role-specific response formats present
5. Critical requirements present for developers/QA
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from specialized_agent import create_agent, AGENT_CONFIGS


def test_agent_creation():
    """Test 1: Verify all agent types can be created"""
    print("\n" + "="*60)
    print("🧪 TEST 1: Agent Creation")
    print("="*60)

    results = []
    for agent_type in AGENT_CONFIGS.keys():
        try:
            agent = create_agent(agent_type, f"Test_{agent_type}")
            results.append((agent_type, True, agent.role))
            print(f"✅ {agent_type:20} → Created as '{agent.role}'")
        except Exception as e:
            results.append((agent_type, False, str(e)))
            print(f"❌ {agent_type:20} → FAILED: {e}")

    passed = sum(1 for _, success, _ in results if success)
    total = len(results)

    print(f"\n📊 Result: {passed}/{total} agents created successfully")
    return passed == total


def test_no_questions_concerns():
    """Test 2: Verify 'Questions/Concerns' removed from all prompts"""
    print("\n" + "="*60)
    print("🧪 TEST 2: No 'Questions/Concerns' Section")
    print("="*60)

    results = []
    for agent_type in AGENT_CONFIGS.keys():
        agent = create_agent(agent_type, f"Test_{agent_type}")
        prompt = agent.system_message.content

        has_questions_concerns = "Questions/Concerns" in prompt or "questions or concerns" in prompt.lower()

        if has_questions_concerns:
            results.append((agent_type, False))
            print(f"❌ {agent_type:20} → Still has 'Questions/Concerns'")
        else:
            results.append((agent_type, True))
            print(f"✅ {agent_type:20} → No 'Questions/Concerns'")

    passed = sum(1 for _, success in results if success)
    total = len(results)

    print(f"\n📊 Result: {passed}/{total} agents have 'Questions/Concerns' removed")
    return passed == total


def test_role_specific_formats():
    """Test 3: Verify role-specific response formats"""
    print("\n" + "="*60)
    print("🧪 TEST 3: Role-Specific Response Formats")
    print("="*60)

    # Expected format markers for specific roles
    expected_formats = {
        "ceo": ["Vision:", "Strategic Decision:", "Success Metrics:", "Immediate Actions:"],
        "product_manager": ["User Problem:", "Requirements:", "MUST HAVE:", "Acceptance Criteria:"],
        "lead_developer": ["Architecture Decision:", "Implementation:", "Code Review Notes:"],
        "qa_tester": ["Test Strategy:", "Test Files Created:", "Test Coverage:"],
        "devops": ["Infrastructure Design:", "Deployment Process:"],
        "designer": ["User Experience Approach:", "Design Concept:", "Accessibility Considerations:"],
        "security": ["Security Assessment:", "Vulnerabilities Identified:", "Security Checklist:"],
        "tech_writer": ["Documentation:", "Example structure:"],
        "data_scientist": ["Analysis Approach:", "Data Processing:", "Results & Insights:"]
    }

    results = []
    for agent_type, expected_markers in expected_formats.items():
        agent = create_agent(agent_type, f"Test_{agent_type}")
        prompt = agent.system_message.content

        found_markers = [marker for marker in expected_markers if marker in prompt]
        all_found = len(found_markers) == len(expected_markers)

        if all_found:
            results.append((agent_type, True))
            print(f"✅ {agent_type:20} → Has all format markers ({len(found_markers)}/{len(expected_markers)})")
        else:
            results.append((agent_type, False))
            print(f"❌ {agent_type:20} → Missing markers ({len(found_markers)}/{len(expected_markers)})")
            print(f"   Found: {found_markers}")
            print(f"   Expected: {expected_markers}")

    passed = sum(1 for _, success in results if success)
    total = len(results)

    print(f"\n📊 Result: {passed}/{total} roles have correct format markers")
    return passed == total


def test_critical_requirements():
    """Test 4: Verify critical requirements for developers and QA"""
    print("\n" + "="*60)
    print("🧪 TEST 4: Critical Requirements (Developers/QA)")
    print("="*60)

    # Roles that must have "CRITICAL REQUIREMENT"
    critical_roles = {
        "lead_developer": "YOU MUST WRITE ACTUAL, WORKING CODE",
        "backend_developer": "YOU MUST WRITE ACTUAL, WORKING CODE",
        "frontend_developer": "YOU MUST WRITE ACTUAL, WORKING CODE",
        "qa_tester": "YOU MUST CREATE ACTUAL TEST FILES",
        "devops": "YOU MUST WRITE ACTUAL, WORKING INFRASTRUCTURE CODE",
        "data_scientist": "YOU MUST WRITE ACTUAL, WORKING DATA CODE"
    }

    results = []
    for agent_type, expected_requirement in critical_roles.items():
        agent = create_agent(agent_type, f"Test_{agent_type}")
        prompt = agent.system_message.content

        has_critical = "CRITICAL REQUIREMENT" in prompt
        has_expected = expected_requirement in prompt

        if has_critical and has_expected:
            results.append((agent_type, True))
            print(f"✅ {agent_type:20} → Has critical requirement")
        else:
            results.append((agent_type, False))
            print(f"❌ {agent_type:20} → Missing critical requirement")
            if not has_critical:
                print(f"   Missing: 'CRITICAL REQUIREMENT'")
            if not has_expected:
                print(f"   Missing: '{expected_requirement}'")

    passed = sum(1 for _, success in results if success)
    total = len(results)

    print(f"\n📊 Result: {passed}/{total} roles have critical requirements")
    return passed == total


def test_action_oriented_language():
    """Test 5: Verify action-oriented language (CEO/PM)"""
    print("\n" + "="*60)
    print("🧪 TEST 5: Action-Oriented Language")
    print("="*60)

    action_roles = {
        "ceo": ["Drive execution", "Be decisive", "make it happen"],
        "product_manager": ["Focus on user value", "Prioritize ruthlessly", "Focus on MVP"]
    }

    results = []
    for agent_type, expected_phrases in action_roles.items():
        agent = create_agent(agent_type, f"Test_{agent_type}")
        prompt = agent.system_message.content

        found_phrases = [phrase for phrase in expected_phrases if phrase.lower() in prompt.lower()]
        all_found = len(found_phrases) == len(expected_phrases)

        if all_found:
            results.append((agent_type, True))
            print(f"✅ {agent_type:20} → Action-oriented ({len(found_phrases)}/{len(expected_phrases)} phrases)")
        else:
            results.append((agent_type, False))
            print(f"❌ {agent_type:20} → Not fully action-oriented ({len(found_phrases)}/{len(expected_phrases)})")
            print(f"   Missing: {set(expected_phrases) - set(found_phrases)}")

    passed = sum(1 for _, success in results if success)
    total = len(results)

    print(f"\n📊 Result: {passed}/{total} roles are action-oriented")
    return passed == total


def test_ceo_prompt_inspection():
    """Test 6: Detailed inspection of CEO prompt"""
    print("\n" + "="*60)
    print("🧪 TEST 6: CEO Prompt Detailed Inspection")
    print("="*60)

    ceo = create_agent("ceo", "Test_CEO")
    prompt = ceo.system_message.content

    print("\nCEO Prompt Excerpt:")
    print("-" * 60)
    # Print first 500 characters
    print(prompt[:500] + "...")
    print("-" * 60)

    checks = [
        ("Has 'Vision:' section", "Vision:" in prompt),
        ("Has 'Strategic Decision:' section", "Strategic Decision:" in prompt),
        ("Has 'Success Metrics:' section", "Success Metrics:" in prompt),
        ("Has 'Immediate Actions:' section", "Immediate Actions:" in prompt),
        ("No 'Questions/Concerns'", "Questions/Concerns" not in prompt),
        ("Action-oriented mindset", "How can we make this happen" in prompt),
        ("Has 'REMEMBER' footer", "REMEMBER:" in prompt and "Drive execution" in prompt)
    ]

    print("\n✅ CEO Prompt Checks:")
    passed = 0
    for check_name, result in checks:
        status = "✅" if result else "❌"
        print(f"{status} {check_name}")
        if result:
            passed += 1

    print(f"\n📊 Result: {passed}/{len(checks)} checks passed")
    return passed == len(checks)


def run_all_tests():
    """Run all tests and provide summary"""
    print("\n" + "="*60)
    print("🚀 TESTING NEW AGENT PROMPTS")
    print("="*60)
    print("Verifying industry-standard prompts are properly integrated")

    tests = [
        ("Agent Creation", test_agent_creation),
        ("No Questions/Concerns", test_no_questions_concerns),
        ("Role-Specific Formats", test_role_specific_formats),
        ("Critical Requirements", test_critical_requirements),
        ("Action-Oriented Language", test_action_oriented_language),
        ("CEO Prompt Inspection", test_ceo_prompt_inspection)
    ]

    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n❌ {test_name} CRASHED: {e}")
            results.append((test_name, False))

    # Summary
    print("\n" + "="*60)
    print("📊 FINAL SUMMARY")
    print("="*60)

    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status:12} {test_name}")

    passed = sum(1 for _, result in results if result)
    total = len(results)

    print("\n" + "="*60)
    if passed == total:
        print(f"🎉 ALL TESTS PASSED! ({passed}/{total})")
        print("="*60)
        print("\n✅ New agent prompts are properly integrated!")
        print("✅ All agents use industry-standard prompts!")
        print("✅ No more 'Questions/Concerns' sections!")
        print("✅ Action-oriented and code-focused!")
        return True
    else:
        print(f"⚠️  SOME TESTS FAILED ({passed}/{total})")
        print("="*60)
        print("\nPlease review the failed tests above.")
        return False


if __name__ == "__main__":
    import sys
    success = run_all_tests()
    sys.exit(0 if success else 1)
