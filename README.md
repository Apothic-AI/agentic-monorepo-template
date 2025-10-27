# Agentic Monorepo Cookiecutter Template

A modern cookiecutter template for creating agentic monorepos with pnpm and optional moon, proto, and git-subrepo support.

## Message From The Author

Our Claude Code-managed monorepo performs extremely well. This template is an attempt to share that performance with others. However, this is only a slice of the original prompts, scripts, and structures. Its performance *SHOULD* be relative to ours but that is not verified or guaranteed. Not yet anyway.

Also, this template is not production-ready. This could amount to bugs in the cookiecutter scripting. It is being shared untested due to some requests for it on Discord.

**MCP**: We have been developing a SOTA MCP system. As such, I am not yet adding any MCP configs in this project since I'm about to replace them. Howevever, I do recommend that you at least use these since they are in the prompts:

**playwright**: `npx @playwright/mcp@latest --extension` * *Requires installing the playwright extension in Chrome*

**exa**: `https://mcp.exa.ai/mcp`

## Features

🚀 **Modern Tooling**
- [pnpm](https://pnpm.io/) - Fast, disk space efficient package manager
- [moon](https://moonrepo.dev/) - Build system and task runner for monorepos (optional)
- [proto](https://moonrepo.dev/proto) - Multi-language version manager (optional)
- [git-subrepo](https://github.com/ingydotnet/git-subrepo) - Multi-repository management (optional)

🏗️ **Multi-Language Support**
- TypeScript, JavaScript
- Python
- Rust, Go, Nim, Zig
- C, Java, PHP, Ruby
- Extensible structure for additional languages

🤖 **AI Agent Ready**
- Pre-configured Claude Code integration
- Agent orchestration patterns
- Development workflow automation

## Quick Start

### Prerequisites

**Template Generation:**
- Python 3.7+ (for cookiecutter)
- `uv` recommended

**Generated Project Requirements:**
- [Node.js](https://nodejs.org/) 18+ (can be managed with [proto](https://moonrepo.dev/proto) if enabled)
- [pnpm](https://pnpm.io/) - Fast package manager
- [Claude Code](https://claude.ai/code) - AI coding assistant
- [uv](https://docs.astral.sh/uv/) - Fast Python package manager (if using Python libraries)

**Optional Tools (based on template choices):**
- [proto](https://moonrepo.dev/proto) - Multi-language version manager (if `use_proto: y`)
- [moon](https://moonrepo.dev/) - Build system and task runner (if `use_moon: y`)
- [git-subrepo](https://github.com/ingydotnet/git-subrepo) - Multi-repository management (if `use_git_subrepo: y`)

### Generate Your Repo

```bash
uvx --with jinja2-time cookiecutter https://github.com/Apothic-AI/agentic-monorepo-template
# or locally:
uvx --with jinja2-time cookiecutter /path/to/this/template
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
- **use_moon**: Enable moon build system (y/n)
- **use_proto**: Enable proto version manager (y/n)
- **node_version**: Node.js version to use
- **pnpm_version**: pnpm version to use
- **moon_version**: moon version constraint (if moon enabled)
- **license**: License type

### After Generation

**First, ensure all required tools are installed** (see Prerequisites above), then:

```bash
cd your-project-slug
```

If you're using Claude Code (recommended):

```bash
claude
# Then use the /setup-monorepo command
```

Or manually:

```bash
pnpm install
pnpm dev
```

## Template Structure

```
your-project-slug/
├── .claude/                 # Claude Code configuration
│   ├── agents/              # Specialized AI agents
│   └── commands/            # Custom Claude Code commands
├── .moon/                   # Moon build system config (if moon enabled)
│   ├── tasks/               # Language-specific task definitions
│   ├── tasks.yml            # Global task definitions
│   ├── toolchain.yml        # Toolchain configuration (Node, Python)
│   └── workspace.yml        # Workspace and project discovery
├── .vscode/                 # VS Code settings
├── projects/
│   ├── apps/                # Applications
│   ├── experiments/         # Experimental code
│   ├── libs/                # Shared libraries by language
│   │   ├── c/
│   │   ├── go/
│   │   ├── java/
│   │   ├── javascript/
│   │   ├── nim/
│   │   ├── php/
│   │   ├── python/
│   │   ├── rust/
│   │   ├── typescript/
│   │   └── zig/
│   └── third_party/         # Third-party dependencies
├── archived/                # Archived/unused features
│   └── .claude/             # Conditional features (e.g., git-subrepo when disabled)
│   └── .moon/               # Moon config if not enabled
├── bin/                     # Utility scripts
├── docs/                    # Documentation
├── logs/                    # Log files
├── CLAUDE.md               # AI agent instructions
├── package.json            # Root package configuration
└── README.md               # Generated project README
```

## Development Workflow

The generated monorepo includes:

1. **Package Management**: pnpm workspaces for efficient dependency management
2. **Build System**: Optional moon for orchestrating builds across all projects
3. **Version Control**: Git with optional git-subrepo for multi-repo management
4. **Version Management**: Optional proto for managing Node.js, Python, and other language versions
5. **AI Integration**: Pre-configured Claude Code setup with agent patterns

### AI-Assisted Development

The template includes a comprehensive `.claude/` directory with:

- **Agents**: Specialized AI agents for different tasks (orchestration, research, testing, etc.)
- **Commands**: Custom Claude Code commands for common workflows
- **Instructions**: Context and guidelines in `CLAUDE.md` for AI-assisted development

Use the `/setup-monorepo` command in Claude Code to get started with an interactive setup process.

### Available Scripts

- `pnpm dev` - Start development servers{% if cookiecutter.use_moon == 'y' %} (runs `moon run :dev`){% endif %}
- `pnpm build` - Build all projects{% if cookiecutter.use_moon == 'y' %} (runs `moon run :build`){% endif %}
- `pnpm test` - Run all tests{% if cookiecutter.use_moon == 'y' %} (runs `moon run :test`){% endif %}
- `pnpm lint` - Run linting{% if cookiecutter.use_moon == 'y' %} (runs `moon run :lint`){% endif %}
{% if cookiecutter.use_moon == 'y' -%}
- `moon run <project>:<task>` - Run a specific task for a specific project
{%- endif %}

### Git-subrepo Commands (if enabled)

When git-subrepo is enabled during template generation (`use_git_subrepo: y`), you can manage external repositories as subdirectories:

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

**Note**: If you choose not to enable git-subrepo during generation, the git-subrepo agent and commands will be automatically moved to the `archived/` directory and git-subrepo references will be removed from documentation.

Git-subrepo allows you to include external repositories directly in your monorepo without requiring users to install additional tools or manage submodules. You can still use standard git commands to manage the monorepo itself.

## Customization

### Extending Configuration

The template includes configuration for:
- pnpm workspaces (always included)
- Moon build system (`.moon/` - optional)
- VS Code settings (`.vscode/`)
- Claude Code integration (`.claude/`)
- Environment variables (`.env.example`)

### Conditional Features

The template supports conditional features based on your choices during generation:

- **git-subrepo**: When disabled (`use_git_subrepo: n`), git-subrepo specific files are moved to `archived/` and all references are removed from documentation
- **moon**: When disabled (`use_moon: n`), the `.moon/` directory is moved to `archived/` and package.json uses placeholder scripts
- **proto**: When disabled (`use_proto: n`), installation instructions use standard Node.js/npm installation instead of proto
- **Multi-language support**: Add or remove language-specific configurations in `.moon/tasks/` as needed (if moon is enabled)

### Post-Generation Hook

The template includes a post-generation hook (`hooks/post_gen_project.py`) that:
- Moves git-subrepo files to archived when not selected
- Moves moon directory to archived when not selected
- Provides setup instructions
- Prepares the project for immediate use

## TODO

- MCP configs via SMCP

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