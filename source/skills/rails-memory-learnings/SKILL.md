---
name: rails-memory-learnings
description: Use this skill when the user requests a concise session learning in Rails memory; capture observed outcomes and reliable provenance without guessing identities or usage.
disable-model-invocation: true
argument-hint: "[--project <name>] [--memory <path>] [--dry-run]"
metadata:
  version: "2.1"
---

# Rails Memory Learnings

## Arguments

The skill was invoked with: $ARGUMENTS

Parse leniently and accept plain-language equivalents such as "preview the learning".

| Token | Meaning |
| --- | --- |
| `--project <name>` | Project identifier. Absent means derive from established project identity. |
| `--memory <path>` | Explicit memory repository. Absent means discover configured or known workspace memory; distinguish an actual instance from a template. |
| `--dry-run` | Return the artifact without writing. Absent means write the requested capture. |
| anything else | Session emphasis or source links. Empty arguments capture the current requested session. |

## Reference

- [Concise evidence and provenance](references/learning-format.md)

## Non-negotiable rules

This is the canonical rule list. Nothing else in this document restates it.

- Capture is optional and explicitly requested. Ordinary work has no required memory deposit, routing/resume update, or manufactured retrospective.
- Produce one concise learning in the actual memory repository's `memories/learnings/new/` location. Capture does not curate, rank models, change Resumes, promote rules, or write implementation status.
- Record requested and observed runtime identities separately, with evidence source. Model, effort, harness version, fast/reasoning mode, and usage stay `unknown` when not observed; task instructions alone do not prove an override took effect.
- Separate observations from inference and user reports. Do not invent praise, friction, token totals, causal savings, or model rankings. Partial receipts and estimates retain their limits and coverage.
- Sanitize secrets, private data, proprietary source, and reasoning traces. Preserve durable source links and hashes when useful; the artifact records conclusions and evidence only.
- Use collision-free kebab-case names for new captures. Existing historical names and schemas remain evidence and are not rewritten by this capture.
- Mint one stable observation ID and use the delivery owner's shared result ID, or mint a new result ID for a distinct attempt. Record participant roles against that shared outcome; no participant receives duplicated credit for the same result. The versioned observation block is immutable after capture, with interpretations separated from observations.
- Discover configured locations and known sibling repositories before asking for missing facts. A memory template is not an instance; unavailable writes can yield a complete inline draft with the destination limitation reported.
- Commit policy follows existing authority; capture does not authorize a commit or external message.

## Workflow

1. Resolve project, requested session, and memory destination from available evidence. Inspect the actual memory instructions/template and preserve its required parser fields.
2. Review the relevant delivery evidence, changed artifacts, commands, receipts, and session observations. Avoid a full repository rescan for a narrow capture.
3. Compose the concise learning using the reference's versioned observation block: actual outcome, one or two actionable observations, evidence, uncertainties, and runtime identity/usage coverage. Empty praise/problem categories need no filler.
4. Select a new target-root-relative name such as `memories/learnings/new/<project>-YYYY-MM-DD.md`, with `-2` on collision. Never overwrite an earlier learning. In dry run, return the complete draft.
5. Write only the one requested artifact and report path, meaningful observation, and material provenance limits.

## Observable output

One requested learning or complete dry-run draft contains supported observations, source links, and explicit identity/usage uncertainty. Existing memory records and Resumes remain untouched.
