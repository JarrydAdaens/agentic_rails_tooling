---
name: rails-project-appraisal-context-and-evidence
metadata:
  version: "1.0"
---

# Context Loading, Validation, and Evidence Rules

Supporting detail for `rails-project-appraisal`. Load this file when actually gathering evidence — the main `SKILL.md` workflow links here at each relevant step.

## Context Loading Order

Start at the repository root and read `README.md` first — it is the project's entry point. Then load the smallest useful set of Agentic Rails context, in this order, using progressive disclosure (indexes and headings first, full files only when needed):

1. `AGENTS.md`, if present.
2. `AGENTIC_RAILS_README.MD`, if present.
3. `context/laws.md`, always if present.
4. `context/agenticworkflow.md`, always if present.
5. `context/design.md`, always if present, including its Milestones Index.
6. `context/milestones/*.md`, enough to understand major delivery structure and what is currently active.
7. `context/backlog/*.md`, enough to understand planned, deferred, and unscheduled work.
8. `context/implementation-plans/*/plan.md`, for plans that are active, recent, or strategically important.
9. `context/dictations-tier-0/*.md`, only when raw rationale, scope drift, or unsynthesized intent materially matters — not by default.
10. `context/wiki/`, only when needed to interpret project-specific operations.

If maintained context (`context/design.md`, milestone/backlog docs) contradicts Tier-0 dictation, prefer maintained context but document the contradiction if it affects the appraisal.

<!-- rails-lint-allow: VC004 -->
If you encounter `context/milestones.md`, `context/goals*.md`, or `context/tier0/` (singular file / old-era paths) instead of the folder-based layout above, treat them as legacy migration signals worth noting, not the canonical structure.

After the first skim, if the project depends on sibling repositories, private resources, or external assets that are not available, ask the human for access or record the missing evidence and continue — never block the whole report on one unavailable resource. Mark affected conclusions with lower confidence instead.

## Codebase Overview Scope

Goal is architectural and execution understanding, not total ingestion. Prioritize:

- Top-level repository structure, build files, and package manifests.
- Runtime entry points and main source folders.
- Test folders and CI/CD configuration.
- Scripts used to build, test, run, lint, or deploy.
- Areas referenced by design, milestone, backlog, or implementation-plan docs.
- High-churn files identified from git (see Git Inspection below).

Skip generated folders, dependency folders, build outputs, caches, vendored libraries, binaries, and large assets unless directly relevant — e.g. `.git/`, `node_modules/`, `bin/`, `obj/`, `dist/`, `build/`, `out/`, `coverage/`, `.vs/`, `.idea/`, `.cache/`, `vendor/`.

## Validation Rules

Attempt to validate the project rather than relying only on static inspection: does it build/compile, do tests pass, do lint/type/static checks pass, can it launch, does the UI visibly work (if it has one)?

Prefer commands documented in `README.md`, `AGENTS.md`, package scripts, build files, or CI config, over guessing at conventions. Typical examples, chosen only when appropriate to the stack: `npm test` / `npm run build` / `npm run lint` / `npm run typecheck`, `pnpm test` / `pnpm build`, `dotnet build` / `dotnet test`, `cargo build` / `cargo test`, `pytest`, `make build` / `make test`.

Never invent risky commands, deploy, publish, push, migrate production data, wipe databases, or rotate secrets. If a command needs credentials, paid services, or unavailable infrastructure, don't force it — record the limitation and its effect on confidence.

If dependency installation is required, use the project's documented method and record what was installed or restored. Do not upgrade dependencies or edit lockfiles for the appraisal — if a validation step changes one anyway (e.g. a restore regenerating a lockfile), note it in the report rather than silently reverting it.

## Screenshot and UI Evaluation

If the project has a UI and it's reasonable to launch locally, capture screenshots and evaluate them for: broken rendering, empty states that shouldn't be empty, layout problems, clipped/overlapping text, visual hierarchy issues, navigation dead ends, error screens, unstyled scaffolding, and UX inconsistencies against the project's stated purpose.

Store screenshots only when useful, under:

```text
context/reports/assets/YYYY-MM-DD_project-appraisal/
```

Reference screenshot paths from the report. If screenshots cannot be captured, say why.

## Git Inspection

Useful commands:

```text
git status --short
git branch --show-current
git log --oneline --decorate -n 30
git log --date=short --pretty=format:"%h %ad %an %s" -n 50
git shortlog -sn --all
git diff --stat
git diff --name-only
git ls-files
```

For churn:

```text
git log --name-only --pretty=format: | sort | uniq -c | sort -nr | head -30
```

Look for: active development vs. abandonment, scaffold-only projects, rewrite loops, churn without durable progress, large unfinished branches (if visible), long-running solo passion-project patterns, recent hardening/test growth/cleanup, and misalignment between the stated roadmap and actual commits.

Summarize contributor patterns rather than exposing private author emails unless the appraisal genuinely needs them.

## Web and External Grounding

Use web research when it materially improves the appraisal — commercial viability, competitor landscape, market demand, library/framework health, current best practice, or claims about trends and ecosystems.

Ground claims with sources: record searches and source URLs/citations in the report's provenance section, with publication or accessed dates where available. If the research is shallow, say so — don't assert market certainty from thin evidence.
