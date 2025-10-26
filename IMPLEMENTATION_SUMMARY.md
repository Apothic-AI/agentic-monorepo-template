# Git-Subrepo Conditional Implementation Summary

This document summarizes the changes made to make git-subrepo features conditional based on the `use_git_subrepo` cookiecutter variable.

## Changes Made

### 1. Post-Generation Hook (`hooks/post_gen_project.py`)

**Updated:** Added logic to move git-subrepo specific files to archived when `use_git_subrepo != 'y'`

Files that get archived when git-subrepo is not selected:
- `.claude/agents/git-subrepo-agent.md`
- `.claude/commands/subrepo-new.md`

These files are moved to:
- `archived/.claude/agents/git-subrepo-agent.md`
- `archived/.claude/commands/subrepo-new.md`

### 2. CLAUDE.md Template

**Updated:** Added Jinja2 conditionals for git-subrepo content:

- Architecture description: "Git-subrepo monorepo" vs "Monorepo"
- Core Technologies: conditionally includes "git-subrepo"
- Project Dependencies: conditional descriptions about git-subrepo organization
- Progress Tracking: conditional mention of subrepo PLANNING_AND_PROGRESS.md files
- git-subrepo section: entire section wrapped in `{% if cookiecutter.use_git_subrepo == 'y' %}`
- Strategic Planning: conditional mention of git-subrepo workflow implications
- Agent Orchestration: conditional mention of subrepo-specific agents
- New Projects section: "New Projects/Subrepos" vs "New Projects"

### 3. orchestrate.md Command

**Updated:** Wrapped git-subrepo-agent reference in conditional:
```markdown
**Repository Management:**
{% if cookiecutter.use_git_subrepo == 'y' -%}
- `git-subrepo-agent`: ...
{% endif -%}
```

### 4. setup-monorepo.md Command

**Updated:** Made subrepo cloning instructions conditional:
- When `use_git_subrepo == 'y'`: mentions cloning/initializing subrepos
- When `use_git_subrepo != 'y'`: generic project creation language

### 5. README.md Template (Generated Project)

**Already conditional:** The project README template already had conditionals for git-subrepo features.

### 6. workspace.yml Template

**Already conditional:** The moon workspace.yml already conditionally enables `gitV2: true` experiment when git-subrepo is enabled.

## Files That Remain Unchanged

The following files don't need changes as they either:
- Don't reference git-subrepo
- Will be moved to archived by the post-generation hook
- Already have appropriate conditionals

## Testing the Template

To test both scenarios:

**With git-subrepo:**
```bash
cookiecutter /home/bitnom/Code/agentic-monorepo
# Select 'y' for use_git_subrepo
```

**Without git-subrepo:**
```bash
cookiecutter /home/bitnom/Code/agentic-monorepo
# Select 'n' for use_git_subrepo
```

Then verify:
1. Git-subrepo agent and commands are in correct location (active vs archived)
2. CLAUDE.md has appropriate content (mentions or omits git-subrepo)
3. Documentation reflects correct architecture
4. No broken references to git-subrepo when disabled

## Expected Behavior

### When `use_git_subrepo == 'y'`:
- All git-subrepo agents and commands are active in `.claude/`
- Documentation mentions git-subrepo features
- Architecture described as "Git-subrepo monorepo"
- Setup instructions mention subrepo cloning

### When `use_git_subrepo == 'n'`:
- Git-subrepo agent and commands moved to `archived/.claude/`
- Documentation omits git-subrepo references
- Architecture described as "Monorepo"
- Setup instructions focus on general project creation

## Implementation Complete ✅

All git-subrepo features are now properly conditional based on user selection during cookiecutter generation.
