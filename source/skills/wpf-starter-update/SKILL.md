---
name: wpf-starter-update
description: >-
  Use this skill when updating a WPF project that was spawned from WPF-Starter
  by selectively reconciling source-code improvements from the current local
  WPF-Starter source-of-truth into the derived project. Use when an older
  derived WPF app needs current starter architecture such as AvalonDock docking,
  advanced theming, AppData JSON configuration, shared projects, reusable
  controls, services, or startup patterns, while preserving project-specific
  behavior. Do not use for Agentic Rails context updates, documentation-tier
  template synchronization, pushing derived app features upstream, generic WPF
  advice, or ordinary feature work unrelated to starter alignment.
disable-model-invocation: true
metadata:
  version: "1.1"
---

# WPF-Starter Update

Update a derived WPF project from the current local `WPF-Starter` source-of-truth.

Treat the starter as an evolving reference implementation, not as an authority that can overwrite the derived app. Compare, classify, discuss risky integrations, and apply only the source-code improvements that make sense.

## Required Input

Require the local filesystem path to the current `WPF-Starter` repository.

If the user did not provide the path, ask exactly:

```text
Where is your local WPF-Starter repository? Please provide the exact directory path on disk.
```

Stop until the user provides the path. Do not guess the starter path.

## Hard Scope Boundary

Update source code and source-adjacent project files only.

Do not update or reconcile Agentic Rails context files, including:

- `context/design.md`
- `context/milestones/`
- `context/backlog/`
- `context/dictations-tier-0/`
- `context/implementation-plans/`
- Agentic Rails context starter templates
- project planning documents, story status, sprint status, or milestone status

You may read lightweight repository documents such as `README.md` only for source-code orientation and starter feature history. Do not treat documentation-tier files as synchronization targets.

## Operating Model

1. Confirm the current working repository is the derived WPF project to update.
2. Obtain the local path to the current `WPF-Starter` source-of-truth.
3. Inspect both repositories at a high level before changing files.
4. Inventory source-code systems present in the starter.
5. Identify which systems are missing, older, divergent, project-specific, or already equivalent in the derived project.
6. Produce a short reconciliation plan grouped by feature area before major edits.
7. Ask the programmer before risky or compatibility-sensitive integrations.
8. Apply accepted changes surgically.
9. Preserve project-specific code unless the programmer explicitly approves replacement.
10. Build and run appropriate validation.
11. Record what was adopted, skipped, deferred, rejected, or intentionally left divergent without writing to Agentic Rails context-tier files.

## Progressive Disclosure

Load broad structure first:

1. solution and project shape
2. `README.md` feature notes
3. high-level source folders
4. feature entry points
5. deeper implementation files only for selected feature areas

For each major area, produce a short finding before digging deeper, such as:

- Docking: missing entirely / present but old / present and divergent / already current.
- Theming: missing starter theme folders; local app has custom theme resources.
- Configuration: local app has ad-hoc JSON config under a different AppData path.
- Shared projects: starter has reusable projects absent from the derived solution.

## Detection Checklist

Inspect the derived project and starter for:

- WPF `.csproj` files and `.sln` structure
- `App.xaml`, `MainWindow.xaml`, and startup/bootstrap code
- shared library projects and project references
- theme folders and resource dictionaries
- AvalonDock references, docking layouts, layout persistence, and docking services
- configuration services, AppData path handling, JSON persistence, and settings models
- dependency injection setup, if present
- reusable controls, services, helpers, and app framework utilities

Derived projects may have renamed projects, namespaces, folders, and assemblies. Do not assume names match the starter.

## Feature Areas

### AvalonDock And Docking

Check package/reference alignment, docking layout XAML, host/window integration, document/tool pane concepts, layout persistence, compatible view/view-model structure, and starter docking services or helpers.

Treat docking as a major architectural integration. Ask before replacing `MainWindow.xaml`, changing the root shell, removing navigation, migrating existing panels into documents/tools, or changing persisted layout formats.

### Advanced Theming

Check starter theme folders, resource-dictionary structure, theme keys, merged dictionaries, theme switching, application resource loading, control style coverage, and compatibility with older custom styles.

Known starter themes may include `Dark`, `Light`, and `Fritcher Aero`, but inspect the starter for the current set.

