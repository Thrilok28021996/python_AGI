#!/usr/bin/env python3
"""
Test Agent Type Consistency
Verifies all agent types used by dynamic_team_builder exist in AGENT_CONFIGS
"""

import sys

print("=" * 80)
print("TESTING AGENT TYPE CONSISTENCY")
print("=" * 80)

# Import the agent configs
from specialized_agent import AGENT_CONFIGS

# Import dynamic team builder
from dynamic_team_builder import DynamicTeamBuilder, analyze_task_and_build_team

print("\n✅ TEST 1: Verify AGENT_CONFIGS Keys")
print("-" * 80)

valid_agent_types = list(AGENT_CONFIGS.keys())
print(f"Valid agent types ({len(valid_agent_types)}):")
for agent_type in valid_agent_types:
    print(f"  • {agent_type}")

print("\n✅ TEST 2: Build Teams and Verify Agent Types")
print("-" * 80)

test_cases = [
    "Create a simple calculator",
    "Build a REST API with authentication and database",
    "Build an e-commerce platform with React frontend, Node.js backend, PostgreSQL, payments, and security",
    "Create a machine learning model for image classification",
    "Build a mobile app with cloud backend and real-time features"
]

all_valid = True
for task in test_cases:
    print(f"\nTask: {task[:60]}...")
    team = analyze_task_and_build_team(task, max_agents=None, user_specified_agents=None)

    print(f"  Team size: {len(team)} agents")

    invalid_types = []
    for agent in team:
        agent_type = agent["type"]
        if agent_type not in valid_agent_types:
            invalid_types.append(agent_type)
            print(f"    ❌ INVALID: {agent_type} - {agent['name']}")
            all_valid = False
        else:
            print(f"    ✅ {agent_type} - {agent['name']}")

    if invalid_types:
        print(f"  ❌ Found {len(invalid_types)} invalid agent types!")

print("\n" + "=" * 80)
if all_valid:
    print("✅ ALL AGENT TYPES ARE VALID!")
    print("All agents used by dynamic_team_builder exist in AGENT_CONFIGS")
else:
    print("❌ INVALID AGENT TYPES FOUND!")
    print("Some agent types used by dynamic_team_builder don't exist in AGENT_CONFIGS")
    sys.exit(1)

print("=" * 80)
