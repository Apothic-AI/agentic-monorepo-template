#!/usr/bin/env python3
"""
Post-generation hook for cookiecutter template.
Performs small cleanup tasks after project generation.
"""


def main():
    """Main post-generation logic."""

    # Post-generation cleanup currently has no conditional removals.
    # Agent-related features were removed from the template.

    print("✅ Post-generation cleanup completed!")
    print("🚀 Your agentic monorepo is ready!")
    print("\nNext steps:")
    print("1. cd {{ cookiecutter.project_slug }}")
    print("2. claude")
    print("3. /setup-monorepo")


if __name__ == "__main__":
    main()