Prefer complete theme resource structures while preserving derived-app custom resources. Ask before replacing large theme dictionaries, renaming keys used by app views, deleting custom themes, or changing the default theme.

### Configuration System

Check AppData folder usage, JSON load/save, default configuration creation, extensible configuration models, versioning or migration support, existing settings models, persisted file names, file locations, and user data compatibility requirements.

Do not blindly replace local configuration code. Ask how to reconcile configuration when existing users may have files, paths differ, schemas differ, old settings must migrate, app-specific fields exist, or the derived project has a similar but incompatible system. Prefer migration over breakage.

### Shared Projects

Compare all starter projects against the derived solution. Determine whether each starter project already exists, has an older or renamed equivalent, is folded into another project, is unnecessary, or requires unsafe restructuring.

When adding shared projects, update the solution and project references, preserve derived naming conventions where possible, and avoid moving application-specific code into shared projects without approval.

## Reconciliation Categories

Classify every starter improvement as one of:

- `Already Current`: local code appears equivalent; no change.
- `Missing`: starter feature does not exist locally; candidate for adoption.
- `Older Version`: local feature predates starter improvements; candidate for update.
- `Divergent Equivalent`: local code solves the same problem differently; discuss first.
- `Project-Specific`: local behavior intentionally differs; preserve unless approved.
- `Unsafe To Merge Blindly`: could break data, layout, startup, config, or public behavior; ask first.
- `Rejected`: programmer does not want this starter feature; record explicitly.
- `Deferred`: useful but not now; record explicitly.

## Human-In-The-Loop Rules

Make straightforward low-risk updates directly when they are isolated starter infrastructure with no local equivalent and do not threaten project-specific behavior.

Ask the programmer before changes that affect:

- configuration file compatibility, AppData locations, persisted user data, or schemas
- root window layout, docking shell migration, navigation, or persisted layouts
- dependency injection architecture or startup/bootstrap order
- project/assembly restructuring or namespace-wide rewrites
- deletion of local styles, controls, services, or custom themes
- replacement of local services with starter services
- any system where the derived app already has a custom implementation

Ask concrete questions that name the local and starter differences and offer practical options, such as migration, wrapper/adaptor, keeping the old path, or deferring.

## Update Strategy

Prefer these strategies in order:

1. Direct copy for isolated starter files with no local equivalent.
2. Three-way-style comparison when local and starter files share ancestry but both changed.
3. Adapter or wrapper when app-specific code must work with starter interfaces.
4. Incremental migration when replacing a whole system is too risky.
5. Documented deferral when adoption is useful but unsafe in this pass.
6. Documented rejection when the programmer explicitly does not want the feature.

Avoid broad find/replace unless the impact is fully understood.

## Safety Rules

- Do not overwrite project-specific source files without comparing them first.
- Do not delete local code just because the starter no longer has it.
- Do not assume starter namespaces or folder structure match the derived project.
- Do not break existing user configuration compatibility.
- Do not change app identity, product name, package id, signing config, or deployment metadata unless explicitly asked.
- Do not update Agentic Rails context files.
- Do not silently skip validation.
- Do not claim the update is complete if the project does not build.

## Recording Decisions

If the programmer rejects or defers a feature, record the decision explicitly.

Create a concise local update report in an appropriate source-adjacent notes location, but keep it outside Agentic Rails context-tier folders such as `context/implementation-plans/`. If the programmer explicitly asks to also update an Agentic Rails implementation log, treat that as a separate logging request governed by the relevant Agentic Rails skill.

Include the feature name, decision, reason, date, and any revisit condition.

## Validation

Run reasonable validation for the repository:

- restore
- build
- unit tests, if present
- WPF startup smoke check, if possible
- resource dictionary load checks, if XAML resources changed
- config load/save checks, if configuration changed

If validation cannot run, record why. The update is not complete until the derived project still restores and builds, or the build failure is explicitly recorded with cause.

## Final Report

Report:

- `WPF-Starter` path used
- derived project path
- feature areas compared
- adopted changes
- rejected or deferred changes
- files changed
- validation run
- build/test result
- remaining risks or manual follow-up

Keep the report factual and specific.
