---
name: state-data-flow
version: 1.0
---

# State and Data Flow

## Use This Reference When

- Deciding where state should live in a component tree
- Reasoning about local, derived, shared, or server state
- Avoiding tangled data flows or excessive prop drilling
- Introducing or reviewing context, view models, or state slices
- Refactoring a component that has grown too stateful

## Veteran Expert Stance

Most state complexity in React applications is self-inflicted. State that is stored twice, state that could be derived but is not, and state that is lifted higher than necessary — these are the root causes of the majority of frontend bugs.

Before adding a `useState`, ask whether the value can be derived from existing state or props. Before lifting state, ask whether the child that owns it genuinely needs to share it. Before introducing a global store, ask whether context is enough. Every piece of state you do not add is a piece of state you do not have to keep in sync.

## State Categories

### Local State

`useState` is sufficient when:
- Only one component reads or writes the value
- The value is purely UI-local (open/closed, active tab, input draft)
- Nothing outside the component needs to react to the value

```tsx
const [isOpen, setIsOpen] = useState(false);
```

### Derived State

Do not store what can be computed.

```tsx
// Bad — redundant state
const [items, setItems] = useState<Item[]>([]);
const [count, setCount] = useState(0); // redundant

// Good — derived
const [items, setItems] = useState<Item[]>([]);
const count = items.length; // computed
```

Use `useMemo` only when the derivation is expensive (large transforms, deep filtering). Do not memoize simple derivations.

### Lifted State

Lift state to the nearest common ancestor — no higher. State that is lifted too high causes unnecessary re-renders across the tree.

- If two siblings need the same value, lift to their parent.
- If three or more distant components need the same value, evaluate context before continuing to lift.

### Server State

Server state (data from API calls) has different characteristics to local UI state: it is asynchronous, potentially stale, and shared across the application. Do not model it with `useState`.

- Use a data-fetching hook pattern (`useQuery`, SWR, or a custom hook that manages `data`, `isLoading`, `error`).
- Do not duplicate server state in local state to make it editable. Work with the API response directly, or hold a draft in local state separately.
- Invalidate and refetch rather than mutating cached data directly.

```tsx
export interface UseUserResult {
  user: UserDto | null;
  isLoading: boolean;
  error: ApiError | null;
  refetch: () => void;
}

export function useUser(in_userId: string): UseUserResult {
  const [user, setUser] = useState<UserDto | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<ApiError | null>(null);

  const refetch = useCallback(() => {
    setIsLoading(true);
    fetchUser(in_userId)
      .then(setUser)
      .catch(setError)
      .finally(() => setIsLoading(false));
  }, [in_userId]);

  useEffect(() => { refetch(); }, [refetch]);

  return { user, isLoading, error, refetch };
}
```

### Shared State via Context

Use React context when multiple components at different levels of the tree need the same value and prop drilling is impractical.

- Keep context values small and focused. Prefer one context per domain (auth, theme, notifications) over a single global context.
- Memoize context values to prevent unnecessary re-renders.
- Do not put high-frequency-update state (e.g., mouse position) in context — every consumer re-renders on change.

```tsx
interface AuthContextValue {
  readonly user: UserDto | null;
  readonly isAuthenticated: boolean;
  readonly logout: () => void;
}

const AuthContext = createContext<AuthContextValue | null>(null);

export function useAuth(): AuthContextValue {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error('useAuth must be used within AuthProvider');
  return ctx;
}
```

## Data Flow Rules

- Data flows down through props. Events flow up through callbacks.
- Do not pass setter functions (`setX`) into deeply nested components. Pass a typed callback instead.
- Do not mutate objects or arrays stored in state directly. Always produce a new reference.

```tsx
// Bad — direct mutation
state.items.push(newItem);
setState(state);

// Good — new reference
setState((prev) => ({ ...prev, items: [...prev.items, newItem] }));
```

## View Models

For complex forms or screens, extract a view model: a hook that owns all the state and derived values for that screen and exposes only what the component needs.

```tsx
export function useOrderForm(): UseOrderFormResult {
  const [items, setItems] = useState<OrderItem[]>([]);
  const total = items.reduce((sum, item) => sum + item.price * item.quantity, 0);
  // ... handlers, validation, submission
  return { items, total, ... };
}
```

## Practical Heuristics

- If a component has more than 5-6 `useState` calls, extract a view model hook.
- If state is passed through more than two intermediary components without being used, introduce context or restructure.
- If you are setting state in a `useEffect` in response to other state, check whether derivation or a different hook structure eliminates the need.
- If two pieces of state always change together, combine them into one object.

## Smells

- Storing derived values in state (`count` alongside `items[]`, `fullName` alongside `firstName`/`lastName`)
- `useEffect` that watches state changes and sets other state — this is a derivation expressed incorrectly
- Setter functions (`setUser`, `setItems`) passed as props through multiple component levels
- Server data stored in `useState` alongside UI state, making it hard to distinguish what is cached vs. what is local
- Context that holds every piece of application state — use multiple focused contexts

## Goal

A data flow where every piece of state has a clear, minimal owner, derived values are computed rather than stored, server state is managed as async data, and components re-render only when the data they actually depend on changes.
