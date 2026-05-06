---
name: type-system-practical-use
version: 1.0
---

# Practical Type System Usage

## Use This Reference When

- Designing or refining TypeScript types, interfaces, or generics
- Choosing between `interface` and `type`, or between a union and optional fields
- Applying type narrowing, guards, or assertion patterns
- Using utility types or mapped types to avoid duplicated definitions
- Working with generic functions or components that need to remain type-safe across multiple shapes

## Veteran Expert Stance

TypeScript's type system is a tool for communicating programmer intent to the compiler — not a puzzle to be solved. A type that is technically valid but requires a comment to explain should be simplified. A type that describes reality accurately is more valuable than one that is clever.

The goal is type safety that helps the engineer rather than one that obstructs them. Avoid types that are too narrow to be practical, too loose to be safe, or too deep to read.

## Interface vs Type

- Use `interface` for object shapes: data structures, API responses, component props, service contracts. Interfaces are extendable and produce cleaner error messages.
- Use `type` for unions, intersections, mapped types, conditional types, and aliases where you are not describing a single object shape.

```ts
// Interface — object shape
interface UserProfile {
  id: string;
  displayName: string;
  isActive: boolean;
}

// Type alias — union of literal states
type RequestStatus = 'idle' | 'loading' | 'success' | 'error';
```

## Discriminated Unions

Prefer discriminated unions over optional fields when an object can be in one of several clearly different states. A shared literal field (`status`, `type`, `kind`) makes narrowing exhaustive and safe.

```ts
type ApiResult<T> =
  | { status: 'ok'; data: T }
  | { status: 'error'; message: string; code: number };

function handleResult<T>(in_result: ApiResult<T>): T | null {
  if (in_result.status === 'ok') return in_result.data;
  console.error(in_result.message);
  return null;
}
```

## Generics

- Use generics when a function, hook, or type is genuinely reusable across multiple input shapes.
- Name generic parameters descriptively when they are not obvious: `TData`, `TError`, `TItem` rather than just `T` in complex signatures.
- Constrain generics with `extends` when the body needs to access known properties.

```ts
function getById<TItem extends { id: string }>(
  in_items: TItem[],
  in_id: string
): TItem | undefined {
  return in_items.find((item) => item.id === in_id);
}
```

## Type Narrowing

Use TypeScript's control-flow narrowing rather than casting. The compiler tracks types through `if`, `switch`, `instanceof`, and `in` checks.

- Use `typeof` for primitives.
- Use `instanceof` for class instances.
- Use `in` for object property presence.
- Write user-defined type guards (`is` predicates) when narrowing needs to be reusable or cross a function boundary.

```ts
function isUserProfile(in_value: unknown): in_value is UserProfile {
  return (
    typeof in_value === 'object' &&
    in_value !== null &&
    'id' in in_value &&
    'displayName' in in_value
  );
}
```

## Utility Types

Use standard utility types to derive types rather than duplicating definitions.

| Utility | When to use |
|---|---|
| `Partial<T>` | All fields optional — update payloads, patches |
| `Required<T>` | All fields required — after defaults applied |
| `Readonly<T>` | Immutable snapshot — event payloads, frozen state |
| `Pick<T, K>` | Subset of an interface — view model slices |
| `Omit<T, K>` | All but some fields — create vs. read DTOs |
| `Record<K, V>` | Typed map — lookup tables, indexed objects |
| `NonNullable<T>` | Strip null/undefined — post-validation values |
| `ReturnType<F>` | Infer return type — avoid duplicating function signatures |

## Readonly and Immutability

- Use `Readonly<T>` or `readonly` field modifiers on data structures that should not be mutated after construction.
- Use `ReadonlyArray<T>` (or `readonly T[]`) for arrays that must not be pushed to or spliced.
- This is especially important for props, context values, and any data derived from the server.

## Avoiding Common Traps

- Do not cast with `as` to silence errors. Fix the underlying type problem instead.
- Do not widen types to `any` or `object` to make TypeScript stop complaining.
- Do not use function overloads for simple cases where a union parameter is clearer.
- Do not use `keyof typeof someEnum` as a workaround for a design that should have used a string union in the first place.
- Do not write types that mirror your runtime validation: write one and derive the other.

## Smells

- Excessive `as` casts throughout the codebase — usually a sign that types were added after the fact
- Optional fields used to represent a discriminated state (`error?: string` alongside `data?: T` instead of a union)
- Duplicated interface shapes with slightly different field sets — use `Omit`, `Pick`, or extend instead
- Generic parameters that are never constrained or used in the return type (effectively unused)
- `Record<string, any>` used as a catch-all instead of defining a real shape

## Goal

Design types that accurately describe the data they represent, make illegal states unrepresentable where practical, and help engineers understand the shape of data without reading through implementation details.
