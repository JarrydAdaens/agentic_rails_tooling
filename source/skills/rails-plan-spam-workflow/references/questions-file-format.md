---
name: rails-plan-spam-questions-file-format
metadata:
  version: "4.0"
---

# Questions and decisions

Each plan or source tracker records its own unresolved decisions. Workers
distinguish facts they can discover from choices requiring user input, and
preserve accepted answers rather than reasking them.

An optional run questions overview contains source links and affected work,
without copying mutable question status or answers. Cross-cutting decisions
live once in the authoritative project record and are linked by affected plans.

```markdown
# Questions for <named batch>

- <Source item or plan section>: <brief unresolved decision and affected scope>.
- <Authoritative shared decision>: <affected plans>.
```

Use the actual resolved links. A plan can be accepted with unresolved questions
when its assumptions, dependencies, and next action are explicit. Blocking
decisions pause only dependent work; continue independent items in the batch.
