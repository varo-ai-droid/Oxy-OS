# Claude Code Architecture Reference

> Complete summary of Claude Code's extension and configuration system for building an AI OS.

## 1. Memory System (CLAUDE.md Hierarchy)

**Loading order (first to last):**
1. `~/.claude/CLAUDE.md` - Global, all projects
2. `./CLAUDE.md` - Project root, share via git
3. `./CLAUDE.local.md` - Project root, gitignored, personal
4. Path-scoped files via `@import` syntax
5. Nested `CLAUDE.md` in subdirectories (lazy loaded)

**Auto Memory:**
- Stored in `~/.claude/MEMORY.md`
- Auto-generated from session learnings (build commands, debugging insights)
- First 200 lines or 25KB loaded into context
- Persists across sessions automatically

**Rules (`.claude/rules/*.md`):**
- Path-scoped via `paths:` frontmatter (gitignore-style patterns)
- Auto-load when matching files are read
- Lost on compaction; reloaded on next matching file read
- Keep under 200 lines total in CLAUDE.md

## 2. Settings System (4 Scopes, Precedence Low→High)

1. **Managed** (MDM/server-managed) - Cannot be overridden
2. **Command line** - Temporary session flags
3. **Local project** (`.claude/settings.local.json`) - Gitignored
4. **Shared project** (`.claude/settings.json`) - Committed to git
5. **User** (`~/.claude/settings.json`) - All projects

**Key settings keys:**
- `model` - Model alias or full name
- `permissions.defaultMode` - default/acceptEdits/plan/auto/dontAsk/bypassPermissions
- `permissions.allow/ask/deny` - Tool access rules
- `permissions.additionalDirectories` - Extra read/write access
- `sandbox.enabled` - OS-level isolation (macOS/Linux/WSL2)
- `env` - Environment variables
- `autoUpdatesChannel` - latest/stable
- `effortLevel` - low/medium/high/xhigh (not max/ultracode)
- `fallbackModel` - Array of fallback models

## 3. Permission System

**Modes (6 total):**
- `default` (Manual) - Prompts for each tool
- `acceptEdits` - Auto-approves file edits + mkdir/touch/rm/mv/cp/sed
- `plan` - Read-only exploration
- `auto` - Classifier approves, blocks risky actions (research preview)
- `dontAsk` - Only pre-approved tools run
- `bypassPermissions` - Everything runs (isolated environments only)

**Rule syntax:**
- `Tool` or `Tool(specifier)`
- Bash: `Bash(npm run *)`, `Bash(git push *)`
- Read/Edit: `Read(./path)`, `Edit(/path)`, `Read(~/.ssh/**)`
- WebFetch: `WebFetch(domain:example.com)`
- MCP: `mcp__server__tool`, `mcp__github__*`
- Agent: `Agent(Explore)`, `Agent(my-custom-agent)`
- Evaluate order: deny → ask → allow (first match wins)

**Protected paths** (never auto-approved):
- `.git`, `.config/git`, `.vscode`, `.idea`, `.husky`, `.cargo`, `.devcontainer`, `.yarn`, `.mvn`, `.claude`
- `.gitconfig`, `.bashrc`, `.zshrc`, `.npmrc`, `.mcp.json`, `.claude.json`

## 4. Hooks System

**Events (25 lifecycle points):**
`SessionStart`, `Setup`, `UserPromptSubmit`, `UserPromptExpansion`, `PreToolUse`, `PermissionRequest`, `PermissionDenied`, `PostToolUse`, `PostToolUseFailure`, `PostToolBatch`, `Notification`, `MessageDisplay`, `SubagentStart`, `SubagentStop`, `TaskCreated`, `TaskCompleted`, `Stop`, `StopFailure`, `TeammateIdle`, `InstructionsLoaded`, `ConfigChange`, `CwdChanged`, `FileChanged`, `WorktreeCreate`, `WorktreeRemove`, `PreCompact`, `PostCompact`, `Elicitation`, `ElicitationResult`, `SessionEnd`

**Hook types:**
- `command` - Shell command (stdin JSON, exit 0=allow, exit 2=block)
- `http` - POST to endpoint
- `prompt` - LLM evaluation (Haiku default)
- `agent` - Multi-turn verification with tools
- `mcp_tool` - Call MCP server tool

