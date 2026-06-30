---
name: modules-project-structure
metadata:
  version: "1.1"
---

# Modules and Project Structure

## Use This Reference When

- Deciding how to organize a TypeScript project's files and folders
- Choosing an import/export strategy
- Introducing or auditing barrel files
- Setting up a feature folder layout or shared library structure
- Ensuring module boundaries prevent unwanted coupling

## Veteran Expert Stance

A module structure should make code easy to find, hard to couple incorrectly, and safe to delete or refactor. The test of a good structure is whether a new engineer can navigate to the right file without reading all the imports. Clever monorepo tricks and deep barrel chains can hide that a structure has no actual design.

Keep dependency direction explicit and unidirectional. Components should not reach into service internals; services should not import from UI layers; shared code should not depend on feature-specific code.

## Recommended Folder Structure

A React + Vite + ASP.NET project typically benefits from a feature-first layout at the application level, with shared infrastructure in dedicated folders.

```
src/
  features/
    users/
      components/
      hooks/
      services/
      types.ts
      index.ts          ← barrel for this feature's public surface
  shared/
    components/
    hooks/
    utils/
    types/
  api/
    client.ts           ← base fetch client
    endpoints/
  app/
    App.tsx
    router.tsx
  main.tsx
```

## Import and Export Rules

- Use named exports. Default exports make refactoring harder because editors cannot reliably rename them across call sites.
- Export from the source file directly. Only introduce a barrel (`index.ts`) at a deliberate module boundary.
- Import what you use directly. Do not import a whole module and destructure it elsewhere.

```ts
// Correct — named export from source
export function useUserProfile(in_userId: string): UseUserProfileResult { ... }

// Correct — barrel at feature boundary
// features/users/index.ts
export { useUserProfile } from './hooks/useUserProfile';
export type { UserProfile } from './types';
```

## Barrel Files

Barrels serve one purpose: defining the public surface of a feature or library. They are not a convenience for lazy imports.

- One barrel per feature folder, at the feature root.
- Barrels export only what should be consumed from outside the feature. Internal implementation files are not re-exported.
- Do not chain barrels across multiple levels. If a barrel re-exports from another barrel, the dependency graph becomes invisible.
- Do not use a root `src/index.ts` that re-exports everything. This is the most common source of circular dependency problems.

## Dependency Direction

Enforce a strict direction:

```
features/* → shared/* → (nothing in src)
api/*      → shared/types
app/*      → features/*, shared/*, api/*
```

- Feature code should not import from other features directly. Promote shared logic to `shared/` or compose at the `app/` level.
- Shared code must not import from feature code.
- API client modules should not import from component or hook code.

Circular imports are a symptom of a missing abstraction or incorrect placement of a type or function.

## Co-location

Place files close to where they are used.

- A hook used only in one component lives next to that component.
- A type used only in one feature lives in that feature's `types.ts`.
- A utility used across multiple features lives in `shared/utils/`.
- Move code outward (toward `shared/`) only when a second consumer appears.

## Path Aliases

Configure Vite and `tsconfig` path aliases to avoid fragile relative imports.

```ts
// tsconfig paths
"@features/*": ["src/features/*"],
"@shared/*":   ["src/shared/*"],
"@api/*":      ["src/api/*"]
```

Use aliases for cross-feature and cross-layer imports. Use relative imports within a feature folder.

## Practical Heuristics

- If you need to look at more than two folders to understand a feature, the structure is too flat or the feature is underbounded.
- If deleting a feature requires edits in more than two other places, the feature is leaking implementation details.
- If a barrel re-exports 20+ items, it is probably exporting internal details that should stay internal.
- If a utility file is in `shared/` but has only one consumer, move it to that consumer's feature folder.

## Smells

- Default exports on components, hooks, and services — inhibits rename refactoring and import tracing
- Barrel files that re-export implementation details just to make imports shorter
- Features that import from each other directly rather than through a shared abstraction
- All types in a single monolithic `types.ts` at the root — types should live close to where they are used
- Deep relative import paths (`../../../../shared/utils/format`) — a sign that path aliases are not configured

## Goal

A project structure that makes the correct way to add a new file obvious, makes cross-feature coupling hard to introduce accidentally, and keeps module boundaries clear enough that any file can be refactored or deleted with confidence.
