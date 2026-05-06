---
name: maintainability-solid-principles
version: 1.0
---

# Maintainability and SOLID Principles

## Use This Reference When

- Refactoring code that has grown too large, too coupled, or too hard to change
- Deciding how to split a module, hook, or component that is doing too much
- Designing a new feature with clean separation of concerns in mind
- Reviewing code for architectural problems beyond correctness
- Weighing how much abstraction is appropriate for a given problem

## Veteran Expert Stance

SOLID principles are a set of constraints that keep code changeable. Code that violates them is not necessarily wrong today — it is wrong when the second requirement arrives, because it forces a rewrite instead of an extension. The discipline is in recognizing when a principle is being violated before the code becomes painful, not after.

In a TypeScript/React codebase, the most damaging violations are usually: components that are too large to reason about (Single Responsibility), modules that are too tightly coupled to their collaborators (Dependency Inversion), and abstractions introduced before the second use case existed (premature abstraction). The antidote to premature abstraction is not no abstraction — it is waiting until the second real use case before extracting.

## Single Responsibility

Each module, component, hook, or function should have one reason to change.

- A component is responsible for: rendering a specific piece of UI given props.
- A hook is responsible for: managing one concern (data fetching, form state, a toggle).
- A service is responsible for: one resource or domain boundary (users, orders, auth).
- A utility function is responsible for: one well-named transformation.

When a component renders, fetches, validates, and formats — it has four reasons to change. Split it.

## Open/Closed

Code should be open for extension but closed for modification.

In practice: prefer adding new files and new types to modifying existing ones. Use discriminated unions and type narrowing over adding fields to an existing type. Use composition over editing existing components.

```ts
// Closed to modification — new notification types extend via the union
type Notification =
  | { kind: 'success'; message: string }
  | { kind: 'error'; message: string; retryable: boolean }
  | { kind: 'info'; message: string; timeout: number };
```

## Liskov Substitution

A component or function that accepts an interface must work correctly with any conforming implementation.

In TypeScript terms: if you accept a `UserSummary`, do not internally cast it to a `FullUser` and access fields that are not on the interface. If your hook says it returns a `UseAuthResult`, it must return a complete and consistent object regardless of whether the user is authenticated.

## Interface Segregation

Do not force consumers to depend on interfaces they do not use.

- Component props should include only what that component actually needs.
- Service interfaces should be split by use case: a component that only reads user data should not receive a full user management service with create/update/delete methods.
- Use `Pick<T, K>` to expose only the relevant fields from a larger type to a specific consumer.

```ts
// The button only needs these two fields from the full User object
interface UserAvatarProps {
  readonly displayName: Pick<UserDto, 'displayName'>['displayName'];
  readonly avatarUrl: string | null;
}
```

## Dependency Inversion

High-level modules should not depend on low-level implementations.

- Pass service dependencies into hooks and components rather than importing them directly. This makes them testable in isolation.
- Define the interface that a collaborator must fulfill, not the concrete class.
- In React, this often means passing callbacks as props rather than calling a global function directly.

```tsx
// Depends on an interface — easy to test, easy to replace
interface OrderFormDependencies {
  onSubmit: (in_order: CreateOrderRequest) => Promise<void>;
  onCancel: () => void;
}

export function OrderForm({ onSubmit, onCancel }: OrderFormDependencies) {
  // ... no direct import of any API module
}
```

## Composition Over Inheritance

- Prefer combining small, focused components and hooks over building class hierarchies or deep HOC chains.
- When two components share visual structure, extract the shared piece as a reusable component rather than a base class.
- When two hooks share logic, extract the shared logic as a third hook that both call.

## Avoiding Over-Abstraction

Abstraction has a cost: indirection, naming overhead, a surface that must be maintained. Pay that cost only when there is a real benefit.

Signs that an abstraction is premature:
- It has only one implementation.
- The generic parameter is never varied in practice.
- The interface was extracted before a second consumer existed.
- The abstraction is harder to explain than the concrete code it replaced.

The rule of three: introduce an abstraction when a pattern appears for the third time, not the first or second.

## Practical Heuristics

- If changing one thing requires changes in three places, the coupling is too high.
- If a file is over 300 lines, it probably has more than one responsibility.
- If a function needs a comment explaining its structure, it is likely two or more functions.
- If two modules need to import each other, there is a missing third module that should own the shared dependency.
- If you cannot name what a module does in a single noun phrase, it is doing too much.

## Refactoring Discipline

- Refactor in isolated steps. Do not mix refactoring with behavior changes in the same commit.
- Ensure tests exist for the behavior being refactored before starting.
- Rename before restructuring. If the current name is wrong, fix that first.
- Prefer moving code to a better location over rewriting it unless the logic itself is the problem.

## Smells

- A component that imports from 5+ different service modules — too many responsibilities
- A hook called `useAppState` or `useData` — name describes nothing
- A utility file called `helpers.ts` or `utils.ts` without a domain qualifier — a dumping ground
- Functions with boolean flags controlling fundamentally different behavior paths — split into two functions
- Abstractions built for one use case "to be ready for future needs" — YAGNI

## Goal

A codebase where each piece has a clear, singular responsibility, modules are loosely coupled at clear boundaries, and abstractions exist because they earn their place — not because they seemed like a good idea when the code was first written.