**Output:**
- Exit 2 + stderr = block action
- Exit 0 + stdout JSON = structured control
- `hookSpecificOutput` for event-specific decisions
- `additionalContext` injects text into Claude's context

**Matchers:**
- Tool events: tool name regex (`Edit|Write`, `Bash`, `mcp__.*`)
- SessionStart: `startup`, `resume`, `clear`, `compact`
- Notification: `permission_prompt`, `idle_prompt`, `auth_success`
- SessionEnd: `clear`, `resume`, `logout`, etc.

## 5. Skills System

**Definition:**
- Directory with `SKILL.md` + optional supporting files
- Frontmatter: `name`, `description`, `disable-model-invocation`, `allowed-tools`, `model`, `effort`
- invoked as `/skill-name` or auto-invoked by Claude
- Arguments via `$ARGUMENTS`

**Key concepts:**
- Progressive disclosure: description loads at startup, full content loads on invocation
- `disable-model-invocation: true` keeps skill out of index until user invokes
- Skills load on-demand; don't bloat base context
- Can include scripts/, reference.md, etc.

**vs Commands:**
- Skills: directories with SKILL.md, namespaced in plugins
- Commands: flat .md files, simpler

## 6. Subagents

**Definition file** (`.claude/agents/name.md`):
```yaml
---
name: agent-name
description: When Claude should use this
model: sonnet/opus/haiku
effort: medium
maxTurns: 20
tools: Read,Grep,Glob,Bash
disallowedTools: Write,Edit
skills: skill1,skill2
memory: true  # Loads own MEMORY.md
background: true/false
isolation: worktree  # Only valid value
---
System prompt content here
```

**Key behaviors:**
- Own context window; only summary returns to parent
- Inherits parent's tools unless restricted
- Built-in: Explore (no CLAUDE.md, minimal prompt), Plan
- Foreground: waits for result before continuing
- Background: runs async, prompts surface in main session (v2.1.186+)
- Hooks fire; permission rules apply; subagent's `permissionMode` ignored

**Forking:**
- `/fork` creates background subagent inheriting full conversation
- Always runs in background
- Claude Code v2.1.161+

## 7. Workflows (Dynamic)

**Definition:**
- JSON or TypeScript script in `.claude/workflows/`
- Orchestrates many subagents in background
- Returns consolidated result
- Use for: 5-30+ parallel tasks, verification passes, large migrations

**vs Subagents:**
- Workflows: scripted orchestration, many agents, background only
- Subagents: Claude-driven delegation, few agents, foreground/background

**Bundled workflows:**
- `/batch` - Decompose large changes into parallel PRs
- `/deep-research` - Web research with citation
- `/ultrareview` - Multi-agent cloud review

## 8. Output Styles

**Definition** (`.claude/output-styles/name.md`):
```yaml
---
name: style-name
description: When to use this style
---
Custom system prompt content
```

- Replaces/augments system prompt for the session
- Switched via `/output-style` or `/config`
- Persists across sessions when selected
- Used for persona shifts (e.g., "Proactive", "Terse")

## 9. Plugins

**Structure:**
```
plugin/
├── .claude-plugin/
│   └── plugin.json      # Required: name, version, description
├── skills/              # SKILL.md directories
├── commands/            # Flat .md files (legacy)
├── agents/              # Subagent definitions
├── hooks/
│   └── hooks.json       # Hook configurations
├── .mcp.json            # MCP servers
├── .lsp.json            # LSP servers
├── monitors/
│   └── monitors.json    # Background monitors
├── output-styles/       # Output style definitions
├── themes/              # Color themes (experimental)
├── bin/                 # Executables added to PATH
├── settings.json        # Plugin default settings (agent, subagentStatusLine)
├── scripts/             # Hook/utility scripts
└── LICENSE, CHANGELOG.md
```

**Manifest** (`.claude-plugin/plugin.json`):
- Required: `name` (kebab-case)
- Optional: `version`, `description`, `author`, `homepage`, `repository`, `license`, `keywords`
- Component paths: `skills`, `commands`, `agents`, `hooks`, `mcpServers`, `outputStyles`, `experimental.monitors`, `experimental.themes`
- `userConfig` - Prompt user for values at enable time
- `channels` - Message injection (Telegram, Slack)
- `dependencies` - Other plugins required

