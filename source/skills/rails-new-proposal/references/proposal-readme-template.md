---
name: proposal-readme-template
metadata:
  version: "1.0"
---

# Proposal README Template

Copy this template to `proposals/<proposal-slug>/README.md` and fill in every section. The README is the pitch a future curator reads to promote or delete the proposal, so it must stand alone. Replace all `<angle-bracket>` placeholders; delete none of the sections - if a section has nothing meaningful, say so plainly.

```markdown
---
name: <proposal-slug>
description: >-
  <One or two sentences: the capability this proposal offers and who would
  want it.>
metadata:
  version: "0.1"
  status: proposed
  origin_project: <project name>
  origin_path: <repo path or URL the slice was taken from>
  proposed_on: <YYYY-MM-DD>
  suggested_destination: <where this should land if promoted, e.g.
    source/skills/, source/rules/, source/agents/, context starter, memory>
---

# Proposal: <Human-Readable Title>

## What This Is

<Two to four sentences: the feature, how it works mechanically (hooks, agents,
scripts, rules), and what it does for the project that runs it.>

## Use Case

<The situation that motivated it in the origin project, described concretely
enough that a reader can recognize the same situation in their own project.>

## Evidence It Works

<Concrete, honest proof from the origin project: sessions where it caught a
problem, measurable behavior changes, adoption by other machines or
developers, design docs, commits. If evidence is thin, say so - a weak
proposal is still worth recording, but not worth overselling.>

## Why Generalize It

<Why this belongs in shared Agentic Rails tooling rather than staying
project-local. Which kinds of projects would benefit.>

## Contents Manifest

| Path | Role |
| --- | --- |
| `<path in this proposal>` | <what it does and why it is in the slice> |

## Dependencies and Requirements

<Runtimes, interpreters, packages, harness features (e.g. Claude Code hooks),
OS assumptions, and anything else the slice needs. Name versions where they
matter. "None beyond a standard <X> install" is a valid answer.>

## Integration Sketch

<A short, non-binding sketch of how promotion might look: what gets
generalized into which rail/layer, what a target project would add to its own
configuration, and what should NOT be carried over. This guides the curator;
it does not commit them.>

## Generalization Notes

<Honest list of what is project-specific in the slice: hardcoded names,
project-shaped assumptions, anything minimally altered during slicing (and
why). The curator's to-do list for promotion.>
```
