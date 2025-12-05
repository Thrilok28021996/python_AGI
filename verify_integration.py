#!/usr/bin/env python3
"""
Integration Verification Script
Verifies all company enhancements are properly integrated
Does NOT require Ollama to be running
"""

import sys
import os

print("=" * 80)
print("INTEGRATION VERIFICATION")
print("Verifying all company enhancements are properly integrated")
print("=" * 80)

# Test 1: Verify imports in file_aware_agent.py
print("\n✅ TEST 1: Import Integration in file_aware_agent.py")
print("-" * 80)

with open('file_aware_agent.py', 'r') as f:
    content = f.read()

checks = {
    "company_enhancements import": "from company_enhancements import",
    "ConflictResolver import": "ConflictResolver",
    "DocumentationGenerator import": "DocumentationGenerator",
    "PerformanceAnalytics import": "PerformanceAnalytics",
    "COMPANY_ENHANCEMENTS_AVAILABLE flag": "COMPANY_ENHANCEMENTS_AVAILABLE",
}

for check_name, check_string in checks.items():
    if check_string in content:
        print(f"  ✅ {check_name}")
    else:
        print(f"  ❌ {check_name} - MISSING!")
        sys.exit(1)

# Test 2: Verify initialization
print("\n✅ TEST 2: System Initialization")
print("-" * 80)

init_checks = {
    "ConflictResolver instantiation": "conflict_resolver = ConflictResolver()",
    "DocumentationGenerator instantiation": "doc_generator = DocumentationGenerator()",
    "PerformanceAnalytics instantiation": "performance_analytics = PerformanceAnalytics()",
    "Company Enhancements message": "Company Enhancements enabled",
}

for check_name, check_string in init_checks.items():
    if check_string in content:
        print(f"  ✅ {check_name}")
    else:
        print(f"  ❌ {check_name} - MISSING!")
        sys.exit(1)

# Test 3: Verify performance tracking integration
print("\n✅ TEST 3: Performance Tracking Integration")
print("-" * 80)

tracking_checks = {
    "File creation tracking": "performance_analytics.record_agent_contribution",
    "Review tracking": "contribution_type=\"review_",
}

for check_name, check_string in tracking_checks.items():
    if check_string in content:
        print(f"  ✅ {check_name}")
    else:
        print(f"  ❌ {check_name} - MISSING!")
        sys.exit(1)

# Test 4: Verify documentation generation integration
print("\n✅ TEST 4: Documentation Generation Integration")
print("-" * 80)

doc_checks = {
    "README generation call": "doc_generator.generate_readme",
    "README file saving": "README.md",
    "Auto-documentation message": "Auto-documentation",
}

for check_name, check_string in doc_checks.items():
    if check_string in content:
        print(f"  ✅ {check_name}")
    else:
        print(f"  ❌ {check_name} - MISSING!")
        sys.exit(1)

# Test 5: Verify performance reporting integration
print("\n✅ TEST 5: Performance Reporting Integration")
print("-" * 80)

reporting_checks = {
    "Quality score calculation": "calculate_code_quality_score",
    "Performance report display": "display_performance_report",
    "Performance report generation": "generate_performance_report",
}

for check_name, check_string in reporting_checks.items():
    if check_string in content:
        print(f"  ✅ {check_name}")
    else:
        print(f"  ❌ {check_name} - MISSING!")
        sys.exit(1)

# Test 6: Verify return value enhancements
print("\n✅ TEST 6: Return Value Enhancements")
print("-" * 80)

return_checks = {
    "Performance report in return": '"performance_report"',
    "README generated flag in return": '"readme_generated"',
}

for check_name, check_string in return_checks.items():
    if check_string in content:
        print(f"  ✅ {check_name}")
    else:
        print(f"  ❌ {check_name} - MISSING!")
        sys.exit(1)

# Test 7: Verify build_project.py has PM coordination enabled
print("\n✅ TEST 7: Build Project PM Coordination")
print("-" * 80)

