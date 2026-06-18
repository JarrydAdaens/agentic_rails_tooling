---
metadata:
  version: "1.0"
---

# TypeScript Agent Design Document

## Purpose

Design a TypeScript-focused agent and rule system that helps produce good-quality TypeScript code for practical application development.

The agent must support engineering execution, not academic TypeScript theory. Its job is to help write sensible, modular, production-grade TypeScript that follows clear conventions and solid software design principles.

The target development environment is:

- **Backend:** ASP.NET / .NET API
- **Frontend:** React
- **Build tooling:** Vite
- **Primary language:** TypeScript

---

## Core Objectives

There are two major deliverables.

### 1. TypeScript Task Rules

Create a collection of task rules for working in TypeScript.

These rules define the expected shape, formatting, structure, and conventions of generated code. They act as the practical coding standard the agent must follow when producing or modifying TypeScript.

The rules should enforce:

- Clear, readable TypeScript
- Modular file structure
- Consistent formatting
- Predictable naming conventions
- Practical SOLID principles
- Avoidance of over-engineered abstractions
- Safe use of TypeScript types
- React + Vite frontend conventions
- Compatibility with a .NET-backed application architecture

These rules are not just linting preferences. They are behavioural constraints for the agent so its generated code consistently matches the desired engineering style.

### 2. TypeScript Agent With Reference Files

Create a TypeScript agent that uses a `references` folder.

The agent should not attempt to load all TypeScript knowledge into the context window at once. Instead, TypeScript knowledge must be split across multiple Markdown reference files, each representing a broad practical domain of TypeScript application development.

The agent must be able to decide which reference files are relevant to the task and load only those files.

This is a GPT-4-style architecture pattern: the agent keeps its general working behaviour lightweight, then selectively loads detailed domain references as needed.

---

## Agent Knowledge Behaviour

The agent should explicitly set aside broad prior assumptions and rely on the project-provided rules and references when working.

This means:

- The project rules take priority over generic TypeScript advice.
- The reference files define the agent’s working knowledge for this environment.
- The agent should choose relevant references based on the task.
- The agent should avoid bloating the context window with unrelated material.
- The agent should produce code suited to this stack: ASP.NET backend, React frontend, Vite tooling, TypeScript implementation.

---

## Proposed Folder Structure

```text
/typescript-agent/
  agent.md
  rules.md
  references/
    01-core-typescript.md
    02-type-system-practical-use.md
    03-modules-project-structure.md
    04-react-vite-frontend.md
    05-api-integration-dotnet.md
    06-state-data-flow.md
    07-error-handling-validation.md
    08-testing-debugging.md
    09-build-tooling-config.md
    10-maintainability-solid-principles.md
```

---

## Broad TypeScript Knowledge Domains

### 1. Core TypeScript Syntax

Covers everyday TypeScript syntax, variables, functions, classes, objects, arrays, enums, literals, and common language constructs used while writing application code.

### 2. Practical Type System Usage

Covers interfaces, type aliases, unions, generics, narrowing, inference, utility types, and type safety patterns used to make code reliable without becoming unreadable.

### 3. Modules and Project Structure

Covers imports, exports, file boundaries, barrel files, feature folders, shared libraries, dependency direction, and how to keep TypeScript projects modular.

### 4. React and Vite Frontend Development

Covers React component structure, hooks, props, events, JSX typing, Vite conventions, frontend folder layout, and avoiding messy component architecture.

### 5. API Integration With .NET Backends

Covers calling ASP.NET APIs from TypeScript, request/response typing, DTO boundaries, fetch clients, error responses, auth headers, and keeping frontend/backend contracts clean.

### 6. State and Data Flow

Covers local state, derived state, server state, shared state, view models, data ownership, mutation flow, and avoiding tangled frontend logic.

### 7. Error Handling and Validation

Covers runtime validation, typed error handling, user-facing errors, API failure handling, defensive parsing, and safely dealing with unknown external data.

