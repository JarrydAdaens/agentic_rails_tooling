---
name: api-integration-dotnet
version: 1.0
agentic_rails_source_version: 1.0
---

# API Integration With .NET Backends

## Use This Reference When

- Calling an ASP.NET API from TypeScript or React
- Designing or reviewing a fetch client, API service, or HTTP abstraction
- Typing API request and response shapes (DTOs)
- Handling auth headers, cookies, or tokens in frontend API calls
- Keeping the frontend/backend contract clean and avoiding drift

## Veteran Expert Stance

The boundary between a TypeScript frontend and an ASP.NET backend is one of the highest-risk points in the application. Both sides must agree on request shapes, response shapes, error formats, and authentication expectations. When that boundary is informal — typed loosely on the frontend, assumed on the backend — bugs hide there.

Treat every API boundary as a contract. Type both sides explicitly. Validate incoming data at the boundary before using it anywhere else in the frontend. Keep API calls out of components and behind a service or hook abstraction.

## DTO Typing

Define TypeScript interfaces that mirror your ASP.NET response and request types. Keep them in an `api/` folder or co-located with the relevant feature.

- Name DTOs to reflect the API surface, not the component that consumes them: `UserDto`, `CreateOrderRequest`, `PaginatedResponse<T>`.
- Use `readonly` fields on response DTOs — you should not mutate data you received from the server.
- Keep request types separate from response types. They often differ and evolve independently.

```ts
// api/types/user.ts
export interface UserDto {
  readonly id: string;
  readonly email: string;
  readonly displayName: string;
  readonly createdAt: string; // ISO date string from the API
}

export interface CreateUserRequest {
  email: string;
  displayName: string;
  password: string;
}
```

## Fetch Client

Centralize your HTTP logic in a base client. This is where you set base URLs, attach auth headers, and enforce consistent error handling.

- Do not scatter raw `fetch` calls across components and hooks.
- Do not use `any` for response types in fetch wrappers.
- Return typed results from the client, not raw `Response` objects.

```ts
// api/client.ts
const BASE_URL = import.meta.env.VITE_API_BASE_URL;

async function request<TResponse>(
  in_path: string,
  in_options: RequestInit = {}
): Promise<TResponse> {
  const token = getAuthToken();
  const response = await fetch(`${BASE_URL}/${in_path}`, {
    ...in_options,
    headers: {
      'Content-Type': 'application/json',
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...in_options.headers,
    },
  });

  if (!response.ok) {
    throw new ApiError(response.status, await response.text());
  }

  return response.json() as Promise<TResponse>;
}

export const api = {
  get: <T>(in_path: string) => request<T>(in_path),
  post: <T>(in_path: string, in_body: unknown) =>
    request<T>(in_path, { method: 'POST', body: JSON.stringify(in_body) }),
  put: <T>(in_path: string, in_body: unknown) =>
    request<T>(in_path, { method: 'PUT', body: JSON.stringify(in_body) }),
  delete: <T>(in_path: string) => request<T>(in_path, { method: 'DELETE' }),
};
```

## API Service Modules

Group related API calls into typed service modules. These live in `api/endpoints/` or `features/<name>/services/`.

```ts
// api/endpoints/users.ts
import { api } from '../client';
import type { UserDto, CreateUserRequest } from '../types/user';

export async function fetchUser(in_userId: string): Promise<UserDto> {
  return api.get<UserDto>(`users/${in_userId}`);
}

export async function createUser(in_request: CreateUserRequest): Promise<UserDto> {
  return api.post<UserDto>('users', in_request);
}
```

## Authentication

- Store access tokens in memory (a module-level variable or a token store) rather than `localStorage` when security is a priority.
- Use `httpOnly` cookies for the highest-security scenarios; coordinate with the ASP.NET backend to set them appropriately.
- Refresh tokens silently before expiry when using JWT. Expose a token refresh hook that the fetch client can call.
- Do not hard-code auth endpoints or token keys in multiple places. Centralize them.

## Error Responses

ASP.NET problem details format (`application/problem+json`) is a common error shape. Type it:

```ts
export interface ProblemDetails {
  type?: string;
  title: string;
  status: number;
  detail?: string;
  traceId?: string;
}

export class ApiError extends Error {
  constructor(
    public readonly status: number,
    public readonly body: string
  ) {
    super(`API error ${status}`);
  }
}
```

See `error-handling-validation.md` for how to handle these errors at the call site.

## Date and Time

- ASP.NET returns ISO 8601 date strings. Store them as strings in DTOs.
- Parse to `Date` objects or a date library type only at the point of display or computation, not in the DTO.
- Never mutate a date string received from the API.

## Pagination

Define a generic pagination wrapper for paginated endpoints:

```ts
export interface PaginatedResponse<TItem> {
  readonly items: readonly TItem[];
  readonly totalCount: number;
  readonly pageNumber: number;
  readonly pageSize: number;
}
```

## Practical Heuristics

- If a component is importing from `api/` directly, move the call into a custom hook.
- If two features call the same endpoint, the endpoint function belongs in `api/endpoints/`, not in a feature folder.
- If the response type is `any`, the DTO has not been written yet — write it before proceeding.
- Keep API service functions pure: input parameters, async result or error. No side effects, no direct state mutation.

## Smells

- Raw `fetch` calls inside React components or hooks without a service abstraction
- Response typed as `any` or cast directly with `as SomeType` without validation
- Auth token handling duplicated in multiple files
- Hardcoded base URLs not controlled by environment variables
- Mixed concerns: a service function that calls the API and also dispatches to a state store

## Goal

A clean, typed, and centralized API layer where every call to the ASP.NET backend is explicit about its request shape, response shape, and error contract — and where components and hooks are insulated from HTTP mechanics.
