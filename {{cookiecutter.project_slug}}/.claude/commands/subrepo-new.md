The user wants to create a new subrepo in this git-subrepo monorepo. It may be that the user wants to initialize an empty subrepo, have you initialize the subrepo and then do some scaffolding, or clone an existing remote repo as a subrepo. Judge by what they supply.

---

**Information supplied by the user:**
$ARGUMENTS

---

If the user has not supplied enough information to create a new subrepo, tell the user what you need.

**If the user supplied a remote**

Use something like:
```bash
git subrepo clone <repo-url> <relative-monorepo-path>
```

If the user supplied a name, description, subdir path, but did not supply a remote:
```bash
git subrepo init <subdir>
```

---

**Subrepo Paths**

This monorepo contains the following subdirectories in which to store subrepos:

- apps/
- docs/
- libs/
- experiments/
- third_party/

If it is unclear where the new subrepo belongs, present the user with their options, and ask them.

Always add a PLANNING_AND_PROGRESS.md to the new subrepo. This will be used by an AI coding agent to track progress in the subrepo.

---

**Once the new subrepo is in-place**

- Analyze the new subrepo
{% if cookiecutter.use_moon == 'y' -%}
- Add an appropriate moon.yml config to the new subrepo.
{%- endif %}
- If the new subrepo already contains a package config (Like package.json) ensure it is properly configured to work with our pnpm workspace{% if cookiecutter.use_moon == 'y' %}, moon, etc{% endif %}.
- Add a new subsection for the new subrepo in the planning and progress section of CLAUDE.md
- Check to see if this monorepo's README.md contains a map of subrepos. If it does, add the new subrepo to it.

**Final Step**

Once the subrepo has been fully established, read all lines of all files in '.claude/agents', and create a new agent file. This will define a new agent's system prompt. The new agent should be geared towards working specifically on the new subrepo, and prompted to have the relevant expertise. Do not add anything to the prompt that instructs the agent to call upon other agents. Ensure the agent's prompt instructs it to always start by reading the subrepo's PLANNING_AND_PROGRESS.md, and to keep that file up to date as it plans and completes tasks. When defining a new agent, consider all the tools you have (Including MCP tools). Ensure the agent has access to everything it needs, and is prompted to use its tools in the most beneficial ways that will support development of that specific subrepo.
