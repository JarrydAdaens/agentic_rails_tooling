---
name: error-handling-validation
metadata:
  version: "1.1"
---

# Error Handling and Validation

## Use This Reference When

- Handling errors from API calls, async operations, or user actions
- Validating runtime data from external sources: API responses, form inputs, URL parameters
- Typing error states and error response shapes
- Deciding how errors should surface to the user
- Safely parsing data of unknown shape

## Veteran Expert Stance

TypeScript provides static safety. Runtime validation provides dynamic safety. They are complementary, not redundant — and you need both.

At every boundary where data enters the application from outside — API calls, form submissions, URL params, localStorage, third-party libraries — assume the data is untrustworthy until you have checked its shape. A TypeScript cast (`as UserDto`) is not validation. It is a promise to the compiler that you know what the data looks like. That promise can be broken at runtime.

Error handling is not just about not crashing. It is about putting the user in a state where they know what happened and what to do next.

## Typed Error Classes

Define application-specific error types rather than throwing raw strings or generic `Error` objects.

```ts
export class ApiError extends Error {
  constructor(
    public readonly status: number,
    public readonly body: string,
    public readonly traceId?: string
  ) {
    super(`HTTP ${status}`);
    this.name = 'ApiError';
  }

  get isNotFound(): boolean { return this.status === 404; }
  get isUnauthorized(): boolean { return this.status === 401; }
  get isBadRequest(): boolean { return this.status === 400; }
}

export class ValidationError extends Error {
  constructor(public readonly fields: Record<string, string[]>) {
    super('Validation failed');
    this.name = 'ValidationError';
  }
}
```

## Catching and Narrowing Errors

`catch` blocks receive `unknown` in strict TypeScript. Narrow before using.

```ts
try {
  await submitOrder(order);
} catch (err) {
  if (err instanceof ApiError && err.isBadRequest) {
    setFieldErrors(parseValidationErrors(err.body));
  } else if (err instanceof ApiError) {
    setGlobalError(`Request failed: ${err.status}`);
  } else {
    setGlobalError('An unexpected error occurred.');
    console.error('Unhandled error:', err);
  }
}
```

Do not catch `unknown` and immediately cast it to `Error`. Check the type first.

## Result Types

For operations where failure is a normal expected outcome (not an exception), consider a result type pattern:

```ts
type Result<T, E = Error> =
  | { ok: true; value: T }
  | { ok: false; error: E };

async function tryFetchUser(in_id: string): Promise<Result<UserDto, ApiError>> {
  try {
    const user = await fetchUser(in_id);
    return { ok: true, value: user };
  } catch (err) {
    if (err instanceof ApiError) return { ok: false, error: err };
    throw err; // unexpected — rethrow
  }
}
```

This is especially useful in hooks and services where the caller should handle both outcomes without try/catch at the call site.

## Runtime Validation

Use type guard functions to validate data at runtime boundaries. Do not use `as` to cast unvalidated data into typed shapes.

```ts
function isUserDto(in_value: unknown): in_value is UserDto {
  return (
    typeof in_value === 'object' &&
    in_value !== null &&
    typeof (in_value as Record<string, unknown>).id === 'string' &&
    typeof (in_value as Record<string, unknown>).email === 'string'
  );
}

function parseUserDto(in_raw: unknown): UserDto {
  if (!isUserDto(in_raw)) {
    throw new ValidationError({ _: ['Unexpected API response shape'] });
  }
  return in_raw;
}
```

For complex schemas, a validation library (Zod, Yup) reduces boilerplate and produces better error messages than hand-written guards. If the project uses one, use it consistently at all boundaries.

## Form Validation

- Validate forms client-side for UX, but never trust client-side validation alone. The ASP.NET backend is the source of truth.
- Display server-side validation errors returned from the API alongside the relevant fields. Map problem details to field-level errors.
- Do not clear server-side errors until the user edits the relevant field.

## Error Boundaries in React

Use React error boundaries to catch rendering errors and prevent the whole application from crashing.

- Wrap major sections (routes, heavy UI areas) in an error boundary.
- Display a recovery UI (reload, try again) rather than a white screen.
- Log caught errors to an error tracking service.

```tsx
// Minimal error boundary
class ErrorBoundary extends Component<
  { fallback: ReactNode; children: ReactNode },
  { hasError: boolean }
> {
  state = { hasError: false };

  static getDerivedStateFromError() { return { hasError: true }; }

  componentDidCatch(in_error: Error, in_info: ErrorInfo) {
    console.error('Rendering error caught:', in_error, in_info);
  }

  render() {
    return this.state.hasError ? this.props.fallback : this.props.children;
  }
}
```

## User-Facing Error Messages

- Never expose raw error objects, stack traces, or internal server messages to users.
- Translate status codes into human-readable messages: `401` → "Please sign in again", `403` → "You don't have permission to do this", `503` → "The service is temporarily unavailable".
- Give the user an action: retry, go back, contact support.

## Practical Heuristics

- If a function can fail in a way the caller needs to handle, model it with a result type or a typed thrown error.
- If data came from outside the application, validate it before using it.
- If you are using `JSON.parse` on user or network data, wrap it in a try/catch and validate the result.
- If a `catch` block does nothing, it is hiding a problem. Log or rethrow.

## Smells

- `catch (err: any)` — narrows nothing and may suppress real type errors
- API responses cast directly with `as SomeType` without shape validation
- Empty or comment-only catch blocks: `catch (err) { /* ignore */ }`
- Error messages that expose server internals or stack traces to users
- Validation logic duplicated in multiple components instead of centralized in a validation function or schema

## Goal

A robust error handling layer that validates data at every external boundary, expresses failure states explicitly in types, and surfaces errors to users in a way that is helpful rather than alarming.
