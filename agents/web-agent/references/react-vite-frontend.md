---
name: react-vite-frontend
version: 1.0
---

# React and Vite Frontend Development

## Use This Reference When

- Building or modifying React components
- Writing or composing custom hooks
- Structuring JSX, handling events, or typing props
- Setting up or adjusting Vite project conventions and folder layout
- Deciding where logic belongs: component, hook, or service

## Veteran Expert Stance

A well-written React codebase is a collection of small, single-concern components wired together through explicit data flow. The components describe what the UI looks like given some data; hooks contain the logic to obtain and manage that data; services contain the logic to interact with the outside world.

When a component becomes hard to read or test, the answer is almost always the same: extract logic into a hook, extract JSX into a sub-component, or move data fetching into a service. Complexity does not disappear — it should be moved to where it is easiest to test and understand.

## Component Design

- One component per file. Filename and exported name must match in `PascalCase`.
- Keep components focused on rendering. A component that decides, fetches, validates, and renders is four concerns in one.
- Write the component's props interface first. It defines what the component depends on and what it communicates back.
- A component's return should be declarative and easy to read. If the JSX block requires significant mental parsing, extract sub-components.

```tsx
interface ProductCardProps {
  readonly title: string;
  readonly price: number;
  readonly isAvailable: boolean;
  readonly onAddToCart: () => void;
}

export function ProductCard({ title, price, isAvailable, onAddToCart }: ProductCardProps) {
  return (
    <div className="product-card">
      <h3 className="product-card__title">{title}</h3>
      <span className="product-card__price">${price.toFixed(2)}</span>
      <button
        className="btn btn--primary"
        disabled={!isAvailable}
        onClick={onAddToCart}
      >
        {isAvailable ? 'Add to cart' : 'Out of stock'}
      </button>
    </div>
  );
}
```

## Hooks

- Prefix all hooks with `use`. Place custom hooks in their own files.
- Hooks are the correct home for: data fetching, derived state, subscriptions, and reusable event logic.
- Return a named object from hooks that return more than two values. Tuples are acceptable for two-value returns.
- Declare `useEffect` dependencies accurately. Do not ignore the exhaustive-deps lint rule without a documented reason.
- Use `useCallback` to stabilize function references passed to child components or included in dependency arrays. Do not use it everywhere by default.
- Use `useMemo` to memoize expensive derivations. Do not use it to memoize every value by default.

```tsx
export interface UseToggleResult {
  isOn: boolean;
  toggle: () => void;
  setOn: () => void;
  setOff: () => void;
}

export function useToggle(in_initial = false): UseToggleResult {
  const [isOn, setIsOn] = useState(in_initial);
  const toggle = useCallback(() => setIsOn((v) => !v), []);
  const setOn = useCallback(() => setIsOn(true), []);
  const setOff = useCallback(() => setIsOn(false), []);
  return { isOn, toggle, setOn, setOff };
}
```

## JSX Conventions

- No inline styles. Use CSS modules, utility classes, or a design system class pattern.
- No anonymous function definitions inline in JSX for non-trivial handlers. Extract them as named variables above the return statement.
- Use self-closing tags for elements with no children.
- Use fragments (`<>...</>`) instead of wrapper `div` elements where no container is semantically needed.
- Prefer ternary for simple conditional rendering. Extract complex conditions to a named variable or dedicated component.

```tsx
// Handler extracted, not inline
function UserRow({ user, onSelect }: UserRowProps) {
  const handleClick = () => onSelect(user.id);
  return <tr onClick={handleClick}>{/* ... */}</tr>;
}
```

## Event Handling

- Type event handlers explicitly: `React.ChangeEvent<HTMLInputElement>`, `React.FormEvent<HTMLFormElement>`.
- Extract the relevant value from the event immediately; do not store the event object.
- Use `onSubmit` with `event.preventDefault()` for forms. Do not use button clicks for form submission.

## Controlled vs Uncontrolled Inputs

- Prefer controlled inputs. Always provide `value` and `onChange` together.
- Use `useRef` for uncontrolled inputs only when you need imperative access (focus, measurements) and not for reading values on change.

## Vite Conventions

- Use Vite's HMR (Hot Module Replacement) by default. Avoid patterns that break it (mutating module-level state, side effects at the module root).
- Configure path aliases in both `vite.config.ts` and `tsconfig.json` so they stay in sync.
- Place static assets in `public/` for files referenced directly by URL, and in `src/assets/` for files imported by the module graph.
- Use `import.meta.env` for environment variables. Prefix custom env vars with `VITE_` to expose them to the client.

```ts
// vite.config.ts — alias example
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@features': path.resolve(__dirname, 'src/features'),
      '@shared': path.resolve(__dirname, 'src/shared'),
      '@api': path.resolve(__dirname, 'src/api'),
    },
  },
});
```

## Practical Heuristics

- If a component needs data from a remote source, put the fetching logic in a custom hook.
- If a hook is doing UI rendering, it is probably a component.
- If two components share logic, extract it to a custom hook or utility.
- If a prop is passed through a component without being used, there is likely a missing context or structural issue.
- Render nothing rather than rendering broken content. Guard against empty/loading states early in the component.

## Smells

- Components that contain `fetch`, `axios`, or service calls directly in the body or `useEffect` without a hook abstraction
- Props with names like `data`, `info`, or `obj` — the props interface is the documentation
- A component with 10+ props that are all optional — likely doing too much or missing a composition pattern
- JSX with deeply nested conditionals and early returns — extract sub-components
- Re-renders caused by referentially unstable objects or functions created inline in JSX
- A single large `useEffect` that manages multiple concerns

## Goal

Build a React frontend that is composed of small, single-concern components wired through clear data flow, where logic lives in hooks, rendering lives in components, and the division of responsibility is easy for any engineer to follow.
