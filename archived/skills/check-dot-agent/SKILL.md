---
name: check-dot-agent
description: >-
  Use this skill when the user wants to verify whether an agentic IDE or tool
  can discover and run skills from the global `%USERPROFILE%\\.agents` folder.
  When active, output the exact validation text in chat and do not add extra
  commentary.
metadata:
  version: "1.0"
---

# Check Dot Agent

This skill is a fast compatibility check for agentic IDEs and related tooling.

Its only job is to confirm that the skill was discovered and activated from the
expected global agent folder setup.

## Instructions

- Output exactly this text in the chat window: `Yup, I can see the .agents folder bro!`
- Do not add any extra explanation before or after the text.
- Do not rewrite, sanitize, or expand the message.
- If the user asks what this skill does, explain that it is a discovery test for global `.agents` folder support.

## When to use

- When the user wants to test whether a tool can see skills from `%USERPROFILE%\\.agents`.
- When validating whether an IDE supports global shared agent configuration instead of per-tool folders.

## Do not use

- Do not use this for normal skill validation, agent design, or repository audits.
- Do not run commands; this is a chat-only discovery signal.
