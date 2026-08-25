---
name: rails-minion-workflow-intervention-report
description: The blocker record written when a story is blocked, the stopping challenge answered before a run ends, and the four-category summary a run produces for the human.
metadata:
  version: "1.0"
---

# Blocker Records and the Intervention Report

Everything here is written into the project's own documents — the story's entry in the milestone, or the plan it belongs to. There is still no run folder and no separate tracker.

## The blocker record

When a story becomes `Blocked` or `Deferred`, record it beside the story:

```markdown
### Blocker

**Blocked on:** <the concrete technical issue>

**Evidence:** <commands run, errors returned, observations, missing platform>

**Attempts made:**
- <what was tried, and what it produced>

**Partial progress completed:**
- <what landed and is usable>

**Possible next paths:**
- <what a future attempt should try first>

**Human input required:** <only when genuinely required, and what exactly>

**Can other milestone work continue?** Yes / No

**Next autonomous action:** <the story, plan, spike, or investigation starting now>
```

The last line is mandatory. Omit it only when there is truly no autonomous action left anywhere in the milestone — which is the same condition that permits ending the run.

A blocker record is not an apology and not a narrative. A reader who was not present should be able to pick the story up from it.

## The stopping challenge

Before ending a run, answer every one of these in writing:

```text
Why is stopping better than continuing?
What useful work remains anywhere in the milestone?
What experiments have not been attempted?
What could be partially completed?
What could be planned even though it cannot be executed?
What could be deferred, isolated, or tested?
What concrete external capability is missing?
Is the blocker global, or local to one story?
```

Any useful answer means the run continues. The challenge is not a formality to write and then override — it exists because the reflex to stop arrives dressed as a considered judgment, and writing the answers is what separates the two.

## The intervention report

An unattended run ends with a summary in four categories. Its purpose is to let the human spend their attention making decisions and removing blockers rather than reconstructing what happened.

**Completed** — stories and phases fully finished and verified.

**Partial** — useful work landed but the story is not resolved. State what remains.

**Blocked / Deferred** — one entry per item, carrying the blocker, the evidence, the attempts, the useful work already completed, the recommended next action, and any human input required. The blocker records written during the run are the source; this is where they are collected.

**Human decisions** — only strategic or genuinely external calls: provide an environment or credential, approve replacing a framework, choose between incompatible architectural directions, supply inaccessible hardware. An implementation problem that was merely hard does not belong in this category.

A report that lists a blocker with no attempts, no partial work, and no recommended next action is describing an abandoned story rather than a routed one.
