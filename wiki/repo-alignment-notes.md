# Repository Alignment Notes

This repository separates reusable context into layers:

- `rules/`: concise standards and style-shaping constraints.
- `skills/`: reusable task capabilities and workflow modules.
- `agents/`: specialist worker definitions with operating contracts and references.
- `prompt_dev/`: source prompt material used to create or refine artifacts.

## Skill Rules For This Repository

- Every skill directory must contain `SKILL.md`.
- The folder name and `name` frontmatter must match.
- Skill names use lowercase letters, numbers, and hyphens.
- Put nonstandard data such as local version, owner, or template status under `metadata`.
- Descriptions should use "Use this skill when..." style when it helps activation.
- Keep workflow-style skills under `skills/` for now, but make their orchestration role explicit.

## Agent Rules For This Repository

Agents are not Agent Skills, but they should follow similar hygiene:

- Use concise trigger-oriented descriptions.
- Put local version and owner information under `metadata`.
- Keep reference maps explicit so agents load only relevant files.
- Keep provider-facing `agents/openai.yaml` metadata aligned with `AGENT.md`.

## Migration Notes

- The discovery-test skill was renamed to `check-dot-agent` for strict Agent Skills compatibility.
- `skill-template` now has valid YAML frontmatter and is a concrete starter template.
- `skill-template-advanced` now has a spec-compliant name matching its folder.
