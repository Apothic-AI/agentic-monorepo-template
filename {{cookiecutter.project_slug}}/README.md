# {{cookiecutter.project_name}}

{{cookiecutter.project_description}}

## Overview

This is a modern agentic monorepo template built with:

- **pnpm** - Fast, disk space efficient package manager
- **moon** - Build system and task runner for monorepos
{% if cookiecutter.use_git_subrepo == 'y' -%}
- **git-subrepo** - Multi-repository management
{% endif -%}
- **TypeScript** - Type-safe JavaScript
{% if cookiecutter.include_python_libs == 'y' -%}
- **Python** - Support for Python libraries
{% endif -%}
{% if cookiecutter.include_nim_libs == 'y' -%}
- **Nim** - Support for Nim libraries
{% endif -%}

## Structure

```
{{cookiecutter.project_slug}}/
├── apps/              # Applications
├── libs/              # Shared libraries
{% if cookiecutter.include_typescript_libs == 'y' -%}
│   ├── typescript/    # TypeScript libraries
{% endif -%}
{% if cookiecutter.include_python_libs == 'y' -%}
│   ├── python/        # Python libraries
{% endif -%}
{% if cookiecutter.include_nim_libs == 'y' -%}
│   └── nim/           # Nim libraries
{% endif -%}
├── docs/              # Documentation
├── experiments/       # Experimental code
└── third_party/       # Third-party dependencies
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