"""
Git Integration System
Provides automatic version control for AI-generated projects
"""

import subprocess
from pathlib import Path
from typing import Optional, Dict, List
import colorama

colorama.init(autoreset=True)


class GitIntegration:
    """
    Manages Git operations for AI-generated projects
    Provides automatic commits, branching, and version history
    """

    def __init__(self, project_path: str, auto_commit: bool = True):
        """
        Initialize Git integration

        Args:
            project_path: Path to the project directory
            auto_commit: Whether to automatically commit changes
        """
        self.project_path = Path(project_path)
        self.auto_commit = auto_commit
        self.initialized = False

    def init_repository(self) -> bool:
        """
        Initialize a Git repository in the project directory

        Returns:
            True if successful or already initialized
        """
        try:
            # Check if already a git repo
            git_dir = self.project_path / ".git"
            if git_dir.exists():
                print(colorama.Fore.YELLOW + "  📁 Git repository already exists" + colorama.Style.RESET_ALL)
                self.initialized = True
                return True

            # Initialize repository
            result = subprocess.run(
                ['git', 'init'],
                cwd=self.project_path,
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                print(colorama.Fore.GREEN + "  ✓ Git repository initialized" + colorama.Style.RESET_ALL)

                # Configure git
                self._configure_git()

                # Create initial commit
                self._initial_commit()

                self.initialized = True
                return True
            else:
                print(colorama.Fore.RED + f"  ✗ Failed to initialize git: {result.stderr}" + colorama.Style.RESET_ALL)
                return False

        except FileNotFoundError:
            print(colorama.Fore.RED + "  ✗ Git not installed. Install git to enable version control." + colorama.Style.RESET_ALL)
            return False
        except Exception as e:
            print(colorama.Fore.RED + f"  ✗ Git initialization error: {e}" + colorama.Style.RESET_ALL)
            return False

    def _configure_git(self):
        """Configure git settings"""
        # Set user for commits
        subprocess.run(
            ['git', 'config', 'user.name', 'AI Agent'],
            cwd=self.project_path,
            capture_output=True
        )
        subprocess.run(
            ['git', 'config', 'user.email', 'agent@ai-project-builder.local'],
            cwd=self.project_path,
            capture_output=True
        )

        # Set main as default branch
        subprocess.run(
            ['git', 'config', 'init.defaultBranch', 'main'],
            cwd=self.project_path,
            capture_output=True
        )

    def _initial_commit(self):
        """Create initial commit with .gitignore"""
        # Create .gitignore
        gitignore_content = """# AI Project Builder
*.backup
*.pyc
__pycache__/
.pytest_cache/
.coverage
*.log
.env
node_modules/
dist/
build/
*.egg-info/
.DS_Store
"""

        gitignore_path = self.project_path / ".gitignore"
        with open(gitignore_path, 'w') as f:
            f.write(gitignore_content)

        # Initial commit
        subprocess.run(['git', 'add', '.gitignore'], cwd=self.project_path, capture_output=True)
        subprocess.run(
            ['git', 'commit', '-m', '🎉 Initial commit - AI Project Builder'],
            cwd=self.project_path,
            capture_output=True
        )

    def commit_changes(self, agent_name: str, iteration: int, message: str, files: List[str] = None) -> bool:
        """
        Commit current changes

        Args:
            agent_name: Name of the agent making changes
            iteration: Current iteration number
            message: Commit message describing changes
            files: Optional list of specific files to commit (default: all changes)

        Returns:
            True if commit successful
        """
        if not self.initialized:
            print(colorama.Fore.YELLOW + "  ⚠️  Git not initialized, skipping commit" + colorama.Style.RESET_ALL)
            return False

        try:
            # Add files
            if files:
                for file in files:
                    subprocess.run(['git', 'add', file], cwd=self.project_path, capture_output=True)
            else:
                subprocess.run(['git', 'add', '.'], cwd=self.project_path, capture_output=True)

            # Check if there are changes to commit
            status_result = subprocess.run(
                ['git', 'status', '--porcelain'],
                cwd=self.project_path,
                capture_output=True,
                text=True
            )

            if not status_result.stdout.strip():
                print(colorama.Fore.YELLOW + "  📝 No changes to commit" + colorama.Style.RESET_ALL)
                return True

            # Create commit message
            commit_msg = f"[Iteration {iteration}] {agent_name}: {message}\n\n🤖 Generated by AI Project Builder"

            # Commit
            result = subprocess.run(
                ['git', 'commit', '-m', commit_msg],
                cwd=self.project_path,
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                # Count files changed
                files_changed = len([line for line in status_result.stdout.split('\n') if line.strip()])
                print(colorama.Fore.GREEN + f"  ✓ Committed {files_changed} file(s)" + colorama.Style.RESET_ALL)
                return True
            else:
                print(colorama.Fore.RED + f"  ✗ Commit failed: {result.stderr}" + colorama.Style.RESET_ALL)
                return False

        except Exception as e:
            print(colorama.Fore.RED + f"  ✗ Commit error: {e}" + colorama.Style.RESET_ALL)
            return False

    def create_branch(self, branch_name: str) -> bool:
        """
        Create a new branch

        Args:
            branch_name: Name of the branch to create

        Returns:
            True if successful
        """
        if not self.initialized:
            return False

        try:
            # Sanitize branch name
            branch_name = branch_name.lower().replace(' ', '-').replace('_', '-')
            branch_name = ''.join(c for c in branch_name if c.isalnum() or c == '-')

            result = subprocess.run(
                ['git', 'checkout', '-b', branch_name],
                cwd=self.project_path,
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                print(colorama.Fore.GREEN + f"  ✓ Created and switched to branch '{branch_name}'" + colorama.Style.RESET_ALL)
                return True
            else:
                print(colorama.Fore.RED + f"  ✗ Failed to create branch: {result.stderr}" + colorama.Style.RESET_ALL)
                return False

        except Exception as e:
            print(colorama.Fore.RED + f"  ✗ Branch creation error: {e}" + colorama.Style.RESET_ALL)
            return False

    def switch_branch(self, branch_name: str) -> bool:
        """
        Switch to an existing branch

        Args:
            branch_name: Name of the branch to switch to

        Returns:
            True if successful
        """
        if not self.initialized:
            return False

        try:
            result = subprocess.run(
                ['git', 'checkout', branch_name],
                cwd=self.project_path,
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                print(colorama.Fore.GREEN + f"  ✓ Switched to branch '{branch_name}'" + colorama.Style.RESET_ALL)
                return True
            else:
                print(colorama.Fore.RED + f"  ✗ Failed to switch branch: {result.stderr}" + colorama.Style.RESET_ALL)
                return False

        except Exception as e:
            print(colorama.Fore.RED + f"  ✗ Branch switch error: {e}" + colorama.Style.RESET_ALL)
            return False

    def get_diff(self, staged: bool = False) -> str:
        """
        Get current diff

        Args:
            staged: If True, show staged changes only

        Returns:
            Diff output as string
        """
        if not self.initialized:
            return ""

        try:
            cmd = ['git', 'diff']
            if staged:
                cmd.append('--staged')

            result = subprocess.run(
                cmd,
                cwd=self.project_path,
                capture_output=True,
                text=True
            )

            return result.stdout

        except Exception as e:
            print(colorama.Fore.RED + f"  ✗ Diff error: {e}" + colorama.Style.RESET_ALL)
            return ""

    def get_log(self, max_count: int = 10) -> List[Dict]:
        """
        Get commit history

        Args:
            max_count: Maximum number of commits to retrieve

        Returns:
            List of commit dictionaries
        """
        if not self.initialized:
            return []

        try:
            result = subprocess.run(
                ['git', 'log', f'-{max_count}', '--pretty=format:%H|%an|%ae|%ad|%s'],
                cwd=self.project_path,
                capture_output=True,
                text=True
            )

            commits = []
            for line in result.stdout.strip().split('\n'):
                if line:
                    parts = line.split('|')
                    if len(parts) >= 5:
                        commits.append({
                            'hash': parts[0],
                            'author': parts[1],
                            'email': parts[2],
                            'date': parts[3],
                            'message': '|'.join(parts[4:])
                        })

            return commits

        except Exception as e:
            print(colorama.Fore.RED + f"  ✗ Log error: {e}" + colorama.Style.RESET_ALL)
            return []

    def get_status(self) -> Dict:
        """
        Get current repository status

        Returns:
            Dictionary with status information
        """
        if not self.initialized:
            return {"initialized": False}

        try:
            # Get current branch
            branch_result = subprocess.run(
                ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
                cwd=self.project_path,
                capture_output=True,
                text=True
            )
            current_branch = branch_result.stdout.strip()

            # Get status
            status_result = subprocess.run(
                ['git', 'status', '--porcelain'],
                cwd=self.project_path,
                capture_output=True,
                text=True
            )

            # Count changes
            modified = []
            added = []
            deleted = []
            untracked = []

            for line in status_result.stdout.strip().split('\n'):
                if not line:
                    continue

                status_code = line[:2]
                filename = line[3:]

                if status_code.strip() == 'M':
                    modified.append(filename)
                elif status_code.strip() == 'A':
                    added.append(filename)
                elif status_code.strip() == 'D':
                    deleted.append(filename)
                elif status_code.strip() == '??':
                    untracked.append(filename)

            return {
                "initialized": True,
                "current_branch": current_branch,
                "modified": modified,
                "added": added,
                "deleted": deleted,
                "untracked": untracked,
                "has_changes": bool(modified or added or deleted or untracked)
            }

        except Exception as e:
            print(colorama.Fore.RED + f"  ✗ Status error: {e}" + colorama.Style.RESET_ALL)
            return {"initialized": True, "error": str(e)}

    def tag_version(self, version: str, message: str = None) -> bool:
        """
        Create a version tag

        Args:
            version: Version tag (e.g., 'v1.0.0')
            message: Optional tag message

        Returns:
            True if successful
        """
        if not self.initialized:
            return False

        try:
            cmd = ['git', 'tag']
            if message:
                cmd.extend(['-a', version, '-m', message])
            else:
                cmd.append(version)

            result = subprocess.run(
                cmd,
                cwd=self.project_path,
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                print(colorama.Fore.GREEN + f"  ✓ Created tag '{version}'" + colorama.Style.RESET_ALL)
                return True
            else:
                print(colorama.Fore.RED + f"  ✗ Failed to create tag: {result.stderr}" + colorama.Style.RESET_ALL)
                return False

        except Exception as e:
            print(colorama.Fore.RED + f"  ✗ Tag error: {e}" + colorama.Style.RESET_ALL)
            return False

    def rollback_to_commit(self, commit_hash: str, hard: bool = False) -> bool:
        """
        Rollback to a specific commit

        Args:
            commit_hash: The commit hash to rollback to
            hard: If True, discard all changes (use with caution)

        Returns:
            True if successful
        """
        if not self.initialized:
            return False

        try:
            reset_type = 'hard' if hard else 'soft'

            result = subprocess.run(
                ['git', 'reset', f'--{reset_type}', commit_hash],
                cwd=self.project_path,
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                print(colorama.Fore.GREEN + f"  ✓ Rolled back to commit {commit_hash[:7]}" + colorama.Style.RESET_ALL)
                return True
            else:
                print(colorama.Fore.RED + f"  ✗ Rollback failed: {result.stderr}" + colorama.Style.RESET_ALL)
                return False

        except Exception as e:
            print(colorama.Fore.RED + f"  ✗ Rollback error: {e}" + colorama.Style.RESET_ALL)
            return False


# Example usage
if __name__ == "__main__":
    import tempfile
    import shutil

    # Create temp project
    with tempfile.TemporaryDirectory() as tmpdir:
        print(f"\n🧪 Testing Git Integration in: {tmpdir}\n")

        git = GitIntegration(tmpdir)

        # Test 1: Initialize repository
        print("Test 1: Initialize repository")
        assert git.init_repository() == True

        # Test 2: Create a file and commit
        print("\nTest 2: Create file and commit")
        test_file = Path(tmpdir) / "test.py"
        test_file.write_text("print('Hello, World!')")

        assert git.commit_changes("TestAgent", 1, "Add test file") == True

        # Test 3: Get status
        print("\nTest 3: Get status")
        status = git.get_status()
        print(f"  Current branch: {status['current_branch']}")
        print(f"  Has changes: {status['has_changes']}")

        # Test 4: Create branch
        print("\nTest 4: Create branch")
        assert git.create_branch("feature-test") == True

        # Test 5: Get log
        print("\nTest 5: Get commit log")
        commits = git.get_log(max_count=5)
        print(f"  Total commits: {len(commits)}")
        for commit in commits:
            print(f"    - {commit['hash'][:7]}: {commit['message']}")

        # Test 6: Get diff
        print("\nTest 6: Make changes and get diff")
        test_file.write_text("print('Hello, Git!')")
        diff = git.get_diff()
        print(f"  Diff length: {len(diff)} characters")

        print("\n✅ All tests passed!")
