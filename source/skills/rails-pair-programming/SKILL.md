---
name: rails-pair-programming
description: >-
  Use this skill when the user explicitly requests an Agentic Rails
  pair-programming session for exploration, debugging, or collaborative changes.
disable-model-invocation: true
argument-hint: "<topic> [--explore|--collaborate] [--story <slug>] [--implement] [--save <path>]"
metadata:
  version: "3.0"
---

# Rails Pair Programming

## Arguments

The skill was invoked with: $ARGUMENTS

Parse leniently and treat natural-language equivalents as equal to the tokens.
"Fix this with me" authorizes in-scope implementation; no magic switch is needed.

| Token | Meaning |
| --- | --- |
| `--explore` | Explain or investigate. Absent means infer intent from the request. |
| `--collaborate` | Work through concrete choices together. Absent means infer intent. |
| `--story <slug>` | Source work item when known. Absent means load relevant established context; a story is optional. |
| `--implement` | Explicit in-scope code authorization. Absent still permits changes clearly requested in natural language; exploration alone does not authorize implementation. |
| `--save <path>` | Save session notes there. Absent means update an existing useful plan/record, or provide the summary inline; no compulsory new artifact. |
| anything else | Topic or requested change. Empty arguments use the active request; ask only if no useful intent can be inferred. |

## Non-negotiable rules

This is the canonical rule list. Nothing else in this document restates it.

- Explicit activation begins the session. Infer exploration or implementation
  from the user's actual words and honor existing authority across turns; do not
  repeat mode-confirmation rituals or require a literal token for an authorized fix.
- Read only relevant project context and source evidence. A missing Story or
  Implementation Plan does not require inventing one for a routine change.
- Preserve unrelated dirty work and accepted decisions. Ask only when a required
  noninferable choice blocks the next action; continue independent useful work.
- Verify the changed artifact proportionately and report actual outcomes.
  Commit, publication, and external messaging remain governed by session authority.
- Keep decisions and continuation notes in an existing useful record when
  needed. A save request produces the requested artifact; ordinary pairing does
  not require a new session file or duplicate tracker.

## Collaborative loop

1. State the next useful action briefly. Read the relevant files, current request,
   and applicable instructions; inspect baseline changes before implementation.
2. Explain choices through the actual code, test ideas, and act on authorized
   changes. Adapt depth to the user; use short questions only for real choices.
3. Record consequential decisions and check evidence in the chosen existing
   project record, or requested notes file. Link an external status owner rather
   than creating local story state.
4. Respond to new steering while keeping the intended outcome. Wrap up when the
   requested work is complete or the user asks, with changes, checks, open items,
   and the saved path when a file was requested.

## Surviving compaction

For a long session, checkpoint intent, authority, decisions, changed paths,
verification identity, and the next step in the active plan or resolved notes
record before context is lost. On continuation reload that record with current
file/Git state. Short sessions can end with an inline summary.

## Observable results

Natural-language requests for changes proceed without repeated mode permission.
Exploration stays within its request, saved notes exist when requested, and
reported decisions and verification are supported by observed evidence.
