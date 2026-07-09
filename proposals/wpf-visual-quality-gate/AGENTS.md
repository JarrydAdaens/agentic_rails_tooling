# AGENTS.md Excerpt

This excerpt carries only the origin-project instruction sections that drive evaluation-gate behavior for the proposed WPF visual quality gate.

From `quota_tank/AGENTS.md`:

- Review matching evaluation gates in `context/evaluations/` when the task touches an area covered by an evaluation.
- Run matching `context/evaluations/` gates when task scope triggers them, using an independent evaluator sub-agent when available.

These instructions make a project-local evaluation gate operational: if a visible WPF UI change matches `context/evaluations/wpf-visual-quality-gate.md`, the implementing agent must run that gate or document why it could not.
