---
name: rails-harvest-innovation
description: >-
  Use this skill when harvesting, extracting, neutralizing, and upstreaming a
  reusable feature, subsystem, control, service, configuration pattern, WPF
  architecture improvement, or implementation from a project derived from
  WPF-Starter back into the local WPF-Starter starter/template repository. Use
  for requests to pull a proven derived-project innovation upstream into
  WPF-Starter so future derived projects inherit it safely. Do not use for
  updating a derived app from WPF-Starter, syncing Agentic Rails context starter
  files, general refactoring inside one repository, or copying project-specific
  business logic into a starter.
---

# Rails Harvest Innovation

Harvest a proven WPF-derived project feature into `WPF-Starter` without importing the derived project's accidental identity.

This is the upstream counterpart to `$wpf-starter-update`: the destination is the starter, and the source is a derived project.

## Required Inputs

Require:

- Destination `WPF-Starter` path. Default to the current repository only when it is clearly WPF-Starter.
- Source derived project path.
- Feature or innovation to harvest.

Accept rough feature identifiers such as a class name, namespace, package, folder, implementation plan, behavior description, or "the JSON AppData settings system".

If the source path or feature identifier is missing, ask exactly:

```text
Where is the WPF-Starter-derived source project that contains the feature to harvest? Please provide the exact directory path on disk, and the feature or innovation you want upstreamed into WPF-Starter.
```

If the destination is not clearly WPF-Starter, ask exactly:

```text
Which local repository is the WPF-Starter destination that should receive this feature? Please provide the exact directory path on disk.
```

Stop until the user provides the required paths. Do not guess either path. If either repository role remains ambiguous after the response, ask again before editing.

## Hard Scope Boundary

Harvest the requested feature into WPF-Starter and nothing else. Writing into `context/implementation-plans/` for this harvest is allowed and expected; tidying unrelated areas while passing through is not.

Do not modify, reorganize, or "clean up" the following in WPF-Starter unless the harvested feature genuinely requires it and the user has accepted the change:

- existing or historical implementation-plan folders unrelated to this harvest
- `context/design.md`, `context/milestones.md`, `context/goals*.md`, `context/laws.md`
- `context/wpf-starter-inventory.md` sections unrelated to the harvested feature
- app identity, product name, assembly name, package id, signing config, or deployment metadata
- starter sample views, panes, or content not related to the feature
- root shell layout, `MainWindow`, DI/Generic Host bootstrap order, or persisted layout/config schemas
- existing public APIs, namespaces, or resource keys consumed by starter XAML

If the feature genuinely requires changing any of the above, stop and ask before editing. Touching unrelated areas during a harvest is out of scope even when the change looks like an obvious improvement.

## Progressive Disclosure

Load only what the current decision needs:

- For repository role checks, Agentic Rails context loading, and Tier 4 plan/log expectations, read [references/context-and-planning.md](references/context-and-planning.md).
- For source inspection, extraction boundaries, neutralization, reconciliation, integration, and validation, read [references/extraction-workflow.md](references/extraction-workflow.md).
- For WPF-specific feature checklists covering configuration, shared projects, XAML, services, dependencies, theming, docking, and startup, read [references/wpf-feature-guides.md](references/wpf-feature-guides.md).
- For implementation logging, final reporting, and failure handling, read [references/report-and-failures.md](references/report-and-failures.md).

For `WPF-Starter`, prefer `context/wpf-starter-inventory.md` as the canonical feature map when present. Read the relevant section before deeper code inspection.

## Operating Model

1. Confirm destination and source repositories.
2. Inspect lightweight context and the relevant starter inventory sections.
3. Create or select a destination Tier 4 implementation-plan folder for meaningful upstreaming work.
4. Write or update `plan.md` before implementation when the feature is non-trivial.
5. Map the source feature and its dependencies.
6. Define the extraction boundary: reusable core, required support, and project-specific baggage.
7. Neutralize names, paths, defaults, branding, and environment assumptions.
8. Reconcile with any existing WPF-Starter equivalent instead of adding a competing system.
9. Integrate surgically into WPF-Starter using its existing structure and conventions.
10. Validate in WPF-Starter, not only in the source project.
11. Update `implementation-log.md` with what actually happened.
12. Report the harvested feature, changed files, exclusions, validation, risks, and plan/log location.

## Core Rules

- Extract the innovation, not the project.
- Treat the source derived project as evidence, not authority.
- Preserve WPF-Starter as a reusable starter/template.
- Do not silently broaden the requested feature.
- Do not silently copy business logic, product names, branding, local paths, secrets, deployment identity, or user-specific settings.
- Do not add a major third-party package without asking.
- Do not claim validation passed unless it actually ran and succeeded.

## Ask Before Proceeding When

- The feature boundary is unclear.
- A file mixes reusable infrastructure with project-specific behavior.
- The destination already has a similar feature.
- A dependency, public API, namespace, AppData path, persisted schema, or starter default must be chosen.
- The change affects startup, DI, shared projects, root window layout, theming, docking, configuration compatibility, or generated runtime files.
- Validation cannot be performed.

## Validation

Run the strongest reasonable checks from the destination repository:

- restore and build
- tests, if present
- WPF startup or smoke checks, when feasible
- XAML/resource dictionary load checks after UI/resource changes
- settings/config load-save checks after configuration changes

Record any validation gap in `implementation-log.md` and the final report.