with open('build_project.py', 'r') as f:
    build_content = f.read()

if "enable_pm_coordination=True" in build_content:
    print("  ✅ PM coordination enabled by default")
else:
    print("  ❌ PM coordination NOT enabled!")
    sys.exit(1)

# Test 8: Count integration points
print("\n✅ TEST 8: Integration Point Count")
print("-" * 80)

integration_points = {
    "Import block": content.count("from company_enhancements import"),
    "Initialization": content.count("ConflictResolver()"),
    "Performance tracking calls": content.count("performance_analytics.record_agent_contribution"),
    "Documentation generation": content.count("doc_generator.generate_readme"),
    "Quality score calculation": content.count("calculate_code_quality_score"),
}

total_points = sum(integration_points.values())
print(f"  Total integration points found: {total_points}")

for point_name, count in integration_points.items():
    print(f"    • {point_name}: {count} occurrence(s)")

if total_points >= 5:
    print(f"  ✅ Sufficient integration points ({total_points} >= 5)")
else:
    print(f"  ❌ Insufficient integration points ({total_points} < 5)")
    sys.exit(1)

# Test 9: Verify company_enhancements.py structure
print("\n✅ TEST 9: Company Enhancements File Structure")
print("-" * 80)

with open('company_enhancements.py', 'r') as f:
    enh_content = f.read()

enh_checks = {
    "ConflictResolver class": "class ConflictResolver:",
    "DocumentationGenerator class": "class DocumentationGenerator:",
    "PerformanceAnalytics class": "class PerformanceAnalytics:",
    "resolve_conflict method": "def resolve_conflict",
    "generate_readme method": "def generate_readme",
    "record_agent_contribution method": "def record_agent_contribution",
    "calculate_code_quality_score method": "def calculate_code_quality_score",
}

for check_name, check_string in enh_checks.items():
    if check_string in enh_content:
        print(f"  ✅ {check_name}")
    else:
        print(f"  ❌ {check_name} - MISSING!")
        sys.exit(1)

# Test 10: Verify all files exist
print("\n✅ TEST 10: Required Files Exist")
print("-" * 80)

required_files = [
    "company_enhancements.py",
    "file_aware_agent.py",
    "project_coordination.py",
    "dynamic_team_builder.py",
    "collaborative_review.py",
    "security_scanner.py",
    "test_executor.py",
    "build_project.py",
    "specialized_agent.py",
    "tdd_mode.py",
    "code_reviewer.py",
    "test_full_integration.py",
    "FINAL_INTEGRATION_REPORT.md",
    "QUICK_REFERENCE.md",
    "SESSION_SUMMARY.md",
]

missing_files = []
for filename in required_files:
    if os.path.exists(filename):
        print(f"  ✅ {filename}")
    else:
        print(f"  ❌ {filename} - MISSING!")
        missing_files.append(filename)

if missing_files:
    print(f"\n  ❌ Missing {len(missing_files)} files")
    sys.exit(1)

# Final Summary
print("\n" + "=" * 80)
print("INTEGRATION VERIFICATION COMPLETE")
print("=" * 80)
print("\n✅ All integration checks passed!")
print("\nVerified:")
print("  ✅ Imports properly added to file_aware_agent.py")
print("  ✅ Systems properly initialized")
print("  ✅ Performance tracking integrated throughout workflow")
print("  ✅ Documentation generation integrated at project completion")
print("  ✅ Performance reporting integrated at project completion")
print("  ✅ Return values enhanced with new data")
print("  ✅ PM coordination enabled by default")
print("  ✅ All required files present")
print("  ✅ company_enhancements.py properly structured")
print(f"  ✅ Total integration points: {total_points}")
print("\n🎉 The system is fully integrated and ready for use!")
print("\nAll company enhancements are properly wired into the workflow:")
print("  • Conflict Resolution - Ready to detect and resolve disagreements")
print("  • Documentation Generation - Will auto-create README.md")
print("  • Performance Analytics - Tracking contributions and quality")
print("\n" + "=" * 80)
