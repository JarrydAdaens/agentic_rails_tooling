# Agentic Rails

Agentic Rails is an opinionated, IDE-agnostic framework for AI-assisted software development.

The core idea is simple:

> Agents can move fast, but they need rails.

Without rails, agentic coding can become generated code, scattered plans, half-remembered decisions, and fragile handovers. Agentic Rails gives AI agents a structured way to work inside a project so the human can keep control, understand what happened, and continue safely.

```text
Left rail  = context and provenance
Right rail = tools, skills, agents, and workflows
Carriage   = the project being built
Driver     = the human
```

The point is not to make agents autonomous. The point is to make agentic coding legible, inspectable, repeatable, and safe enough for real engineering work.

## Repository Model

Agentic Rails is the framework name for projects that use the context starter and reusable tooling together. It is not a separate repository.

| Layer | Role | Responsibility |
| --- | --- | --- |
| Agentic Rails | Framework name | Names the combined development system, terminology, and adoption model |
| `agentic_rails_context_starter` | Left rail | Template repository for project-local context, plans, implementation logs, and handovers |
| `agentic_rails_tooling` | Right rail | Reusable skills, agents, rules, workflows, and references |
| Target project repositories | Carriage | Actual software projects created from the starter and supported by tooling |

This repository was created from, or is itself, the `agentic_rails_context_starter` template. It should carry the context structure and persistent framework overview, but it should not become the home for generic reusable skills, agents, or workflows. Those belong in `agentic_rails_tooling`.

## The Left Rail: Context And Provenance

The left rail answers:

> Where does project knowledge live?

It is provided by `agentic_rails_context_starter` and gives each project a durable documentation structure:

- five-tier context hierarchy
- documentation conventions
- implementation-plan folders
- required plan and implementation-log templates
- optional skill-generated provenance artifacts
- handover locations when a handover skill or workflow is used
- persistent framework identity files

The starter is a template. A derived project should replace placeholders with project-specific purpose, architecture, milestones, goals, and execution history.

## The Right Rail: Tooling And Behaviour

The right rail answers:

> How should agents behave while working?

It is provided by `agentic_rails_tooling` and may include reusable:

- skills
- specialist agents
- rules
- workflow skills
- handover behaviours
- planning behaviours
- complaint logging behaviours
- evidence and provenance behaviours

Project-local context remains authoritative. Shared tooling supplements the project, but it does not override the project laws, design, milestones, goals, or implementation plans.

## Five-Tier Context System

Agentic Rails uses a five-tier context model:

| Tier | Layer | Location | Purpose |
| --- | --- | --- | --- |
| Tier 0 | Raw intake and addenda | `Documentation/tier0/` | Dictated notes, rough source material, and recurring supplemental vision |
| Tier 1 | Project purpose and design | `Documentation/design.md` | Maintained architecture, principles, constraints, and system shape |
| Tier 2 | Milestones | `Documentation/milestones.md` | Roadmap stages and milestone intent |
| Tier 3 | Goals | `Documentation/goals*.md` | Specific deliverables, acceptance criteria, scope, and status |
| Tier 4 | Implementation plans and execution records | `Documentation/implementation_plans/` | Task-ready plans and implementation logs, with optional skill-generated provenance artifacts |

Lower tiers give agents strategic context. Higher tiers capture what happened during execution. This prevents agents from operating only on immediate prompts and scattered source files.

## Provenance

Agentic Rails treats provenance as a first-class engineering artifact.

It does not only ask:

> What code changed?

It also asks:

> What was intended, what happened, what evidence proves it, what friction appeared, and how does ownership transfer back to the human?

Meaningful implementation work should live in a dedicated folder under `Documentation/implementation_plans/`:

```text
Documentation/
  implementation_plans/
    GOAL_3_1_short-readable-name/
      plan.md
      implementation-log.md
```

### `plan.md`

The intended work:

- goal
- approach
- scope and non-goals
- steps
- acceptance criteria
- risks and open questions

### `implementation-log.md`

What actually happened:

- execution steps
- deviations from the plan
- failed attempts
- implementation decisions
- validation performed
- remaining uncertainty

The following artifacts are optional. They are created only when the corresponding reusable skill or workflow is invoked for the task.

### `complaining.md`

Operational friction:

- missing permissions
- ambiguous requirements
- broken tooling
- risky assumptions
- repeated workarounds
- missing domain knowledge
- unclear validation paths

This is not emotional theatre. It captures actionable friction that would otherwise disappear.

Created by the `complaining` skill.

### `thinking.md`

Sanitised agent notes:

- useful investigation paths
- discovered constraints
- observations for future agents
- things to revisit

This is not a private chain-of-thought dump.

Created by the `thinking-out-loud` skill.

### `evidence.md`

The provenance index:

- files changed
- commits
- tests run
- build results
- validation evidence
- planning inputs
- known unverified claims

Created by the `evidence` skill.

### `handover/`

Ownership transfer artifacts that help the human understand what was done and how to continue.

Created by the `handover` skill or a larger handover workflow.

## Accountability Handover

Agentic Rails treats handover as part of the work, not an afterthought.

### Shallow Handover

Use shallow handover for smaller tasks. It should answer:

> What did you build, did it work, and where can I verify it?

It usually includes:

- elevator pitch
- scope covered
- technical choices
- outcome assessment
- source-grounded evidence
- important decisions
- risks
- suggested next step

### Deep Handover

Use deep handover for larger or production-grade work. It should answer:

> If the AI never comes back, how does the human fully understand, maintain, criticise, and continue this work?

Deep handover can produce:

```text
handover/deep/
  00-index.md
  01-deep-technical-report.md
  02-walkthrough-tour-script.md
  03-post-mortem-retrospective.md
  04-180-performance-review.md
  05-software-bill-of-materials.md
  06-future-maintenance-map.md
```

Deep handover should be grounded in the plan, implementation log, complaints, thinking notes, evidence, source files, git history, tests, and planning documents.

## Warm And Cold Handover

Warm handover happens immediately after the work, while the agent still has conversation context. It can produce stronger retrospectives, decision history, and collaboration assessments.

Cold handover happens later, when the agent was not present. It must rely only on source code, git history, documentation, implementation logs, complaint logs, and evidence files. Cold retrospectives should label claims as verified, inferred, assumed, or unknown.

## Progressive Disclosure

Agentic Rails should not dump every rule into every prompt.

Agents should first detect whether a repository follows Agentic Rails conventions, then load only the relevant project context and skills for the task.

Common detection points include:

- `AGENTIC_RAILS.md`
- `.agentic-rails.json`
- `Documentation/implementation_plans/`
- `AGENTIC_RAILS_README.MD`

Detailed conventions should live in reference files and project documentation, not in every prompt.

## Design Boundaries

`agentic_rails_context_starter` should contain:

- templates
- folder conventions
- starter documentation
- bootstrap files
- persistent framework identity files
- default context structure

It should not contain:

- generic reusable skills
- generic reusable agents
- generic reusable workflows

`agentic_rails_tooling` should contain reusable agentic machinery.

Target project repositories may contain project-specific agents, skills, tools, generated plans, logs, evidence, and handovers when they belong directly to that project.

## Operating Loop

Agentic Rails turns agentic coding from:

```text
Prompt -> Code -> Hope
```

into:

```text
Context -> Plan -> Execute -> Log -> Evidence -> Handover -> Ownership
```

The human remains responsible for direction, judgement, priorities, acceptance, taste, risk tolerance, and final ownership. Agents can execute, inspect, explain, complain, and hand over. They do not become the owner.
