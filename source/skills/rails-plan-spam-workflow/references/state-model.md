---
name: rails-plan-spam-state-model
metadata:
  version: "4.0"
---

# Queue and recovery

The coordinator owns planning dispatch; an existing tracker owns story state
when adopted. Record queued source links, output paths, worker ownership, accepted
content hashes, source/template identities, and blockers in the chosen run record.
No second editable story-status table is required.

Queued work becomes active before dispatch. A returned plan remains pending
acceptance until path, content, and relevant checks are inspected. Accepted plans
are identified by their file digest, not a worker's claim. Open questions do not
prevent acceptance when the plan records uncertainty and useful next steps.

On restart check active workers and existing outputs first. Reuse unchanged
accepted outputs, inspect pending ones, and report source/template changes rather
than silently regenerating the whole batch. Dirty preexisting plans require an
authorized revision and preservation. Blocked items need new evidence or a
deliberate retry decision before consuming more work.

Run records remain while they are the only continuation evidence. Retire only
owned records whose useful evidence already lives in accepted plans or source
items, through an authorized cleanup; never delete accepted plans as run cleanup.
