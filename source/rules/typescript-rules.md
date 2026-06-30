---
description: TypeScript coding rules — strict typing, naming, modules, and formatting for .ts and .tsx files.
globs: ["**/*.ts", "**/*.tsx"]
alwaysApply: false
metadata:
  version: "1.0"
  owner: Jarryd Adaens
---

# TypeScript Coding Rules

## Scope

Applies to all `.ts` and `.tsx` files in this workspace.

Intent: readable, strict, consistent TypeScript that works well in a React + Vite frontend and integrates cleanly with an ASP.NET backend.

## Language

- Enable and maintain strict mode (`"strict": true` in `tsconfig`). Never relax it to suppress errors.
- Do not use `any`. When the type is genuinely unknown, use `unknown` and narrow it before use.
- Do not use non-null assertions (`!`) without a comment explaining why the value cannot be null or undefined at that point.
- Use `unknown` for untyped external data: API responses before validation, `JSON.parse` results, event payloads from third parties.
- Prefer `const` over `let`. Use `let` only when reassignment is genuinely required.
- Avoid implicit returns in complex functions. Be explicit about what is returned.
- Use `async`/`await` for asynchronous work. Avoid raw `.then()` chains in application code.

## Naming

- Types, interfaces, enums, and classes: `PascalCase`.
- Variables, functions, and methods: `camelCase`.
- Module-level constants that are truly constant: `SCREAMING_SNAKE_CASE`.
- Boolean variables and properties: prefix with `is`, `has`, `can`, or `should` (`isLoading`, `hasError`).
- Parameters: `camelCase` with the `in_` prefix (`in_userId`, `in_options`).
- Avoid single-letter names except simple loop counters. Avoid unclear acronyms.

## Types

- Prefer `interface` for object shapes that may be implemented or extended.
- Use `type` for unions, intersections, mapped types, and aliases that are not object shapes.
- Provide explicit return types on all exported functions. Inferred return types are acceptable on private/local helpers when the type is obvious.
- Use generic type parameters when a function or type is genuinely reusable across multiple input shapes.
- Use discriminated unions (a shared literal field) rather than optional fields when a value can be in one of several clearly different states.
- Use `Readonly<T>` or `readonly` fields when a data structure should not be mutated after construction.
- Use utility types (`Partial`, `Pick`, `Omit`, `Required`, `Record`) to derive types rather than duplicating definitions.

## Modules

- Prefer named exports over default exports. Named exports are more refactor-safe and easier to discover.
- One primary export per file for components and services. Utility files may export multiple related functions.
- Do not create deep barrel re-export chains. Barrel files at the feature folder boundary are acceptable; nested barrels compound the problem.
- Group imports: external packages first, then internal aliases, then relative imports. Separate each group with a blank line.

## Formatting

- Indent with 2 spaces. No tabs.
- Single quotes for strings. Template literals when interpolating.
- Semicolons at the end of statements.
- Maximum line width approximately 100 characters.
- Trailing commas in multi-line arrays, objects, and function parameters.
- One statement per line. One declaration per line.

## Do Not

- Do not use `any`. It silently disables type checking across call sites.
- Do not use non-null assertions without a justifying comment.
- Do not use `// @ts-ignore` or `// @ts-expect-error` as a first resort. Fix the underlying type problem.
- Do not leave unused imports. Remove them when they are no longer needed.
- Do not rely on implicit `any` through untyped function parameters or empty object types (`{}`).
- Do not write separate `.d.ts` type files alongside implementation files for internal code. Keep types co-located with their implementation.

## Examples

```ts
// Named export, explicit return type, in_ parameter prefix
export function formatUserName(in_firstName: string, in_lastName: string): string {
  return `${in_firstName} ${in_lastName}`;
}

// Interface for object shape
interface UserSummary {
  readonly id: string;
  displayName: string;
  isActive: boolean;
}

// Discriminated union
type ApiResult<T> =
  | { status: 'ok'; data: T }
  | { status: 'error'; message: string };

// unknown for external data — validate before use
function parseApiResponse(in_raw: unknown): UserSummary {
  if (!isUserSummary(in_raw)) {
    throw new Error('Invalid API response shape');
  }
  return in_raw;
}
```
