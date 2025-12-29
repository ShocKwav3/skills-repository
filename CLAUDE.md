# CLAUDE.md

This file provides guidance to agentic tools (including Claude Code) (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a skills repository for agentic tools (including Claude Code), containing packaged skills and resources for creating new skills. Skills are modular packages that extend agents' capabilities (including Claude) with specialized knowledge, workflows, and tool integrations.

## Repository Structure

```
SkillsRepo/
├── .claude/
│   └── skills/              # Active skills used by agentic tools (including Claude Code)
│       ├── skill-creator/   # Skill creation guidance and utilities
│       ├── pio-wrapper/     # PlatformIO output filtering
│       └── coding-standard/ # Code design standards and patterns
├── skillPackages/           # Packaged .skill files ready for distribution
├── externalResources/       # External reference materials and skill sources
└── .venv/                   # Python virtual environment
```

## Common Development Tasks

### Creating a New Skill

1. **Initialize the skill structure:**
   ```bash
   python3 .claude/skills/skill-creator/scripts/init_skill.py <skill-name> --path .claude/skills
   ```
   - Skill names must be hyphen-case (e.g., `my-new-skill`)
   - This creates SKILL.md with proper frontmatter and example resource directories

2. **Edit the skill:**
   - Update SKILL.md frontmatter with name and comprehensive description
   - The `description` field is critical - it determines when the skill triggers
   - Implement scripts in `scripts/`, references in `references/`, and assets in `assets/`
   - Test any scripts by running them to ensure they work correctly
   - Delete example files that aren't needed

3. **Package for distribution:**
   ```bash
   python3 .claude/skills/skill-creator/scripts/package_skill.py .claude/skills/<skill-name> skillPackages
   ```
   - Automatically validates the skill before packaging
   - Creates a `.skill` file (zip format with .skill extension)
   - Output goes to `skillPackages/` directory

### Python Environment

The repository uses a Python virtual environment for skill scripts:

```bash
# Activate virtual environment (if not already active)
source .venv/bin/activate

# Install dependencies
uv pip install <package-name>
```

## Key Architecture Concepts

### Skill Structure

Every skill consists of:

1. **SKILL.md (required):**
   - YAML frontmatter with `name` and `description` (required)
   - `description` determines when the skill triggers - must be comprehensive
   - Markdown body with instructions (loaded only after skill triggers)

2. **Bundled Resources (optional):**
   - `scripts/` - Executable code for deterministic operations
   - `references/` - Documentation loaded into context as needed
   - `assets/` - Files used in output (templates, boilerplate, etc.)

### Progressive Disclosure Pattern

Skills use three-level loading to manage context efficiently:

1. **Metadata (name + description)** - Always in context (~100 words)
2. **SKILL.md body** - Loaded when skill triggers (<5k words, keep under 500 lines)
3. **Bundled resources** - Loaded as needed by agents (including Claude)

**Important:** Keep SKILL.md lean. Move detailed content into `references/` files and reference them from SKILL.md with clear guidance on when to read them.

### When to Split Content

- If SKILL.md approaches 500 lines, split content into reference files
- For skills with multiple variants/frameworks, organize by variant in `references/`
- For large reference files (>100 lines), include table of contents at the top
- Avoid deeply nested references - keep references one level deep from SKILL.md

## Skill Design Principles

1. **Concise is Key** - Context window is a public good. Only add information agents don't already have.

2. **Set Appropriate Degrees of Freedom:**
   - High freedom (text instructions): Multiple valid approaches
   - Medium freedom (pseudocode/scripts with parameters): Preferred patterns with variation
   - Low freedom (specific scripts): Fragile operations requiring consistency

3. **Avoid Duplication** - Information should live in either SKILL.md or references files, not both

4. **No Extraneous Files** - Don't create README.md, INSTALLATION_GUIDE.md, CHANGELOG.md, etc. Skills contain only what the AI agent needs to perform tasks.

## Installed Skills

### skill-creator
Creates and packages new skills. Provides comprehensive guidance on skill design patterns, progressive disclosure, and best practices.

### pio-wrapper
Filters PlatformIO output to reduce token usage. Returns success confirmation or only error lines instead of full logs.

### coding-standard
Expert guidance for SOLID principles, Clean Code patterns (KISS, YAGNI, DRY, TDA), design patterns, and pragmatic software design. Use proactively when writing any code.

## Important Notes

- The `.venv/` directory and `externalResources/` are gitignored
- Skills are packaged as zip files with `.skill` extension
- Scripts should be tested before packaging to ensure they work
- Validation runs automatically during packaging - fix any errors before distribution
