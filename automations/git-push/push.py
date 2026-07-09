#!/usr/bin/env python3
"""
Auto-push script for Oxy OS.
Generates conventional commit messages and pushes changes to GitHub.
"""

import subprocess
import sys
from pathlib import Path
from datetime import datetime


def run_cmd(cmd, check=True):
    """Run a shell command and return output."""
    result = subprocess.run(
        cmd,
        shell=True,
        capture_output=True,
        text=True,
        cwd=Path(__file__).parent.parent.parent
    )
    if check and result.returncode != 0:
        print(f"Error running '{cmd}': {result.stderr}")
        sys.exit(1)
    return result.stdout.strip(), result.returncode


def get_changed_files():
    """Get list of changed files (staged and unstaged)."""
    # Get all changes including new files
    output, _ = run_cmd("git status --porcelain", check=False)
    if not output:
        return []
    
    files = []
    for line in output.split('\n'):
        line = line.strip()
        if line:
            # Format: "?? file.txt" or "M  file.txt" - get the path (skip first 2 chars for status + space)
            # Handle both porcelain formats
            if ' ' in line:
                files.append(line[3:].strip())
    return files


def determine_commit_type(files):
    """Map changed files to conventional commit types."""
    if not files:
        return None
    
    # Check for automations (features)
    for f in files:
        if f.startswith('automations/') and not f.endswith('.md'):
            return 'feat'
    
    # Check for documentation
    doc_files = [f for f in files if f.endswith('.md') or f == '.gitignore']
    if len(doc_files) == len(files):
        return 'docs'
    
    # Check for bug fixes (changes to existing code)
    for f in files:
        if f.endswith('.py') and not f.startswith('automations/git-push/'):
            return 'fix'
    
    return 'chore'


def generate_commit_message(files, commit_type):
    """Generate a conventional commit message."""
    if not files:
        return None
    
    if commit_type == 'feat':
        # Find the automation/script name
        for f in files:
            if f.startswith('automations/') and f != 'automations/git-push/push.py':
                name = f.split('/')[1]
                return f"feat: add {name} automation"
        return "feat: add new automation"
    
    elif commit_type == 'docs':
        changed_docs = [f.split('/')[-1] for f in files if f.endswith('.md') or f == '.gitignore']
        if changed_docs:
            return f"docs: update {', '.join(changed_docs)}"
        return "docs: update documentation"
    
    elif commit_type == 'fix':
        name = files[0].split('/')[-1] if files else "code"
        return f"fix: update {name}"
    
    return "chore: update files"


def push_to_git(message=None):
    """Stage all changes, commit, and push to GitHub."""
    # Check if we're in a git repo
    output, code = run_cmd("git rev-parse --is-inside-work-tree", check=False)
    if code != 0:
        print("Error: Not a git repository")
        return False
    
    # Get changed files
    files = get_changed_files()
    if not files:
        print("No changes to commit")
        return True
    
    print(f"Changed files: {files}")
    
    # Determine commit type and message
    commit_type = determine_commit_type(files)
    if commit_type is None:
        print("No commit needed")
        return True
    
    msg = message or generate_commit_message(files, commit_type)
    print(f"Commit message: {msg}")
    
    # Stage all changes
    run_cmd("git add .")
    
    # Commit
    run_cmd(f'git commit -m "{msg}"')
    
    # Push
    output, code = run_cmd("git push", check=False)
    if code != 0:
        print(f"Push failed: {output}")
        return False
    
    print("Successfully pushed to GitHub!")
    return True


if __name__ == "__main__":
    # Allow optional custom message
    custom_msg = sys.argv[1] if len(sys.argv) > 1 else None
    push_to_git(custom_msg)