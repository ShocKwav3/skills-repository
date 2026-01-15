---
name: typescript-standards
description: |
  TypeScript coding standards, patterns, and best practices for writing type-safe, maintainable code. Use when: (1) Writing TypeScript code - types, interfaces, generics, (2) Refactoring JavaScript to TypeScript, (3) Implementing type-safe patterns, (4) Working with advanced types (conditional, mapped, template literals), (5) Setting up TypeScript conventions for a project, (6) Using modern ES6+ features with proper typing, (7) Implementing async/await patterns, (8) Building type-safe APIs or libraries.
---

# TypeScript Standards

Comprehensive TypeScript coding standards covering conventions, patterns, advanced types, and modern JavaScript/TypeScript patterns for building maintainable, type-safe applications.

## Quick Reference

### Essential Patterns

**Const Types Pattern (REQUIRED):**
```typescript
// Create const object first, then extract type
const STATUS = {
  ACTIVE: "active",
  INACTIVE: "inactive",
  PENDING: "pending",
} as const;

type Status = (typeof STATUS)[keyof typeof STATUS];
```

**Flat Interfaces (REQUIRED):**
```typescript
// Nested objects -> dedicated interface
interface UserAddress {
  street: string;
  city: string;
}

interface User {
  id: string;
  name: string;
  address: UserAddress;  // Reference, not inline
}
```

**Never Use `any`:**
```typescript
// Use unknown for truly unknown types
function parse(input: unknown): User {
  if (isUser(input)) return input;
  throw new Error("Invalid input");
}

// Use generics for flexible types
function first<T>(arr: T[]): T | undefined {
  return arr[0];
}
```

### Type Guards

```typescript
function isUser(value: unknown): value is User {
  return (
    typeof value === "object" &&
    value !== null &&
    "id" in value &&
    "name" in value
  );
}
```

### Common Utility Types

```typescript
Pick<User, "id" | "name">     // Select fields
Omit<User, "id">              // Exclude fields
Partial<User>                 // All optional
Required<User>                // All required
Readonly<User>                // All readonly
Record<string, User>          // Object type
NonNullable<T | null>         // Remove null/undefined
ReturnType<typeof fn>         // Function return type
```

### Import Patterns

```typescript
import type { User } from "./types";
import { createUser, type Config } from "./utils";
```

## Conventions Summary

- **File Naming**: Use kebab-case (`user-service.ts`, `api-client.ts`)
- **Named Imports**: Prefer over namespace imports
- **Always Await**: Never fire-and-forget promises
- **Braces Required**: All control statements need braces
- **HTTP Verb Prefixes**: `PostUserRequest`, `GetUserParams`, `PatchUserRequest`

## References

This skill includes detailed reference files for specific topics. Read these when you need deeper guidance:

### [typescript-conventions.md](references/typescript-conventions.md)
**Read when:** Setting up project conventions, handling imports/exports, file naming, error handling patterns, or following style guidelines. Covers ESLint/Prettier config, naming conventions, type safety basics, and Promise handling.

### [typescript-patterns.md](references/typescript-patterns.md)
**Read when:** Implementing the const types pattern, flat interfaces pattern, or when you need a quick reference for utility types and type guards. Contains the core required patterns for TypeScript development.

### [typescript-advanced-types.md](references/typescript-advanced-types.md)
**Read when:** Working with generics, conditional types, mapped types, template literal types, or building type-safe libraries. Covers advanced patterns like type-safe event emitters, API clients, builder patterns, and deep readonly/partial types.

### [modern-typescript-patterns.md](references/modern-typescript-patterns.md)
**Read when:** Using ES6+ features with TypeScript, implementing async/await patterns, functional programming (map/filter/reduce), composition/piping, or performance optimization (debounce/throttle). Covers arrow functions, destructuring, spread/rest operators, iterators/generators, and modern operators.

## Best Practices

1. **Use `unknown` over `any`**: Enforce type checking
2. **Prefer `interface` for object shapes**: Better error messages
3. **Use `type` for unions and complex types**: More flexible
4. **Leverage type inference**: Let TypeScript infer when possible
5. **Use const assertions**: Preserve literal types with `as const`
6. **Avoid type assertions**: Use type guards instead
7. **Enable strict mode**: Use all strict compiler options
8. **Prefer immutability**: Use spread operators over mutation

## Common Pitfalls

- **Anemic types with `any`**: Defeats TypeScript's purpose
- **Inline nested objects**: Makes interfaces hard to reuse
- **Fire-and-forget promises**: Exceptions get lost
- **Missing braces**: Single-line control statements without braces
- **Ignoring strict null checks**: Can lead to runtime errors
- **Over-complex types**: Can slow down compilation
