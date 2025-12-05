"""
.DS_Store File Handler Utility

This module provides utilities to handle .DS_Store files in the project:
- Detect .DS_Store files
- Remove .DS_Store files
- Filter out .DS_Store files from file lists
- Prevent .DS_Store-related errors
"""

import os
from pathlib import Path
from typing import List, Set


class DSStoreHandler:
    """Handler for managing .DS_Store files"""

    # Files and directories to ignore
    IGNORE_FILES = {'.DS_Store', '.DS_Store?', '._*', 'Thumbs.db', 'ehthumbs.db'}
    IGNORE_DIRS = {'__pycache__', '.git', '.pytest_cache', 'node_modules', 'venv', '.venv'}

    @staticmethod
    def is_ds_store_file(path: str) -> bool:
        """
        Check if a file is a .DS_Store or similar system file

        Args:
            path: Path to check

        Returns:
            True if file should be ignored, False otherwise
        """
        filename = os.path.basename(path)

        # Check exact matches
        if filename in DSStoreHandler.IGNORE_FILES:
            return True

        # Check patterns (._*)
        if filename.startswith('._'):
            return True

        return False

    @staticmethod
    def should_ignore_directory(path: str) -> bool:
        """
        Check if a directory should be ignored

        Args:
            path: Directory path to check

        Returns:
            True if directory should be ignored
        """
        dirname = os.path.basename(path)
        return dirname in DSStoreHandler.IGNORE_DIRS or dirname.startswith('.')

    @staticmethod
    def filter_files(file_list: List[str]) -> List[str]:
        """
        Filter out .DS_Store and system files from a list

        Args:
            file_list: List of file paths

        Returns:
            Filtered list without system files
        """
        return [
            f for f in file_list
            if not DSStoreHandler.is_ds_store_file(f)
        ]

    @staticmethod
    def find_ds_store_files(root_path: str = ".") -> List[str]:
        """
        Find all .DS_Store files in the project

        Args:
            root_path: Root directory to search from

        Returns:
            List of .DS_Store file paths
        """
        ds_store_files = []

        for root, dirs, files in os.walk(root_path):
            # Skip ignored directories
            dirs[:] = [d for d in dirs if not DSStoreHandler.should_ignore_directory(d)]

            # Find .DS_Store files
            for file in files:
                file_path = os.path.join(root, file)
                if DSStoreHandler.is_ds_store_file(file_path):
                    ds_store_files.append(file_path)

        return ds_store_files

    @staticmethod
    def remove_ds_store_files(root_path: str = ".", dry_run: bool = False) -> int:
        """
        Remove all .DS_Store files from the project

        Args:
            root_path: Root directory to clean
            dry_run: If True, only list files without deleting

        Returns:
            Number of files removed (or would be removed in dry run)
        """
        ds_store_files = DSStoreHandler.find_ds_store_files(root_path)

        if dry_run:
            print(f"🔍 Found {len(ds_store_files)} .DS_Store file(s) (dry run):")
            for file in ds_store_files:
                print(f"  - {file}")
            return len(ds_store_files)

        removed_count = 0
        for file in ds_store_files:
            try:
                os.remove(file)
                removed_count += 1
                print(f"✅ Removed: {file}")
            except Exception as e:
                print(f"❌ Failed to remove {file}: {e}")

        return removed_count

    @staticmethod
    def get_clean_file_list(directory: str, extensions: List[str] = None) -> List[str]:
        """
        Get a clean list of files, excluding .DS_Store and system files

        Args:
            directory: Directory to scan
            extensions: Optional list of file extensions to include (e.g., ['.py', '.txt'])

        Returns:
            List of clean file paths
        """
        clean_files = []

        for root, dirs, files in os.walk(directory):
            # Skip ignored directories
            dirs[:] = [d for d in dirs if not DSStoreHandler.should_ignore_directory(d)]

            for file in files:
                file_path = os.path.join(root, file)

                # Skip system files
                if DSStoreHandler.is_ds_store_file(file_path):
                    continue

                # Check extensions if specified
                if extensions:
                    if not any(file.endswith(ext) for ext in extensions):
                        continue

                clean_files.append(file_path)

        return clean_files


def cleanup_project(root_path: str = ".") -> None:
    """
    Main cleanup function to remove all .DS_Store files from project

    Args:
        root_path: Root directory to clean (default: current directory)
    """
    print("🧹 Starting .DS_Store cleanup...")
    print("")

    handler = DSStoreHandler()

    # Find files first
    ds_files = handler.find_ds_store_files(root_path)

    if not ds_files:
        print("✅ No .DS_Store files found. Your project is clean!")
        return

    print(f"Found {len(ds_files)} .DS_Store file(s):")
    for file in ds_files:
        print(f"  - {file}")
    print("")

    # Remove files
    removed = handler.remove_ds_store_files(root_path, dry_run=False)

    print("")
    print(f"🎉 Cleanup complete! Removed {removed} file(s).")


if __name__ == "__main__":
    import sys

    # Parse arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "--dry-run":
            print("🔍 Dry run mode - no files will be deleted")
            print("")
            handler = DSStoreHandler()
            count = handler.remove_ds_store_files(".", dry_run=True)
            print("")
            print(f"Would remove {count} file(s)")
        elif sys.argv[1] == "--help":
            print("Usage:")
            print("  python ds_store_handler.py           # Remove all .DS_Store files")
            print("  python ds_store_handler.py --dry-run # Show what would be removed")
            print("  python ds_store_handler.py --help    # Show this help")
        else:
            print(f"Unknown option: {sys.argv[1]}")
            print("Run with --help for usage information")
    else:
        cleanup_project()