**Scopes:** user (all projects), project (shared via git), local (gitignored), managed

**Environments:**
- `${CLAUDE_PLUGIN_ROOT}` - Plugin install dir (ephemeral)
- `${CLAUDE_PLUGIN_DATA}` - Persistent data (~/.claude/plugins/data/{id}/)
- `${CLAUDE_PROJECT_DIR}` - Project root

**Distribution:**
- Marketplaces: `claude-plugins-official`, `claude-community`
- `/plugin install`, `/plugin enable/disable`, `/plugin update`
- Auto-update: version field or git commit SHA

## 10. MCP (Model Context Protocol)

**Configuration:**
- Project: `.mcp.json` (committed to git)
- User: `~/.claude.json` under `mcpServers`
- Local: `~/.claude.json` under project entry
- Managed: System paths (macOS/Linux/Windows)

**Server types:**
- HTTP: `{"type": "http", "url": "https://..."}`
- SSE: `{"type": "sse", "url": "https://..."}`
- Stdio: `{"type": "stdio", "command": "npx", "args": [...], "env": {...}}`

**Key features:**
- Tool search: deferred loading, only names in context until used
- OAuth authentication support
- Resources via `@server:path` mentions
- Prompts as `/mcp__server__prompt` commands
- `CLAUDE_CODE_MCP_TIMEOUT` - Startup timeout (default 30s)
- `ENABLE_TOOL_SEARCH` - auto/false/true control schema loading

## 11. Context Window Management

**Startup load (~4200 tokens):**
- System prompt
- Auto memory (MEMORY.md, 200 lines/25KB)
- Environment info (cwd, platform, git status)
- MCP tool names (deferred schemas)
- Skill descriptions (one-liners, not bodies)
- CLAUDE.md hierarchy
- Output styles

**As Claude works:**
- File reads: 1K-5K tokens each
- Path-scoped rules: auto-load with matching files
- Hook output: additionalContext injects text
- Subagents: separate windows, only summary returns

**Compaction (`/compact`):**
- Replaces history with structured summary
- Preserves: system prompt, CLAUDE.md, auto memory, hooks, MCP
- Loses: path-scoped rules, nested CLAUDE.md, invoked skill bodies (capped at 5K/skill, 25K total)
- Skill descriptions don't reload after compaction

**1M context window:**
- Fable 5, Sonnet 5, Opus 4.6+, Sonnet 4.6
- `opus[1m]`, `sonnet[1m]` aliases
- Sonnet 5 always 1M, no suffix needed

## 12. Sessions & Checkpointing

**Session management:**
- Stored at `~/.claude/projects/{project-hash}/transcripts/{session-id}.jsonl`
- Resume: `--resume`, `--continue`, `/resume`
- Name sessions: `-n name`, `/rename`
- Branch: `/branch`, `--fork-session`
- `/clear` starts new conversation (old one resumable)

**Checkpointing:**
- Auto-tracked: every prompt + file edits
- `/rewind` or Esc+Esc to restore
- Restore: code, conversation, or both
- Summarize: compress part of conversation
- Persists across sessions
- Bash changes NOT tracked (git for that)

## 13. Agent Orchestration Comparison

| Approach | Coordination | Communication | Context | Use When |
|----------|-------------|---------------|---------|----------|
| **Subagents** | Parent delegates | Results to parent only | Separate windows | Side tasks, research |
| **Agent View** | You manage | Independent sessions | Separate windows | Multiple independent tasks |
| **Agent Teams** | Lead coordinates | Shared task list + messaging | Separate windows | Complex parallel work |
| **Workflows** | Script orchestrates | No inter-agent comms | Separate windows | 5-30+ agents, batch ops |

## 14. Key Environment Variables

**Authentication:**
- `ANTHROPIC_API_KEY` - Direct API access
- `ANTHROPIC_AUTH_TOKEN` - Bearer token for gateway
- `CLAUDE_CODE_OAUTH_TOKEN` - Long-lived OAuth (1 year)
- `ANTHROPIC_BASE_URL` - Custom API endpoint

