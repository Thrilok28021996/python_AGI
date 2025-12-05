from langchain.prompts.chat import SystemMessagePromptTemplate
from assistant_prompt import assistant_inception_prompt
from user_prompt import user_inception_prompt
from pathlib import Path
from typing import Iterator, List


# System files that agents should NEVER see or process
SYSTEM_IGNORE_FILES = {
    '.DS_Store',
    '.DS_Store?',
    '._*',
    'Thumbs.db',
    'ehthumbs.db',
    '.Spotlight-V100',
    '.Trashes',
    'desktop.ini',
}

# Directories that agents should skip
SYSTEM_IGNORE_DIRS = {
    '__pycache__',
    '.git',
    '.svn',
    '.hg',
    'node_modules',
    '.pytest_cache',
    '.mypy_cache',
    '.tox',
    'venv',
    '.venv',
    'env',
    '.env',
}


def should_ignore_file(file_path: Path) -> bool:
    """
    Check if a file should be ignored by agents

    Args:
        file_path: Path object to check

    Returns:
        True if file should be ignored, False otherwise
    """
    filename = file_path.name

    # Check exact matches
    if filename in SYSTEM_IGNORE_FILES:
        return True

    # Check patterns (._*, etc.)
    if filename.startswith('._'):
        return True

    # Check backup files
    if filename.endswith('.backup') or filename.endswith('.bak'):
        return True

    return False


def should_ignore_directory(dir_path: Path) -> bool:
    """
    Check if a directory should be ignored by agents

    Args:
        dir_path: Path object to check

    Returns:
        True if directory should be ignored, False otherwise
    """
    dirname = dir_path.name

    # Check exact matches
    if dirname in SYSTEM_IGNORE_DIRS:
        return True

    # Hidden directories (starting with .)
    if dirname.startswith('.') and dirname not in {'.', '..'}:
        return True

    return False


def filter_paths(paths: Iterator[Path]) -> List[Path]:
    """
    Filter out system files and directories from a list of paths

    Args:
        paths: Iterator of Path objects

    Returns:
        Filtered list of paths excluding system files
    """
    filtered = []
    for path in paths:
        if path.is_file() and not should_ignore_file(path):
            filtered.append(path)
        elif path.is_dir() and not should_ignore_directory(path):
            filtered.append(path)
    return filtered


# Create a helper to get system messages for AI assistant
# and AI user from role names and the task


def get_sys_msgs(assistant_role_name: str, user_role_name: str, task: str):
    assistant_sys_template = SystemMessagePromptTemplate.from_template(
        template=assistant_inception_prompt
    )
    assistant_sys_msg = assistant_sys_template.format_messages(
        assistant_role_name=assistant_role_name,
        user_role_name=user_role_name,
        task=task,
    )[0]

    user_sys_template = SystemMessagePromptTemplate.from_template(
        template=user_inception_prompt
    )
    user_sys_msg = user_sys_template.format_messages(
        assistant_role_name=assistant_role_name,
        user_role_name=user_role_name,
        task=task,
    )[0]

    return assistant_sys_msg, user_sys_msg
