# {{cookiecutter.project_name}}

{{cookiecutter.project_description}}

## Overview

This is a modern agentic monorepo built with:

- **pnpm** - Fast, disk space efficient package manager
- **moon** - Build system and task runner for monorepos
{% if cookiecutter.use_git_subrepo == 'y' -%}
- **git-subrepo** - Multi-repository management
{% endif -%}
- **Multi-language support** - TypeScript, JavaScript, Python, Rust, Go, Nim, Zig, C, Java, PHP, Ruby, (and any others really)

## Structure

```
{{cookiecutter.project_slug}}/
├── .claude/           # Claude Code agent configuration
├── .moon/             # Moon build system config
├── projects/
│   ├── apps/          # Applications
│   ├── experiments/   # Experimental code
│   ├── libs/          # Shared libraries (by language)
│   │   ├── c/
│   │   ├── go/
│   │   ├── java/
│   │   ├── javascript/
│   │   ├── nim/
│   │   ├── php/
│   │   ├── python/
│   │   ├── ruby/
│   │   ├── rust/
│   │   ├── typescript/
│   │   └── zig/
│   └── third_party/   # Third-party dependencies
├── bin/               # Utility scripts
├── docs/              # Documentation
└── logs/              # Log files
```

## Getting Started

1. Install dependencies:
```bash
pnpm install
```

2. Run development servers:
```bash
pnpm dev
```

3. Build all projects:
```bash
pnpm build
```

4. Run tests:
```bash
pnpm test
```

## Development

This monorepo uses [moon](https://moonrepo.dev/) for build orchestration and task management. Each project can have its own tasks defined in `moon.yml` files.

### Environment Variables

Each project may have its own environment files:
- `.dev.vars` - Development variables
- `.env` - Environment variables
- `.env.local` - Local overrides

## License

{{cookiecutter.license}}

## Author

{{cookiecutter.author_name}} <{{cookiecutter.author_email}}>