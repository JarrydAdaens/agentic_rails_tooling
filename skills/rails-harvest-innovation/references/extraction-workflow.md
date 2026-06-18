# Extraction Workflow

Use this reference while inspecting, bounding, neutralizing, integrating, and validating the harvested feature.

## Source Feature Mapping

Map the requested feature in the source repository:

- primary implementation files
- dependent files
- interfaces and abstractions
- configuration models
- registration/bootstrap code
- XAML, resource dictionaries, templates, converters, behaviors, and styles
- tests and smoke paths
- docs, plans, and usage sites
- package references and project references
- runtime data locations and AppData paths
- project-specific names, branding, defaults, assumptions, and business logic

Record concise findings in `implementation-log.md`, or in `thinking.md` only when the thinking-out-loud skill is active.

## Destination Convention Mapping

Inspect how WPF-Starter currently handles:

- solution and project structure
- namespaces and assembly names
- shared projects
- configuration and AppData paths
- dependency injection and Generic Host startup
- services and abstractions
- XAML resources and merge order
- tests and validation commands
- starter documentation and inventory

Use existing starter conventions unless the user explicitly asks for a new convention.

## Extraction Boundary

Classify source material into:

| Group | Meaning | Action |
| --- | --- | --- |
| Reusable core | generic capability WPF-Starter should gain | extract and adapt |
| Required support | minimal support needed for the feature to work | extract, adapt, or recreate |
| Project-specific baggage | business logic, product identity, paths, branding, one-off assumptions | exclude |

If a file contains mixed reusable and project-specific code, split or rewrite it. Do not copy the whole file just because part of it is useful.

## Neutralization Checklist

Before integrating into WPF-Starter:

- replace derived-project namespaces with starter namespaces
- remove source app names, branding, secrets, deployment identity, and product-specific copy
- replace source-specific paths, AppData folders, and environment assumptions with starter-safe defaults
- remove business-specific settings, commands, views, data models, and workflows
- keep public APIs generic and extensible
- align file locations, naming, and project references with WPF-Starter
- remove dead code and unused dependencies
- update comments and docs so they describe starter behavior, not the source project

Neutralization should preserve the reusable behavior while removing accidental source identity.

## Reconcile Existing Starter Capability

When WPF-Starter already has a similar feature:

- compare both implementations
- identify overlapping files, services, contracts, packages, and runtime state
- preserve existing starter public contracts when reasonable
- migrate toward the better generic implementation
- document intentional replacement or divergence

Do not add two competing systems unless the user explicitly accepts that.

## Integration Checklist

Apply the feature to WPF-Starter by updating only what the feature requires:

- source files
- project and solution files
- package references
- dependency injection registrations
- configuration defaults
- XAML resources and resource merges
- tests or test fixtures
- `context/wpf-starter-inventory.md`
- relevant design, goals, plan, or implementation-log files when behavior changes

Keep WPF-Starter usable as a standalone template after the change.

## Validation

Validate against the destination starter:

- restore dependencies
- build the solution or affected projects
- run tests, if present
- run static checks, if configured
- smoke WPF startup, when feasible
- verify XAML resource dictionaries after XAML/resource changes
- verify settings/config load-save behavior after configuration changes

If validation fails, record the command, failure summary, likely cause if known, affected files, and safest next step. Do not mark the work complete unless the user explicitly accepts the validation gap.
