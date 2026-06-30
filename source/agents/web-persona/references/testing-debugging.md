---
name: testing-debugging
metadata:
  version: "1.1"
---

# Testing and Debugging

## Use This Reference When

- Writing unit tests for TypeScript utility functions, hooks, or services
- Writing component tests for React components
- Mocking API calls or external dependencies in tests
- Setting up a test environment or reviewing test quality
- Debugging a TypeScript compiler error, runtime error, or test failure

## Veteran Expert Stance

Tests are the best documentation a codebase has, because they describe expected behavior in runnable form. Write tests that describe what the code should do, not how it does it. Tests that are coupled to implementation details — internal state, private methods, exact DOM structure — break when the code is refactored correctly.

The goal is not coverage percentage. The goal is confidence: when the test suite passes, the feature works as described. Prioritize testing the behavior that matters to the user and the boundaries where things can go wrong.

## Test Anatomy

Every test should follow the Arrange/Act/Assert pattern:

```ts
it('formats a user display name with first and last name', () => {
  // Arrange
  const firstName = 'Jane';
  const lastName = 'Smith';

  // Act
  const result = formatUserName(firstName, lastName);

  // Assert
  expect(result).toBe('Jane Smith');
});
```

One assertion per test where practical. Tests with multiple unrelated assertions are harder to diagnose when they fail.

## Unit Testing TypeScript Functions

- Test pure functions exhaustively: happy path, edge cases, and error cases.
- Test type guard functions with both valid and invalid inputs.
- Test error handling: verify that the right error type is thrown, not just that some error occurs.

```ts
describe('parseApiResponse', () => {
  it('returns a typed UserDto when the response shape is valid', () => {
    const raw = { id: '1', email: 'a@b.com', displayName: 'Alice', isActive: true };
    expect(parseApiResponse(raw)).toEqual(raw);
  });

  it('throws ValidationError when the id field is missing', () => {
    const raw = { email: 'a@b.com' };
    expect(() => parseApiResponse(raw)).toThrow(ValidationError);
  });
});
```

## Testing Custom Hooks

Use `@testing-library/react`'s `renderHook` utility to test hooks in isolation.

```ts
import { renderHook, act } from '@testing-library/react';
import { useToggle } from './useToggle';

describe('useToggle', () => {
  it('starts with the provided initial value', () => {
    const { result } = renderHook(() => useToggle(true));
    expect(result.current.isOn).toBe(true);
  });

  it('toggles the value on each call', () => {
    const { result } = renderHook(() => useToggle(false));
    act(() => { result.current.toggle(); });
    expect(result.current.isOn).toBe(true);
  });
});
```

## Testing React Components

Use `@testing-library/react` and query by accessible role, label, or text — not by CSS class or implementation detail.

```tsx
import { render, screen, fireEvent } from '@testing-library/react';
import { SaveButton } from './SaveButton';

describe('SaveButton', () => {
  it('calls onSave when clicked and not loading', () => {
    const onSave = vi.fn();
    render(<SaveButton isLoading={false} onSave={onSave} />);
    fireEvent.click(screen.getByRole('button', { name: 'Save' }));
    expect(onSave).toHaveBeenCalledOnce();
  });

  it('is disabled while loading', () => {
    render(<SaveButton isLoading={true} onSave={() => {}} />);
    expect(screen.getByRole('button')).toBeDisabled();
  });
});
```

Avoid testing internal state. Test what the user sees and does.

## Mocking API Calls

Do not hit real networks in unit or component tests. Mock at the service boundary.

- Mock service modules with `vi.mock` (Vitest) or `jest.mock`.
- Use `msw` (Mock Service Worker) for integration-level component tests that should be independent of the real service implementation.
- Return realistic shapes — test fixtures should match your DTO interfaces.

```ts
// Mocking a service module
vi.mock('@api/endpoints/users', () => ({
  fetchUser: vi.fn().mockResolvedValue({
    id: '1',
    email: 'test@example.com',
    displayName: 'Test User',
    isActive: true,
  } satisfies UserDto),
}));
```

## Vitest and Vite Integration

Prefer Vitest when the project uses Vite. It shares the Vite config, including path aliases, and runs significantly faster than Jest on Vite projects.

```ts
// vitest.config.ts
import { defineConfig } from 'vitest/config';
import { mergeConfig } from 'vite';
import viteConfig from './vite.config';

export default mergeConfig(viteConfig, defineConfig({
  test: {
    environment: 'jsdom',
    setupFiles: ['./src/test/setup.ts'],
    globals: true,
  },
}));
```

## Debugging

### TypeScript Compiler Errors

- Read the full error. TypeScript errors often have the actual problem at the bottom of a chain.
- Narrow the problem: simplify the type expression, add an explicit annotation, or isolate the failing call.
- Check that `tsconfig` paths and `baseUrl` are configured correctly when seeing "module not found" errors.

### Runtime Errors

- Use browser DevTools source maps. Ensure Vite generates them in development mode.
- Use `console.error` for unexpected error states; avoid `console.log` left in production code.
- For React rendering issues, use React DevTools to inspect the component tree and current props/state.

### Test Failures

- Start with the test failure message before reading the test code. The message usually describes the mismatch.
- For hook tests, wrap state-changing actions in `act()` to flush updates before asserting.
- For component tests, use `screen.debug()` to print the current rendered DOM when queries return unexpected results.

## Practical Heuristics

- If a function is hard to test, it is probably doing too much or has too many dependencies.
- If a test requires mocking many things, the unit under test has too many concerns.
- If a test is brittle (breaks when you change implementation without changing behavior), it is testing the wrong thing.
- Tests for validation and error handling are as important as tests for the happy path.

## Smells

- Tests that only verify method call counts without asserting observable outcomes
- Snapshot tests used broadly — they assert structure, not behavior, and accumulate noise
- Tests that import and assert on internal state or private module exports
- Mocking the module under test itself
- Test files with no test description (`it('works', ...)`)

## Goal

A test suite that gives genuine confidence in application behavior, where passing tests mean the feature works as described, and failing tests point clearly to the real problem.
