---
name: build-tooling-config
metadata:
  version: "1.1"
---

# Build, Tooling, and Configuration

## Use This Reference When

- Configuring or troubleshooting `tsconfig.json`
- Configuring Vite: plugins, aliases, environment variables, build output
- Setting up or tuning ESLint or Prettier
- Managing path aliases between TypeScript and Vite
- Diagnosing a build failure, type error caused by config, or module resolution problem

## Veteran Expert Stance

Build and tooling configuration is infrastructure. Getting it right once makes every engineer's daily workflow faster and every CI run more reliable. Getting it wrong silently — permissive TypeScript settings, misaligned path aliases, inconsistent formatting rules — creates problems that compound over time.

Keep configuration minimal and explicit. Do not copy-paste configs without understanding what each option does. Align TypeScript and Vite configs so they both resolve modules the same way.

## TypeScript Configuration

### Recommended tsconfig.json Base

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "lib": ["ES2022", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "moduleResolution": "bundler",
    "jsx": "react-jsx",
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "skipLibCheck": true,
    "esModuleInterop": true,
    "resolveJsonModule": true,
    "baseUrl": ".",
    "paths": {
      "@features/*": ["src/features/*"],
      "@shared/*": ["src/shared/*"],
      "@api/*": ["src/api/*"]
    }
  },
  "include": ["src"],
  "exclude": ["node_modules", "dist"]
}
```

### Key Options

- `"strict": true` — enables all strict checks. Never disable.
- `"noUncheckedIndexedAccess": true` — array index access returns `T | undefined`, not `T`. Prevents off-by-one and empty-array bugs.
- `"moduleResolution": "bundler"` — correct resolution strategy for Vite projects.
- `"jsx": "react-jsx"` — enables the automatic JSX runtime; no need to import React in every component file.
- `"skipLibCheck": true` — skips type checking of `.d.ts` files in `node_modules`. Acceptable for application code; keeps build fast.

### Common tsconfig Mistakes

- Using `"moduleResolution": "node"` with Vite — misaligns with how Vite resolves modules
- Using `"noEmit": false` in a Vite project — Vite handles emit; TypeScript is for type checking only
- Disabling `strict` or individual strict flags to silence errors — fix the type instead

## Vite Configuration

### Standard vite.config.ts

```ts
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
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'https://localhost:5001',
        changeOrigin: true,
        secure: false,
      },
    },
  },
  build: {
    sourcemap: true,
    outDir: 'dist',
  },
});
```

### Path Aliases

Path aliases must be defined in both `tsconfig.json` (TypeScript) and `vite.config.ts` (Vite). If either is missing, imports work in one tool but not the other.

### Proxy for ASP.NET Backend

The `server.proxy` config routes `/api/*` requests to the ASP.NET dev server. This eliminates CORS issues during development and mirrors the production deployment pattern where both frontends and API are served from the same domain or proxied by a reverse proxy.

### Environment Variables

- Vite exposes environment variables prefixed with `VITE_` to client code via `import.meta.env`.
- Provide a `.env.example` file documenting all required variables. Do not commit `.env` or `.env.local`.
- Access env vars through a typed wrapper rather than scattering `import.meta.env.VITE_*` throughout the codebase.

```ts
// shared/config.ts
export const config = {
  apiBaseUrl: import.meta.env.VITE_API_BASE_URL as string,
  appVersion: import.meta.env.VITE_APP_VERSION as string,
} as const;
```

## ESLint

### Minimum Rule Set for React + TypeScript

```json
{
  "extends": [
    "eslint:recommended",
    "plugin:@typescript-eslint/recommended-type-checked",
    "plugin:react-hooks/recommended",
    "plugin:jsx-a11y/recommended"
  ],
  "parser": "@typescript-eslint/parser",
  "parserOptions": {
    "project": "./tsconfig.json"
  },
  "rules": {
    "@typescript-eslint/no-explicit-any": "error",
    "@typescript-eslint/no-non-null-assertion": "warn",
    "@typescript-eslint/consistent-type-imports": "error",
    "react-hooks/exhaustive-deps": "error",
    "no-console": ["warn", { "allow": ["error", "warn"] }]
  }
}
```

- `@typescript-eslint/recommended-type-checked` provides richer checks that use the TypeScript type checker.
- `react-hooks/exhaustive-deps` as `error` (not `warn`) — missing deps cause real bugs.
- `jsx-a11y` catches common accessibility issues at lint time.

## Prettier

Prettier eliminates formatting debates. Configure once and commit the config.

```json
{
  "semi": true,
  "singleQuote": true,
  "trailingComma": "all",
  "printWidth": 100,
  "tabWidth": 2,
  "arrowParens": "always"
}
```

Integrate Prettier with ESLint via `eslint-config-prettier` to prevent rule conflicts.

## Package Scripts

Define consistent npm scripts in `package.json`:

```json
{
  "scripts": {
    "dev": "vite",
    "build": "tsc --noEmit && vite build",
    "preview": "vite preview",
    "test": "vitest run",
    "test:watch": "vitest",
    "lint": "eslint src --ext .ts,.tsx",
    "format": "prettier --write src",
    "typecheck": "tsc --noEmit"
  }
}
```

- `build` runs TypeScript type checking before Vite builds. This catches type errors that Vite would silently ignore.
- `typecheck` is a standalone step for CI or pre-commit hooks.

## Practical Heuristics

- If type errors appear in IDE but not in build, check that both use the same `tsconfig`.
- If path aliases resolve in IDE but not in tests, Vitest needs the same aliases configured via `vitest.config.ts`.
- If a library type is causing spurious errors, check if the `@types/*` package is installed and at a compatible version.
- Keep `devDependencies` and `dependencies` clearly separated. Tooling belongs in `devDependencies`.

## Smells

- A `tsconfig` that disables strict checks across the board to make the project compile
- Path aliases defined in only one config (TypeScript or Vite) but not both
- Environment variables accessed directly from `import.meta.env` scattered throughout the codebase
- ESLint `no-explicit-any` set to `warn` instead of `error`
- No type checking step in the CI/CD pipeline — Vite builds successfully even with type errors

## Goal

A well-configured build pipeline where TypeScript strictness is non-negotiable, tooling is consistent across local development and CI, and every engineer's environment produces the same results.