**Model config:**
- `ANTHROPIC_MODEL` - Model override
- `ANTHROPIC_DEFAULT_OPUS_MODEL` - Pin Opus version
- `ANTHROPIC_DEFAULT_SONNET_MODEL` - Pin Sonnet version
- `ANTHROPIC_DEFAULT_HAIKU_MODEL` - Pin Haiku version
- `ANTHROPIC_DEFAULT_FABLE_MODEL` - Pin Fable version
- `CLAUDE_CODE_SUBAGENT_MODEL` - Subagent model override
- `CLAUDE_CODE_EFFORT_LEVEL` - Effort override

**Performance:**
- `DISABLE_PROMPT_CACHING` - Disable caching
- `BASH_DEFAULT_TIMEOUT_MS` - Bash timeout (default 2min)
- `BASH_MAX_TIMEOUT_MS` - Max bash timeout (default 10min)
- `BASH_MAX_OUTPUT_LENGTH` - Output cap (default 30K chars, max 150K)
- `CLAUDE_CODE_DISABLE_1M_CONTEXT` - Disable 1M context
- `MAX_THINKING_TOKENS` - Thinking budget

**Behavior:**
- `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` - Enable agent teams
- `CLAUDE_CODE_ENABLE_AUTO_MODE` - Enable auto mode on Bedrock/Vertex/Foundry
- `CLAUDE_CODE_SIMPLE` - Bare mode
- `CLAUDE_CODE_SAFE_MODE` - Disable all customizations
- `CLAUDE_ENV_FILE` - Env persistence script path
- `CLAUDE_CONFIG_DIR` - Override ~/.claude location

**Security:**
- `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` - Disable telemetry
- `CLAUDE_CODE_SUBPROCESS_ENV_SCRUB` - Strip credentials from subprocesses

## 15. Directory Structure Reference

**Project-level:**
```
project/
├── CLAUDE.md                 # Project context
├── CLAUDE.local.md           # Personal overrides
├── .claude/
│   ├── settings.json         # Shared project settings
│   ├── settings.local.json   # Personal project settings
│   ├── rules/                # Path-scoped rules
│   │   ├── api-conventions.md
│   │   └── testing.md
│   ├── agents/               # Custom subagents
│   │   └── reviewer.md
│   ├── skills/               # Project skills
│   │   └── deploy/
│   │       └── SKILL.md
│   ├── commands/             # Project commands
│   ├── hooks/                # Hook scripts
│   │   └── protect-files.sh
│   ├── output-styles/        # Custom output styles
│   ├── workflows/            # Dynamic workflows
│   ├── .mcp.json             # (Not loaded from here; use project root)
│   └── worktrees/            # Git worktrees for Claude
└── .mcp.json                 # MCP servers (project root)
```

**User-level:**
```
~/.claude/
├── CLAUDE.md                 # Global context
├── settings.json             # User preferences
├── MEMORY.md                 # Auto-generated memory
├── credentials.json          # Encrypted credentials
├── agents/                   # Global subagents
├── skills/                   # Personal plugins (@skills-dir)
│   └── my-plugin/
│       ├── .claude-plugin/
│       │   └── plugin.json
│       └── skills/
│           └── example/
│               └── SKILL.md
├── plugins/
│   ├── cache/                # Marketplace plugins
│   └── data/                 # Plugin persistent data
├── themes/                   # Custom color themes
└── projects/                 # Session transcripts
    └── {project-hash}/
        └── transcripts/
```

## 16. Extension Decision Matrix

| Need | Use |
|------|-----|
| Persistent project context | CLAUDE.md |
| Context that loads on file read | Path-scoped rules |
| One-off instructions | Prompt |
| Reusable workflow | Skill |
| Automation with zero exceptions | Hook |
| Isolated research task | Subagent |
| Parallel independent work | Agent view / Workflows |
| Complex multi-agent coordination | Agent teams |
| External tool integration | MCP |
| Shareable extension package | Plugin |
| Persona/system prompt change | Output style |
| Project-specific automation | Project-scoped hook/skill |
| Cross-project personal config | User-scoped settings |
| Organization-wide policy | Managed settings |

## 17. Critical Rules & Edge Cases

**Settings precedence:**
- Deny from any scope blocks allow from any scope
- Managed settings cannot be overridden
- Array settings merge by concatenation (not replacement), except managed sources

**Permission rules:**
- Deny rules block regardless of hook approval
- Ask rules force prompt even when hook returns "allow"
- Hook can tighten restrictions but cannot loosen past permission rules

