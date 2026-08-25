---
name: rails-minion-workflow-blocker-ladder
description: The nine responses a blocked Minion works through before stopping, and the doctrine behind them - a blocker is a routing decision, not an ending condition.
metadata:
  version: "1.0"
---

# Blocker Ladder

A blocker is a routing decision, not an ending condition.

Finding a problem and describing it is half of engineering. The other half is resolving, mitigating, isolating, or routing around it. A Minion that reports an obstacle and stops has done half the work and called it done.

## Doctrine

**Progress is the default.** The question on hitting an obstacle is not "what is wrong here" but "what are the viable ways forward". Both get asked; only the second one ends the turn.

**A concern travels with a path.** Naming a risk without a mitigation, an experiment, a smaller scope, a workaround, a decomposition, a deferral, or a concrete request for human input is an incomplete finding.

**The burden of proof is on stopping.** "This is risky", "this could regress", "this is complicated", "the architecture is unclear", "a human should look at this" — none of those are conclusions. They are the starting point of the work. Translate the risk into a concrete consequence, then look for the mitigation.

**Experiments beat speculation.** When uncertainty is cheap to resolve, resolve it: invoke `rails-spike` rather than reasoning about what might happen. Version control is the safety mechanism — work can be reverted, branched, cherry-picked, or discarded, so uncertainty alone is never a reason not to try.

**Partial progress is progress.** The most useful achievable improvement beats all-or-nothing completion. Upgrade to the newest compatible version rather than attempting a disruptive rewrite. Implement the one missing call rather than replacing the subsystem. Fix five of eight cases and document the other three.

**Tactical creativity is yours to use.** Local, reversible, implementation-level decisions — a wrapper, an adapter, a compatibility shim, a stub, a temporary fallback, instrumentation, a split into phases — need no permission. Document them where they create debt or need later review.

**Strategic redefinition is not.** Abandoning a framework, replacing the rendering architecture, migrating engines, changing target platform, rewriting a major subsystem, or materially changing product requirements are human decisions. Document the decision point, preserve the evidence, and continue with unrelated work. A strategic blocker blocks the work it touches, not the milestone.

**There is no idle state.** If implementation is blocked, planning, decomposition, investigation, test improvement, documentation, dependency analysis, migration notes, and spikes are all still available. The standing question is: what is the highest-value work available with the capabilities I have right now?

## The ladder

Work down it. Stop descending as soon as one rung produces useful work; a rung that fails sends you to the next, not to the end.

**1 — Solve directly.** Try the obvious implementation. Read the error. Inspect the surrounding code. Use the patterns the project already uses.

**2 — Try alternatives.** Do not fixate on the first approach. A different API, a different dependency version, a wrapper, an adapter, a fallback path, a compatibility shim, a smaller implementation.

**3 — Run a spike.** When the right solution is genuinely ambiguous, invoke `rails-spike` by name and let evidence settle it. Prolonged reasoning about what might work is the thing a spike exists to replace.

**4 — Decompose.** A task too large or too tangled to move gets split — `rails-planning-phaser` by name, or a manual split at natural seams. Then execute the phases that are not blocked.

**5 — Complete a useful subset.** Ask what part of this can be finished. Port the non-blocked layer. Complete interfaces and tests while the platform integration stays unavailable. Document what was left out and why.

**6 — Isolate and defer.** Mark the blocked story or phase `Blocked` or `Deferred`, write the blocker record from [intervention-report.md](intervention-report.md), and continue immediately.

**7 — Switch stories.** Take the next runnable story. A blocked story holds up the milestone only where a real dependency exists.

**8 — Produce future leverage.** When nothing can be executed, reduce the cost of executing later: write the missing plans, refine existing ones, run the investigation, map the dependencies, identify affected files, prepare the test cases, write the migration notes.

**9 — Human intervention.** The last rung, reachable only when every rung above it is genuinely exhausted.

## Anti-fixation

Tenacity is not repeatedly attacking the same wall. Tenacity is refusing to waste an available opportunity for progress.

Two attempts at the same approach without new evidence is the signal to change rung, not to try a third time. Repeating an approach because it *should* work is how a run burns an afternoon on one call site while eleven runnable stories wait.

## Where stopping is legitimate

Two terminal states, both concrete:

**Milestone exhausted.** No useful work remains anywhere. Every story is complete, or reduced to a documented intervention item with no autonomous work left against it.

**Global hard block.** No meaningful progress is possible anywhere in the milestone, for a reason that names a missing capability rather than a difficulty — a required platform, environment, credential, or piece of hardware that is genuinely unavailable, with no story, plan, test, investigation, documentation task, or spike able to proceed without it.

"The current story is difficult" is neither of these.
