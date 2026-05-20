---
name: core-typescript
version: 1.0
agentic_rails_source_version: 1.0
---

# Core TypeScript

## Use This Reference When

- Writing or reviewing everyday TypeScript: variables, functions, classes, destructuring, enums, or common syntax
- Deciding how to express a common programming construct in idiomatic TypeScript
- A piece of code is valid JavaScript but not idiomatic TypeScript

## Veteran Expert Stance

TypeScript's value is not in decorating JavaScript with type annotations — it is in giving the compiler enough information to catch real bugs before runtime. Write TypeScript that makes intent explicit and lets the toolchain do meaningful work. Every use of `any` or a cast that bypasses the type system is a hole in that contract.

Everyday application code should be readable at a glance. Prefer clarity over cleverness, and use modern language features where they reduce noise without obscuring meaning.

## Core Syntax Choices

### Variables and Declarations

- Prefer `const`. Use `let` only when the binding will be reassigned.
- Declare one variable per statement.
- Initialize variables close to where they are first used.

```ts
const userId = params.get('id');
let retryCount = 0;
```

### Functions

- Prefer `function` declarations for module-level named functions. They hoist cleanly and are easy to locate.
- Prefer arrow functions for callbacks, closures, and inline expressions.
- Provide parameter types and return types on exported functions. Inferred types are acceptable on short private helpers where the return type is obvious from the body.

```ts
export function buildApiUrl(in_path: string, in_baseUrl: string): string {
  return `${in_baseUrl}/${in_path.replace(/^\//, '')}`;
}
```

### Classes

- Use classes when an object has meaningful state and lifecycle methods, or when implementing an interface contract.
- Prefer `readonly` for properties that should not be reassigned after construction.
- Avoid inheritance for code reuse. Prefer composition.
- Do not use classes as namespaces for static methods. Use a plain module with named exports instead.

### Destructuring

- Use object destructuring for function parameters when consuming several properties from an object.
- Use array destructuring for two-element returns such as `useState` pairs.
- Rename destructured variables when the original name is ambiguous in the local scope.

```ts
const { id, displayName, isActive } = user;
const [value, setValue] = useState('');
```

### Template Literals

- Prefer template literals over string concatenation for multi-part strings.
- Use tagged template literals only when the tag adds real value (localization, SQL escaping). Do not tag just for style.

### Enums

- Prefer `const enum` for compile-time-erased enums used only in TypeScript code.
- Prefer a string literal union (`'pending' | 'success' | 'error'`) for states that cross API boundaries or need to be serialized.
- Avoid numeric enums for anything that appears in data payloads or logs.

### Nullability

- Treat `null` and `undefined` as distinct. Use `null` for intentional absence, `undefined` for optional or unset values.
- Use optional chaining (`?.`) for safe property access on potentially null/undefined values.
- Use nullish coalescing (`??`) to provide defaults, not `||`, which also triggers on `0`, `false`, and `''`.

```ts
const name = user?.profile?.displayName ?? 'Anonymous';
```

## Practical Heuristics

- If a function does two conceptually separate things, split it.
- If a file exports more than one major concept, consider splitting it.
- Keep functions short enough to read without scrolling. If a function needs a comment to explain its structure, it is probably doing too much.
- Avoid deep nesting. Invert conditions and return early to reduce indent depth.
- Prefer `for...of` for iteration over arrays when the index is not needed. Use `.map()`, `.filter()`, `.reduce()` for transformations.

## Early Return Pattern

Flatten branching with early returns. This reduces nesting and makes the success path obvious.

```ts
export function getDisplayName(in_user: User | null): string {
  if (!in_user) return 'Guest';
  if (!in_user.profile) return in_user.email;
  return in_user.profile.displayName;
}
```

## Smells

- Functions with more than two levels of nesting without good reason
- `var` declarations in any context
- Using `||` as a null coalescing operator where `??` is more accurate
- Reassigning `const` by accident, worked around by switching everything to `let`
- Classes that contain only static methods — use a module instead
- String concatenation instead of template literals for multi-part strings

## Goal

Write TypeScript that reads like well-structured English and makes the compiler's job easy. Favor explicitness where it clarifies intent, and use modern language features to remove noise — not to be clever.
