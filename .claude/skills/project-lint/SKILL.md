---
name: project-lint
description: Use when someone asks to lint the project, check project structure, clean up files, audit project files, or maintain project structure.
argument-hint: [directory]
---

## What This Skill Does

Audits and maintains the Oxy OS project by:
1. Checking folder structure and file organization
2. Validating configuration and code files
3. Identifying junk/unnecessary files for potential deletion
4. Auto-fixing minor issues
5. Pausing at ~50% context window and providing exact continuation instructions

## Priority Order

Files are processed in this order:
1. **Configuration files** - .mcp.json, requirements.txt, .env files
2. **Project documentation** - CLAUDE.md, me.md, memory.md
3. **Code files** - Python scripts in automations/, other code
4. **Knowledge base** - Markdown files in context/
5. **All other files** - Deep scan for junk

## Steps

1. **Initialize report** - Create `context/logs/lint-report.md` with timestamp
2. **Discover project structure** - List all files in project root
3. **Check context/logs/ directory** exists, create if needed
4. **Process files by priority:**
   - Read each file
   - Check for issues:
     - **Python files:** syntax, trailing whitespace, excessive line length
     - **Markdown files:** frontmatter format, proper headers, trailing whitespace
     - **JSON files:** valid syntax
     - **Text files:** encoding, trailing whitespace
5. **Auto-fix minor issues:**
   - Trailing whitespace removal
   - Missing newline at EOF
   - Obvious formatting issues
6. **Identify potential junk files:**
   - Temporary files (*.tmp, *~, .DS_Store)
   - Files not referenced in CLAUDE.md or other documentation
   - Large files with no apparent purpose
7. **Track context usage** - Check token count periodically
8. **At 50% context:** Generate continuation file with exact next steps
9. **Present findings** to user before making major changes

## Continuation File Format

When stopping at 50% context, save to `context/logs/lint-continuation.md`:
```markdown
# Lint Continuation
**Stopped at:** [timestamp]
**Files checked:** [list]
**Next batch:** [remaining files]
**To resume:** Run `/project-lint` and load this file
```

## Issue Classification

**Auto-fix (minor):**
- Trailing whitespace
- Missing final newline
- Excessive blank lines
- Obvious typos in comments

**Requires user approval (major):**
- File deletions
- Structural changes to CLAUDE.md
- Renaming of important files
- Removal of code blocks

## Notes

- Never delete CLAUDE.md, me.md, memory.md without explicit confirmation
- Output goes to `context/logs/lint-report.md`
- Continuation file saved to `context/logs/lint-continuation.md`
- Use `python -m py_compile` for Python syntax checking
- Use `json.tool` for JSON validation