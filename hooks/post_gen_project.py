#!/usr/bin/env python3
"""
Post-generation hook for cookiecutter template.
Performs small cleanup tasks after project generation.
"""

import os
import shutil


def main():
    """Main post-generation logic."""

    use_git_subrepo = "{{ cookiecutter.use_git_subrepo }}".lower()

    # Move git-subrepo files to archived if not using git-subrepo
    if use_git_subrepo != "y":
        print("📦 Git-subrepo not selected, archiving git-subrepo specific files...")

        # Define files to move
        files_to_archive = [
            ".claude/agents/git-subrepo-agent.md",
            ".claude/commands/subrepo-new.md",
        ]

        # Ensure archived directories exist
        os.makedirs("archived/.claude/agents", exist_ok=True)
        os.makedirs("archived/.claude/commands", exist_ok=True)

        # Move each file to archived location
        for file_path in files_to_archive:
            if os.path.exists(file_path):
                archive_path = os.path.join("archived", file_path)
                shutil.move(file_path, archive_path)
                print(f"  ✓ Moved {file_path} to archived/")

    print("✅ Post-generation cleanup completed!")
    print("🚀 Your agentic monorepo is ready!")
    print("\nNext steps:")
    print("1. cd {{ cookiecutter.project_slug }}")
    print("2. claude")
    print("3. /setup-monorepo")


if __name__ == "__main__":
    main()