**Hooks:**
- Run in parallel when multiple match
- Exit 2 blocks action (except non-blockable events)
- JSON output via stdout (exit 0) for structured control
- Deduplication: identical hook commands run once

**Skills:**
- Can't invoke `disable-model-invocation` skills themselves
- Plugin skills namespaced: `/plugin-name:skill-name`
- Skills-directory plugins: `@skills-dir` namespace, auto-loaded

**Subagents:**
- Don't inherit parent's conversation history
- Auto memory not included (use `memory: true` for separate MEMORY.md)
- Permission mode from parent, ignore subagent's `permissionMode`
- Plan-mode controls stripped by default

**Sandbox:**
- macOS: Seatbelt; Linux/WSL2: bubblewrap + socat
- Native Windows not supported
- Applies to Bash + child processes only
- Filesystem: write to working dir + temp by default
- Network: prompt per host first time (v2.1.191+ session-scoped)
- `allowUnsandboxedCommands: false` = strict mode

**Compaction:**
- Skill bodies reloaded, capped 5K/skill, 25K total
- Path-scoped rules lost until re-triggered
- Invoked skills preserved, not-listed skills gone
- Auto-compact at ~967K tokens (Sonnet 5 default)

**MCP:**
- Project `.mcp.json` requires workspace trust dialog
- Tool schemas deferred by default (load on use)
- OAuth tokens stored in system keychain

**Plugins:**
- Components at plugin root, NOT inside `.claude-plugin/`
- Marketplace plugins cached at `~/.claude/plugins/cache/`
- Symlinks preserved only within plugin dir
- Updates: version field or git commit SHA

## 18. Auto Mode Classifier Default Blocks

**Blocked by default:**
- `curl | bash`, data exfiltration
- Production deploys/migrations
- Mass deletion on cloud storage
- IAM/repo permission grants
- Force push, pushing to main
- `git reset --hard`, `git clean -fd`, `git stash drop`
- `terraform destroy`, `pulumi destroy`, `cdk destroy`
- DNS/TLS certificate changes
- Merging unapproved PRs
- Posting bot commands as comments
- Deleting production feature flags
- Kubernetes DaemonSets/admission webhooks
- Interactive shells into production
- Live credential printing
- Disabling CI checks

**Allowed by default:**
- Local file operations in working directory
- Installing dependencies from lock files
- Reading `.env` for matching API
- Read-only HTTP requests
- Pushing to current branch

## 19. Quick Reference: File Locations

| Config | Project | User | Managed |
|--------|---------|------|---------|
| Skills | `.claude/skills/` | `~/.claude/skills/` | Plugin/marketplace |
| Agents | `.claude/agents/` | `~/.claude/agents/` | Plugin/marketplace |
| Hooks | `.claude/settings.json` | `~/.claude/settings.json` | Managed settings |
| Rules | `.claude/rules/*.md` | N/A | N/A |
| MCP | `.mcp.json` (root) | `~/.claude.json` | System paths |
| CLAUDE.md | `./CLAUDE.md` | `~/.claude/CLAUDE.md` | Plugin-provided |
| Plugins | `.claude/settings.json` | `~/.claude/settings.json` | Managed settings |

## 20. CLI Essentials

**Start:**
- `claude` - Interactive mode
- `claude "query"` - Start with prompt
- `claude -p "query"` - Non-interactive, exit
- `claude -c` - Continue last session
- `claude -r "name"` - Resume named session

**Key flags:**
- `--model sonnet/opus/fable/haiku` - Model selection
- `--permission-mode plan/auto/acceptEdits` - Permission mode
- `--add-dir ../path` - Extra working directory
- `--mcp-config file.json` - MCP servers
- `--plugin-dir ./plugin` - Load plugin
- `--settings file.json` - Custom settings
- `--bare` - Skip auto-discovery (faster startup)
- `--output-format json/stream-json` - Structured output
- `--debug` - Enable debug logging

**Management:**
- `/permissions` - Manage permission rules
- `/sandbox` - Toggle sandbox
- `/mcp` - Manage MCP servers
- `/agents` - Manage subagents
- `/hooks` - View hooks
- `/resume` - Session picker
- `/compact` - Summarize context
- `/model` - Switch model
- `/effort` - Set effort level