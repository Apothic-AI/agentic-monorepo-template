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
    use_moon = "{{ cookiecutter.use_moon }}".lower()

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

    # Move moon files to archived if not using moon
    if use_moon != "y":
        print("📦 Moon not selected, archiving moon specific files...")

        # Define directories and files to move
        moon_items = [
            ".moon",
        ]

        # Ensure archived directory exists
        os.makedirs("archived", exist_ok=True)

        # Move each item to archived location
        for item_path in moon_items:
            if os.path.exists(item_path):
                archive_path = os.path.join("archived", item_path)
                if os.path.isdir(item_path):
                    shutil.move(item_path, archive_path)
                    print(f"  ✓ Moved {item_path}/ to archived/")
                else:
                    shutil.move(item_path, archive_path)
                    print(f"  ✓ Moved {item_path} to archived/")

    print("✅ Post-generation cleanup completed!")
    print("🚀 Your agentic monorepo is ready!")
    print("\nNext steps:")
    print("1. cd {{ cookiecutter.project_slug }}")
    print("2. claude")
    print("3. /setup-monorepo")


if __name__ == "__main__":
    main()