---
name: code-philosophy-and-readability
version: 1.0
---

# Code Philosophy and Readability

## Use This Reference When

- The task touches code style, naming, comments, readability, or code review standards
- You need to decide whether a "clever" implementation is worth it
- You need the default coding stance for game code before framework-specific details take over

## Expert Stance

Readability is king. The developer is God.

Game code should optimize for the humans maintaining it, extending it, debugging it, and onboarding into it. Performance can often be recovered somewhere else. Human confusion is more expensive than a few extra lines of code.

Build strong architecture first. Use rails that make the correct path easy and the stupid path hard. Verbose is fine. Clever is expensive.

## Core Rules

- Never reduce readability just to make code "look faster" when the real runtime win is unclear or small.
- Expand dense logic into multiple lines when that makes mistakes easier to spot.
- Do not abuse ternaries, deeply nested conditionals, or one-line stunts that hide intent.
- Use names that optimize comprehension, not typing speed. If the right name is long, use the long name.
- Avoid acronyms unless they are truly universal in the local codebase and domain.
- Follow the existing codebase's formatting style instead of turning style wars into the real task.
- Comment class and method intent, tricky behavior, and non-obvious rationale. Do not waste comments on obvious statements.

## Practical Heuristics

- If a senior engineer would need to slow down and parse it twice, simplify it.
- If the explanation of a variable needs a sentence, prefer the sentence as the name over a compressed abbreviation.
- If a helper makes the human-facing code clearer and the compiler can optimize it away, keep the helper.
- If the code only looks "clean" because important detail is hidden, it is not actually clean.

## High-Signal Quotes

- "Readability is king. The developer is God."
- "You should never ever reduce readability to make it go faster."
- "It's more important to optimise the developer than to micro-optimise the machine."
- "Lines of code don't cost any money."
- "Do not abuse ternaries."
- "It is a fucking sin to use acronyms."
- "You need good commenting and thorough commenting."

## Common Mistakes

- Copying software-fashion patterns that make game code harder to read for no real project benefit
- Compressing logic to look smart instead of making bugs obvious
- Pretending comments are unnecessary because the code is "self-documenting"
- Letting stale comments survive nearby changes until nobody trusts the docs anymore
