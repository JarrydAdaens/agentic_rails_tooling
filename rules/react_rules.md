# React Coding Rules

## Scope

Applies to all React components, custom hooks, and JSX in `.tsx` files in this workspace.

Intent: readable, focused React code using function components, hooks, and clear data flow — consistent with the TypeScript rules and this project's ASP.NET-backed stack.

## Components

- Use function components exclusively. Do not write class components.
- One component per file. The filename and the component name must match in `PascalCase`.
- Keep components focused on one concern. If a component handles layout, data fetching, and form logic simultaneously, split it.
- Keep JSX readable. If the return block exceeds roughly 50 lines, the component is likely doing too much.
- Use `React.FC` only when the props interface is already defined separately and the typing benefit is clear. Prefer explicit props parameters with a named interface in most cases.

## Props

- Define an explicit named interface for every component's props. Name it after the component: `ButtonProps`, `UserCardProps`.
- Do not use inline object type literals for props in the function signature.
- Use `readonly` on props interface fields. Props should not be mutated.
- Do not spread unknown or untyped prop objects onto DOM elements without filtering.

```tsx
// Correct
interface AvatarProps {
  readonly src: string;
  readonly alt: string;
  readonly size?: 'sm' | 'md' | 'lg';
}

export function Avatar({ src, alt, size = 'md' }: AvatarProps) {
  return <img className={`avatar avatar--${size}`} src={src} alt={alt} />;
}
```

## Hooks

- Prefix all custom hooks with `use`: `useUserData`, `useFormState`.
- Place custom hooks in their own files, not inside component files.
- Follow the rules of hooks: call only at the top level, never inside conditions, loops, or nested functions.
- Declare dependencies in `useEffect`, `useMemo`, and `useCallback` accurately. Do not suppress exhaustive-deps warnings without a comment explaining why.
- Do not put side effects directly in the component body. Wrap them in `useEffect`.
- Prefer returning a single typed object from custom hooks rather than a tuple when more than two values are returned.

## JSX

- Do not use inline styles. Use CSS modules, a utility class library, or a design-system class pattern.
- Do not use magic strings in `className`. Use named constants or CSS module imports.
- Do not define non-trivial functions inline inside JSX. Extract them as named handlers above the return statement.
- Self-close elements with no children: `<Spinner />` not `<Spinner></Spinner>`.
- Use fragments (`<>...</>`) to avoid unnecessary wrapper `div` elements.
- Prefer conditional rendering with short-circuit (`&&`) or ternary for simple cases. Extract to a named variable or helper component for complex conditions.

## State

- Keep state minimal. Do not store values that can be derived from existing state or props.
- Lift state only as far as needed to be shared.
- Do not use `useState` for server data. Use a data-fetching hook or library pattern that handles loading, error, and data states.
- Prefer controlled inputs (value + onChange) over uncontrolled refs for form fields.
- Do not use a single large state object when individual `useState` calls are clearer. Combine only when the fields change together.

## Data Flow

- Pass data down through props. Raise events up through callbacks.
- Do not access or mutate parent state from child components directly.
- Do not prop-drill past two or three component levels. Introduce context or restructure the component tree.
- Keep data transformations out of the render path. Compute or memoize them before the return statement.

## Do Not

- Do not write class components.
- Do not prop-drill past two levels without context.
- Do not put API calls, service calls, or complex business logic inside a component body. Move them to a custom hook or service module.
- Do not render large lists without considering virtualization.
- Do not suppress React warnings and ESLint rules without understanding and documenting the reason.
- Do not import from `react` for JSX in projects using the automatic JSX runtime. Only import named hooks and APIs you use.

## Examples

```tsx
// Custom hook — separate file, named exports, typed return
export interface UseCounterResult {
  count: number;
  increment: () => void;
  reset: () => void;
}

export function useCounter(in_initial = 0): UseCounterResult {
  const [count, setCount] = useState(in_initial);
  const increment = useCallback(() => setCount((c) => c + 1), []);
  const reset = useCallback(() => setCount(in_initial), [in_initial]);
  return { count, increment, reset };
}
```

```tsx
// Component — named interface, no inline styles, no inline handlers
interface SaveButtonProps {
  readonly isLoading: boolean;
  readonly onSave: () => void;
}

export function SaveButton({ isLoading, onSave }: SaveButtonProps) {
  const label = isLoading ? 'Saving...' : 'Save';

  return (
    <button className="btn btn--primary" disabled={isLoading} onClick={onSave}>
      {label}
    </button>
  );
}
```