### 8. Testing and Debugging

Covers practical TypeScript testing, React component tests, API mocking, unit test structure, debugging workflows, and writing code that is easy to verify.

### 9. Build, Tooling, and Configuration

Covers `tsconfig`, Vite config, ESLint, Prettier, package scripts, dependency management, strict mode, path aliases, and practical build pipeline concerns.

### 10. Maintainability and SOLID Principles

Covers clean architecture, separation of concerns, dependency boundaries, composition, readability, refactoring safety, avoiding over-abstraction, and building code that other engineers can maintain.

---

## Rules File Scope

The `rules.md` file should contain mandatory behavioural rules for the agent.

It should define how the agent writes code, not deep TypeScript knowledge. Deep knowledge belongs in the reference files.

Example rule categories:

- Formatting rules
- Naming conventions
- File organisation rules
- Type usage rules
- React component rules
- API boundary rules
- Error handling rules
- Testing expectations
- Refactoring behaviour
- Avoided patterns

---

## Reference File Scope

Each reference file should contain domain-specific guidance.

A reference file should answer:

- What problem domain does this cover?
- When should the agent load this file?
- What conventions apply in this domain?
- What patterns are preferred?
- What patterns are forbidden or discouraged?
- What examples clarify the expected style?

Each file should be small enough to load only when relevant.

---

## Agent Routing Behaviour

The agent should inspect the task and decide which references to load.

Examples:

| Task | References To Load |
|---|---|
| Create a React component | `04-react-vite-frontend.md`, `02-type-system-practical-use.md`, `10-maintainability-solid-principles.md` |
| Add API client code | `05-api-integration-dotnet.md`, `07-error-handling-validation.md`, `02-type-system-practical-use.md` |
| Refactor messy frontend state | `06-state-data-flow.md`, `10-maintainability-solid-principles.md`, `04-react-vite-frontend.md` |
| Fix build or compiler issue | `09-build-tooling-config.md`, `02-type-system-practical-use.md` |
| Add tests | `08-testing-debugging.md`, plus the relevant domain reference |

---

## Quality Bar

The output of the agent should be judged against these standards:

- Code is readable without explanation.
- Files have clear responsibility boundaries.
- Types help the engineer rather than obstruct them.
- React components are not overloaded with business logic.
- API boundaries are explicit and typed.
- Runtime data is treated as unsafe until validated or normalised.
- Error handling is predictable.
- Code avoids unnecessary cleverness.
- Generated code fits naturally into a React + Vite + ASP.NET environment.
- The agent follows project conventions over generic online advice.

---

## Implementation Plan

### Step 1: Create the Agent Shell

Create `agent.md` defining the TypeScript agent’s purpose, priorities, and reference-loading behaviour.

### Step 2: Create the Rules File

Create `rules.md` containing the mandatory style, formatting, architecture, and behavioural rules for TypeScript work.

### Step 3: Create the Reference Folder

Create the `references` folder and add the ten broad domain reference files.

### Step 4: Populate Each Reference File

Each reference file should include:

- Domain summary
- When to load it
- Preferred patterns
- Discouraged patterns
- Practical examples
- Stack-specific notes for React, Vite, and ASP.NET where relevant

### Step 5: Validate With Common Tasks

Test the agent against common work items:

- Build a React component
- Add an API client
- Refactor frontend state
- Fix a TypeScript compiler issue
- Add validation around API data
- Add unit tests

The agent is successful if it loads only relevant references and produces clean, modular TypeScript aligned with the project rules.

---

## Non-Goals

This design is not intended to create:

- A full academic TypeScript textbook
- A complete JavaScript language reference
- A generic frontend engineering agent
- A framework-agnostic web development agent
- A maximal context dump of every TypeScript concept

The goal is practical engineering support for building TypeScript applications in a React + Vite frontend backed by ASP.NET.

