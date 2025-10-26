# Agentic Monorepo Cookiecutter Template

A modern cookiecutter template for creating agentic monorepos with pnpm, moon, and git-subrepo support.

## Features

🚀 **Modern Tooling**
- [pnpm](https://pnpm.io/) - Fast, disk space efficient package manager
- [moon](https://moonrepo.dev/) - Build system and task runner for monorepos
- [git-subrepo](https://github.com/ingydotnet/git-subrepo) - Multi-repository management (optional)

🏗️ **Multi-Language Support**
- TypeScript libraries
- Python libraries
- Nim libraries
- Others can be added

🤖 **AI Agent Ready**
- Pre-configured Claude Code integration
- Agent orchestration patterns
- Development workflow automation

## Quick Start

### Prerequisites

**Template Generation:**
- Python 3.7+ (for cookiecutter)
- [cookiecutter](https://cookiecutter.readthedocs.io/) installed

```bash
pip install cookiecutter
```

**Generated Project Requirements:**
- [Node.js](https://nodejs.org/) 18+ (recommended: use [proto](https://moonrepo.dev/proto) for version management)
- [pnpm](https://pnpm.io/) - Fast package manager
- [moon](https://moonrepo.dev/) - Build system and task runner
- [Claude Code](https://claude.ai/code) - AI coding assistant
- [uv](https://docs.astral.sh/uv/) - Fast Python package manager (if using Python libraries)

**Optional Tools:**
- [proto](https://moonrepo.dev/proto) - Multi-language version manager (recommended)
 

**Installation Commands:**
```bash
# Install proto (recommended for version management)
curl -fsSL https://moonrepo.dev/install/proto.sh | bash

# Install Node.js and pnpm via proto
proto install node 22
proto install pnpm 10

# Install moon
npm install -g @moonrepo/cli

# Install uv (for Python projects)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install Claude Code
npm install -g @anthropic-ai/claude-code
```

### Generate Your Monorepo

```bash
cookiecutter https://github.com/yourusername/agentic-monorepo-template
# or locally:
cookiecutter /path/to/this/template
```

You'll be prompted for:

- **project_name**: Display name for your project
- **project_slug**: URL/folder-safe version of the name
- **project_description**: Brief description of your project
- **author_name**: Your name
- **author_email**: Your email address
- **github_username**: Your GitHub username
- **github_organization**: GitHub org (defaults to your username)
- **use_git_subrepo**: Enable git-subrepo support (y/n)
- **node_version**: Node.js version to use
- **pnpm_version**: pnpm version to use
- **moon_version**: moon version constraint
- **license**: License type

### After Generation

**First, ensure all required tools are installed** (see Prerequisites above), then:

```bash
cd your-project-slug
pnpm install
pnpm dev
```

## Template Structure

```
your-project-slug/
├── .claude/                 # Claude Code configuration
├── .moon/                   # Moon build system config
├── .vscode/                 # VS Code settings
├── apps/                    # Applications
├── libs/                    # Shared libraries
│   ├── typescript/          # TypeScript libraries
│   ├── python/              # Python libraries
│   └── nim/                 # Nim libraries
├── docs/                    # Documentation
├── experiments/             # Experimental code
├── third_party/             # Third-party dependencies
├── CLAUDE.md               # AI agent instructions
├── package.json            # Root package configuration
└── README.md               # Generated project README
```

## Development Workflow

The generated monorepo includes:

1. **Build System**: Moon orchestrates builds across all projects
2. **Package Management**: pnpm workspaces for efficient dependency management
3. **Version Control**: Optional git-subrepo for multi-repo management
4. **AI Integration**: Pre-configured Claude Code setup with agent patterns

### Available Scripts

- `moon run my-website:dev` - Run a subrepo's dev server via pnpm
- `pnpm dev` - Start development servers
- `pnpm build` - Build all projects
- `pnpm test` - Run all tests
- `pnpm lint` - Run linting

### Git-subrepo Commands (if enabled)

When git-subrepo is enabled, you can manage external repositories as subdirectories:

```bash
# Add external repo as subrepo
git subrepo clone <repository> <subdir>

# Update subrepo with upstream changes  
git subrepo pull <subdir>

# Push local changes to upstream
git subrepo push <subdir>

# Check subrepo status
git subrepo status [<subdir>]
```

Git-subrepo allows you to include external repositories directly in your monorepo without requiring users to install additional tools or manage submodules.

In regards to the monorepo, you may use standard git commands to manage it independent of git-subrepo.

## Customization

### Adding New Languages

To add support for additional languages:

1. Update `cookiecutter.json` with new options
2. Modify `hooks/post_gen_project.py` to handle new directories
3. Update `.moon/workspace.yml` template with new project patterns

### Extending Configuration

The template includes configuration for:
- Moon build system (`.moon/`)
- VS Code settings (`.vscode/`)
- Claude Code integration (`.claude/`)
- Environment variables (`.env.example`)

## Contributing

1. Fork this repository
2. Make your changes
3. Test with `cookiecutter .`
4. Submit a pull request

## License

This template is licensed under the Apache License 2.0. Generated projects use the license you select during generation.

## Acknowledgments

- Built with [Cookiecutter](https://github.com/cookiecutter/cookiecutter)
- Inspired by modern monorepo practices
- Designed for AI-assisted development workflows