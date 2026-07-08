---
name: rails-new-proposal
description: >-
  Use this skill when the user wants to capture a proven, project-local
  innovation - a guard rail, hook set, agent, rule pack, script, or workflow -
  as a self-contained proposal for the Agentic Rails tooling repository.
  Triggers: "make this a proposal", "propose this for rails", "bundle this up
  for tooling", "this guard rail should be generalized". It copies the working
  slice verbatim (hooks extracted into a fresh .claude/settings.json, agents,
  scripts, dependency manifests, docs) into proposals/<slug>/ in the tooling
  repo, writes a README recording the use case, the evidence it works, and a
  suggested destination, and can zip the proposal for sharing with another
  developer. It is drop-off only: it never integrates anything into source/,
  never generalizes code, and never touches other proposals.
disable-model-invocation: true
metadata:
  version: "1.0"
---

# Rails New Proposal

Capture a proven, project-local innovation as a **self-contained proposal** and drop it into the `proposals/` inbox at the root of the `agentic_rails_tooling` repository. A proposal is a pitch plus its proof: a README that records the use case and the evidence it worked, and a verbatim slice of every file needed to make the feature work somewhere else.

This skill has exactly one job: **package and drop off**. It does not integrate, generalize, or curate. The user reviews the inbox later and asks an agent to promote a proposal into the right part of the Agentic Rails system - or delete it. Because a proposal is self-contained, it can also be zipped and shared directly with another developer.

## Scope: Package and Drop Off

| In scope | Out of scope |
| --- | --- |
| Trace the feature's full dependency closure in the origin project | Integrating anything into `source/` |
| Copy the slice verbatim into `proposals/<slug>/` | Rewriting or generalizing the copied code |
| Extract only the relevant hooks into a fresh `.claude/settings.json` | Copying the origin project's whole settings or rules |
| Write the proposal README (use case, evidence, manifest, destination) | Deciding the proposal's fate (promote/delete) |
| Bootstrap `proposals/` with its folder README on first use | Editing or deleting other proposals |
| Zip the proposal on request for sharing | Committing - leave that to the user / repo convention |

## Locating the Tooling Repository

Proposals are written to `<agentic_rails_tooling>/proposals/`. If the `agentic_rails_tooling` repository is not at a known path, ask the user for its location before writing. Never create a `proposals/` folder inside the origin project.

The `proposals/` folder is deliberately **excluded from `rails_lint.py`**: slices are verbatim copies from foreign projects and must not be mutated to satisfy tooling-repo conventions. Do not "fix" lint-style issues in copied files.

## Proposal Layout

```text
proposals/<proposal-slug>/
  README.md                  # the pitch: use case, evidence, manifest, destination
  .claude/settings.json      # fresh file with only the hooks the feature needs
  .claude/hooks/...          # hook scripts, copied verbatim
  .claude/agents/...         # subagent definitions, copied verbatim
  CLAUDE.md                  # only the instruction sections that drive the feature
  context/...                # design docs / provenance worth carrying along
  <scripts, dependency manifests, assets as needed>
  <proposal-slug>.zip        # optional, created on request for sharing
```

- `<proposal-slug>` is kebab-case and names the **proposed capability** (e.g. `advisor-guard-rail`, `camera-validation-guard-rail`, `kotlin-rules`), not the origin project.
- Everything except `README.md` (and the optional zip) mirrors the origin project's layout, so the slice can be dropped into another project's root as-is.
- If the slug already exists in `proposals/`, ask the user whether to replace it or pick a new slug. Never silently overwrite.

## Slicing Rules

1. **Trace the full dependency closure.** Hooks and their scripts, agents, skills, rules, helper scripts, dependency manifests (`requirements.txt`, `package.json` fragments, `pyproject.toml`, etc.), design docs, and the `CLAUDE.md` / `AGENTS.md` sections that drive the behavior. The test: could another developer drop the slice into a fresh project and make it work using only what is inside the proposal?
2. **Copy verbatim.** The proposal preserves the proven artifact exactly as it ran. Generalization happens at promotion time, not here. If something genuinely cannot be copied as-is, alter it minimally and record the alteration in the README's Generalization Notes.
3. **Settings are extracted, not copied.** Never copy the origin `.claude/settings.json` wholesale. Create a fresh one containing only the hook entries (and other settings keys) the feature needs.
4. **Instructions are excerpted, not copied.** From `CLAUDE.md` / `AGENTS.md`, carry over only the sections that belong to the feature. Whole-project rules stay behind.
5. **Keep paths portable.** Preserve `$CLAUDE_PROJECT_DIR`-style relative paths; strip machine-absolute paths, usernames, and drive letters.
6. **Sanitize.** No secrets, API keys, tokens, credentials, or customer data. No transient state (session markers, caches, logs, `__pycache__`).
7. **Record the origin.** The README names the origin project and path so provenance survives even after the slice is shared or promoted.

## The Proposal README

`README.md` at the proposal root is the pitch a future curator (human or agent) reads to decide the proposal's fate. Write it from `references/proposal-readme-template.md`. It must stand alone: use case, the concrete evidence the feature worked in the origin project, why it deserves generalization, a file-by-file manifest, dependencies, a suggested destination in the Agentic Rails system, and honest notes on what is project-specific.

Ground the Evidence section in real observations from the origin project - sessions where the feature caught a problem, adoption on other machines or by other developers, design docs, commits. Do not invent proof; a proposal with thin evidence should say so.

## First Use: Bootstrap the Inbox

If `proposals/` does not exist at the tooling repo root, create it and write `proposals/README-PROPOSALS.md` from `references/proposals-folder-readme.md`. Do this once; never overwrite an existing folder README.

## Zip for Sharing

When the user asks to share the proposal (or says "zip it"), create `<proposal-slug>.zip` inside the proposal folder, containing the folder's contents except the zip itself. The zip is a snapshot: if the proposal changes afterwards, regenerate it. Mention the zip in the README manifest only if it is expected to be kept current.

## Operating Model

1. Confirm the tooling repository location (ask if unknown) and bootstrap `proposals/` if missing.
2. Ask the user (or read from their description) what the feature is, where it lives, and what evidence exists that it worked.
3. Explore the origin project and trace the feature's full dependency closure per the Slicing Rules.
4. Choose the kebab-case slug and create `proposals/<slug>/`.
5. Copy the slice verbatim, extracting hooks into a fresh `.claude/settings.json` and excerpting instruction sections.
6. Write `README.md` from the template, grounding the Evidence section in what you actually found.
7. If asked, produce the zip.
8. Report the proposal path and a one-paragraph summary of what was captured. Leave committing to the user.

## Boundaries

- Write only inside `proposals/<slug>/` (plus the one-time folder README). Never touch `source/`, `archived/`, `context/`, or other proposals.
- One proposal per invocation.
- Copy, do not improve: no refactoring, renaming, or lint-conforming of slice files.
- Never copy secrets, transient state, or the origin project's unrelated configuration.
- Do not promote, integrate, or delete anything - drop off and stop.

## Validation

Before considering the skill applied correctly, confirm:

- `proposals/<slug>/README.md` exists, follows the template, and its manifest matches the files actually present.
- The slice mirrors the origin layout and contains the full dependency closure - nothing needed to run the feature is missing.
- `.claude/settings.json` in the proposal contains only the feature's hooks and uses portable paths.
- No secrets, absolute machine paths, or transient state files were copied.
- Nothing outside `proposals/<slug>/` (and the one-time `README-PROPOSALS.md`) was created or modified.
