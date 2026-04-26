# Agent Skills Wiki

This wiki captures the AgentSkills.io material used by this repository and turns it into local, reviewable guidance for maintaining compatible skills and agents.

## Pages

| Page | Purpose |
| --- | --- |
| [overview.md](overview.md) | What Agent Skills are, why they exist, and how progressive disclosure works. |
| [specification.md](specification.md) | The compatibility rules for skill directories, `SKILL.md` frontmatter, optional folders, and validation. |
| [best-practices.md](best-practices.md) | How to write useful, scoped, execution-tested skills. |
| [optimizing-descriptions.md](optimizing-descriptions.md) | How to make skill descriptions trigger reliably without becoming too broad. |
| [evaluating-skills.md](evaluating-skills.md) | How to test whether a skill improves output quality. |
| [using-scripts.md](using-scripts.md) | How to reference commands and bundle scripts in skills. |
| [repo-alignment-notes.md](repo-alignment-notes.md) | Local conventions for this repository's `skills/`, `agents/`, `rules/`, and workflow-style skills. |

## Local Maintenance Checklist

- Skill folder names and `name` frontmatter values must match.
- Skill names use lowercase letters, numbers, and hyphens only.
- `description` should explain what the skill does and when to use it.
- Nonstandard fields belong under `metadata`.
- Keep `SKILL.md` focused; move deeper material into `references/` or `assets/`.
- Add gotchas, examples, validation loops, and scripts only when they prevent likely mistakes.
