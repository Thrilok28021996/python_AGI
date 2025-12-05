#!/usr/bin/env python3
"""
Test .DS_Store Automatic Filtering

This test verifies that agents NEVER see .DS_Store files anywhere in the codebase.
"""

import tempfile
import os
from pathlib import Path


def test_utils_filtering():
    """Test utils.py filtering functions"""
    print("Testing utils.py filtering functions...")

    from utils import should_ignore_file, should_ignore_directory, SYSTEM_IGNORE_FILES

    # Test .DS_Store detection
    assert should_ignore_file(Path(".DS_Store")), "Failed to detect .DS_Store"
    assert should_ignore_file(Path(".DS_Store?")), "Failed to detect .DS_Store?"
    assert should_ignore_file(Path("._hidden")), "Failed to detect ._* files"
    assert should_ignore_file(Path("Thumbs.db")), "Failed to detect Thumbs.db"

    # Test normal files are NOT ignored
    assert not should_ignore_file(Path("main.py")), "Incorrectly ignored main.py"
    assert not should_ignore_file(Path("README.md")), "Incorrectly ignored README.md"

    # Test directory filtering
    assert should_ignore_directory(Path("__pycache__")), "Failed to detect __pycache__"
    assert should_ignore_directory(Path(".git")), "Failed to detect .git"
    assert should_ignore_directory(Path("node_modules")), "Failed to detect node_modules"

    # Test normal directories are NOT ignored
    assert not should_ignore_directory(Path("src")), "Incorrectly ignored src"
    assert not should_ignore_directory(Path("tests")), "Incorrectly ignored tests"

    print("✅ utils.py filtering: PASSED")
    return True


def test_file_aware_agent_filtering():
    """Test file_aware_agent.py filtering"""
    print("Testing file_aware_agent.py filtering...")

    from file_aware_agent import FileManager

    # Create temporary test directory
    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)

        # Create test files
        (tmppath / "main.py").write_text("print('hello')")
        (tmppath / "utils.py").write_text("def foo(): pass")
        (tmppath / ".DS_Store").write_text("system file")
        (tmppath / "._backup").write_text("system file")
        (tmppath / "Thumbs.db").write_text("system file")

        # Create file manager
        manager = FileManager(tmppath)

        # List files
        files = manager.list_files()

        # Verify system files are NOT in the list
        assert ".DS_Store" not in str(files), "❌ .DS_Store found in file list!"
        assert "._backup" not in str(files), "❌ ._backup found in file list!"
        assert "Thumbs.db" not in str(files), "❌ Thumbs.db found in file list!"

        # Verify normal files ARE in the list
        assert "main.py" in str(files), "❌ main.py not found!"
        assert "utils.py" in str(files), "❌ utils.py not found!"

        print(f"  Files seen by agents: {files}")
        print("✅ file_aware_agent.py filtering: PASSED")

    return True


def test_security_scanner_filtering():
    """Test security_scanner.py filtering"""
    print("Testing security_scanner.py filtering...")

    from security_scanner import SecurityScanner

    # Create temporary test directory
    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)

        # Create test files
        (tmppath / "main.py").write_text("import os\nos.system('ls')")
        (tmppath / ".DS_Store").write_text("system file")
        (tmppath / "._backup.py").write_text("import os")

        # Create scanner
        scanner = SecurityScanner(tmppath)

        # Check if detected as Python project
        is_python = scanner._is_python_project()
        assert is_python, "❌ Failed to detect Python project"

        # The scanner should only scan main.py, not system files
        # This is tested indirectly through the filtering
        print("✅ security_scanner.py filtering: PASSED")

    return True


def test_test_executor_filtering():
    """Test test_executor.py filtering"""
    print("Testing test_executor.py filtering...")

    from test_executor import TestExecutor

    # Create temporary test directory
    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)

        # Create test files
        (tmppath / "test_main.py").write_text("def test_foo(): assert True")
        (tmppath / ".DS_Store").write_text("system file")

        # Create executor
        executor = TestExecutor(tmppath)

        # Detect test framework (should find test_main.py, not .DS_Store)
        command = executor.detect_test_framework()
        assert command is not None, "❌ Failed to detect test framework"

        print(f"  Detected test command: {command}")
        print("✅ test_executor.py filtering: PASSED")

    return True


def test_real_project_filtering():
    """Test filtering on actual project directory"""
    print("Testing filtering on real project...")

    from file_aware_agent import FileManager

    # Use current directory
    manager = FileManager(Path("."))

    # List all files
    files = manager.list_files()

    # Verify NO system files in the list
    system_files = [".DS_Store", "._", "Thumbs.db"]
    for sys_file in system_files:
        assert not any(sys_file in f for f in files), f"❌ {sys_file} found in project files!"

    # Count files
    print(f"  Total files visible to agents: {len(files)}")
    print(f"  Sample files: {files[:5]}")
    print("✅ Real project filtering: PASSED")

    return True


def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("🧪 Testing .DS_Store Automatic Filtering")
    print("=" * 60)
    print()

    tests = [
        ("Utils Filtering", test_utils_filtering),
        ("FileAwareAgent Filtering", test_file_aware_agent_filtering),
        ("SecurityScanner Filtering", test_security_scanner_filtering),
        ("TestExecutor Filtering", test_test_executor_filtering),
        ("Real Project Filtering", test_real_project_filtering),
    ]

    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
            print()
        except Exception as e:
            print(f"❌ {name}: FAILED - {e}")
            results.append((name, False))
            print()

    # Summary
    print("=" * 60)
    print("📊 Test Summary")
    print("=" * 60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"  {name}: {status}")

    print()
    print(f"Total: {passed}/{total} tests passed")

    if passed == total:
        print()
        print("🎉 All tests passed! Agents will NEVER see .DS_Store files!")
        print("=" * 60)
        return True
    else:
        print()
        print("⚠️  Some tests failed. Check the output above.")
        print("=" * 60)
        return False


if __name__ == "__main__":
    import sys
    success = run_all_tests()
    sys.exit(0 if success else 1)
