---
name: tooling-stages
metadata:
  version: "1.0"
---

# Tooling Stages

## Purpose

This reference defines how Quality Gate handles validation commands. Each repository may have different tooling; the persona should discover and run the commands that are configured locally, then report gaps honestly.

## Discovery Order

Look for validation commands in:

- The task plan or user request.
- Repository documentation such as `README.md`, `AGENTS.md`, `CONTRIBUTING.md`, or project-specific docs.
- Build files, package manifests, solution files, project files, and CI configuration.
- Existing scripts or task runners.

## Common Stages

- Build or compile checks.
- Unit, integration, snapshot, or UI tests.
- Type checking.
- Linting.
- Formatting checks.
- Static analysis.
- Security or dependency checks.
- Database migration checks.
- Domain-specific validation such as Unreal Build Tool analysis, Clang-Tidy, Visual Studio code analysis, asset validation, or generated-code checks.

## Reporting

Each tool entry in the final report records:

- Tool name.
- Status: `ran`, `not installed`, `errored`, or `skipped`.
- Command or project-specific entry point when useful.
- Short output summary.
- Whether the output produced findings, confidence, or a validation gap.

Do not skip expected tools silently. If a tool is unavailable, report it as `not installed` or `skipped` with the reason.
