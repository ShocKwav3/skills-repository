# Skills Repository

A collection of reusable skills for agentic tools (including Claude Code) that extend their capabilities with specialized knowledge and workflows.

## Purpose

This repository serves as a central location for developing, packaging, and distributing skills for agentic tools (including Claude Code). Skills are modular packages that provide agents (including Claude) with domain-specific knowledge, tools, and workflows.

## Available Skills

### skill-creator
**Purpose:** Create new skills in a systematic way

**Provider:** Anthropic

**Usage:** Used within this repository to develop new skills. Provides guidance, templates, and utilities for skill creation and packaging.

### pio-wrapper
**Purpose:** Filters PlatformIO output to reduce token usage

**Usage:** Copy to your actual projects. Use either:
- The skill folder from `.claude/skills/pio-wrapper/`
- The packaged file `skillPackages/pio-wrapper.skill`

Returns success confirmations on successful builds and only error lines on failures, dramatically reducing context consumption.

### coding-standard
**Purpose:** Expert guidance for SOLID principles, Clean Code patterns, and design patterns

**Usage:** Copy to your actual projects. Use either:
- The skill folder from `.claude/skills/coding-standard/`
- The packaged file `skillPackages/coding-standard.skill`

Provides proactive guidance when designing classes, implementing features, refactoring code, or writing functions.

## Getting Started

1. **To use a skill in your project:**
   - Copy the skill folder to your project's `.claude/skills/` directory, or
   - Import the `.skill` package file from `skillPackages/`

2. **To create a new skill:**
   - See `CLAUDE.md` for detailed instructions on using the skill-creator utilities

## License

- **skill-creator**: Apache License 2.0 (see `.claude/skills/skill-creator/LICENSE.txt`)
- **Other skills**: Check individual skill directories for license information
