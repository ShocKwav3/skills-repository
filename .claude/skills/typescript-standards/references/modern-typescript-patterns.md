# Modern TypeScript Patterns

Comprehensive guide for mastering modern TypeScript (ES6+) features, functional programming patterns, and best practices for writing clean, maintainable, and performant code.

## Table of Contents

1. [ES6+ Core Features](#es6-core-features)
2. [Asynchronous Patterns](#asynchronous-patterns)
3. [Functional Programming Patterns](#functional-programming-patterns)
4. [Modern Class Features](#modern-class-features)
5. [Modules](#modules-es6)
6. [Iterators and Generators](#iterators-and-generators)
7. [Modern Operators](#modern-operators)
8. [Performance Optimization](#performance-optimization)
9. [Best Practices](#best-practices)

## ES6+ Core Features

### 1. Arrow Functions

**Syntax and Use Cases:**
```typescript
// Traditional function
function add(a: number, b: number): number {
  return a + b;
}

// Arrow function
const add = (a: number, b: number): number => a + b;

// Single parameter (parentheses optional)
const double = (x: number): number => x * 2;

// No parameters
const getRandom = (): number => Math.random();

// Multiple statements (need curly braces)
interface User {
  name: string;
}

const processUser = (user: User): User => {
  const normalized = user.name.toLowerCase();
  return { ...user, name: normalized };
};

// Returning objects (wrap in parentheses)
const createUser = (name: string, age: number): { name: string; age: number } => ({ name, age });
```

**Lexical 'this' Binding:**
```typescript
class Counter {
  count: number = 0;

  // Arrow function preserves 'this' context
  increment = (): void => {
    this.count++;
  };

  // Traditional function loses 'this' in callbacks
  incrementTraditional(): void {
    setTimeout(function(this: Counter) {
      this.count++;  // 'this' is undefined
    }, 1000);
  }

  // Arrow function maintains 'this'
  incrementArrow(): void {
    setTimeout(() => {
      this.count++;  // 'this' refers to Counter instance
    }, 1000);
  }
}
```

### 2. Destructuring

**Object Destructuring:**
```typescript
interface Address {
  city: string;
  country: string;
}

interface User {
  id: number;
  name: string;
  email: string;
  age?: number;
  address: Address;
}

const user: User = {
  id: 1,
  name: 'John Doe',
  email: 'john@example.com',
  address: {
    city: 'New York',
    country: 'USA'
  }
};

// Basic destructuring
const { name, email } = user;

// Rename variables
const { name: userName, email: userEmail } = user;

// Default values
const { age = 25 } = user;

// Nested destructuring
const { address: { city, country } } = user;

// Rest operator
const { id, ...userWithoutId } = user;

// Function parameters
function greet({ name, age = 18 }: { name: string; age?: number }): void {
  console.log(`Hello ${name}, you are ${age}`);
}
greet(user);
```

**Array Destructuring:**
```typescript
const numbers: number[] = [1, 2, 3, 4, 5];

// Basic destructuring
const [first, second] = numbers;

// Skip elements
const [, , third] = numbers;

// Rest operator
const [head, ...tail] = numbers;

// Swapping variables
let a = 1, b = 2;
[a, b] = [b, a];

// Function return values
function getCoordinates(): [number, number] {
  return [10, 20];
}
const [x, y] = getCoordinates();

// Default values
const [one, two, three = 0] = [1, 2];
```

### 3. Spread and Rest Operators

**Spread Operator:**
```typescript
// Array spreading
const arr1: number[] = [1, 2, 3];
const arr2: number[] = [4, 5, 6];
const combined: number[] = [...arr1, ...arr2];

// Object spreading
interface Settings {
  theme: string;
  lang: string;
}

const defaults: Settings = { theme: 'dark', lang: 'en' };
const userPrefs: Partial<Settings> = { theme: 'light' };
const settings: Settings = { ...defaults, ...userPrefs };

// Function arguments
const numbers: number[] = [1, 2, 3];
Math.max(...numbers);

// Copying arrays/objects (shallow copy)
const copy = [...arr1];
const objCopy = { ...user };

// Adding items immutably
const newArr = [...arr1, 4, 5];
const newObj = { ...user, age: 30 };
```

**Rest Parameters:**
```typescript
// Collect function arguments
function sum(...numbers: number[]): number {
  return numbers.reduce((total, num) => total + num, 0);
}
sum(1, 2, 3, 4, 5);

// With regular parameters
function greet(greeting: string, ...names: string[]): string {
  return `${greeting} ${names.join(', ')}`;
}
greet('Hello', 'John', 'Jane', 'Bob');

// Object rest
const { id, ...userData } = user;

// Array rest
const [first, ...rest] = [1, 2, 3, 4, 5];
```

### 4. Template Literals

```typescript
// Basic usage
const name = 'John';
const greeting = `Hello, ${name}!`;

// Multi-line strings
const title = 'Welcome';
const content = 'This is the content';
const html = `
  <div>
    <h1>${title}</h1>
    <p>${content}</p>
  </div>
`;

// Expression evaluation
const price = 19.99;
const total = `Total: $${(price * 1.2).toFixed(2)}`;

// Tagged template literals
function highlight(strings: TemplateStringsArray, ...values: unknown[]): string {
  return strings.reduce((result, str, i) => {
    const value = values[i] ?? '';
    return result + str + `<mark>${value}</mark>`;
  }, '');
}

const userName = 'John';
const userAge = 30;
const htmlOutput = highlight`Name: ${userName}, Age: ${userAge}`;
// Output: "Name: <mark>John</mark>, Age: <mark>30</mark>"
```

### 5. Enhanced Object Literals

```typescript
const name = 'John';
const age = 30;

// Shorthand property names
const user = { name, age };

// Shorthand method names
const calculator = {
  add(a: number, b: number): number {
    return a + b;
  },
  subtract(a: number, b: number): number {
    return a - b;
  }
};

// Computed property names
const field = 'email';
const dynamicUser = {
  name: 'John',
  [field]: 'john@example.com',
  [`get${field.charAt(0).toUpperCase()}${field.slice(1)}`](): string {
    return this[field];
  }
};

// Dynamic property creation
function createUser(name: string, ...props: [string, unknown][]): Record<string, unknown> {
  return props.reduce((user, [key, value]) => ({
    ...user,
    [key]: value
  }), { name });
}

const dynamicUserResult = createUser('John', ['age', 30], ['email', 'john@example.com']);
```

## Asynchronous Patterns

### 1. Promises

**Creating and Using Promises:**
```typescript
interface User {
  id: number;
  name: string;
}

// Creating a promise
const fetchUser = (id: number): Promise<User> => {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      if (id > 0) {
        resolve({ id, name: 'John' });
      } else {
        reject(new Error('Invalid ID'));
      }
    }, 1000);
  });
};

// Using promises
fetchUser(1)
  .then(user => console.log(user))
  .catch(error => console.error(error))
  .finally(() => console.log('Done'));

// Chaining promises
interface Post {
  id: number;
  title: string;
}

declare function fetchUserPosts(userId: number): Promise<Post[]>;
declare function processPosts(posts: Post[]): Promise<Post[]>;

fetchUser(1)
  .then(user => fetchUserPosts(user.id))
  .then(posts => processPosts(posts))
  .then(result => console.log(result))
  .catch(error => console.error(error));
```

**Promise Combinators:**
```typescript
// Promise.all - Wait for all promises
const promises: Promise<User>[] = [
  fetchUser(1),
  fetchUser(2),
  fetchUser(3)
];

Promise.all(promises)
  .then(users => console.log(users))
  .catch(error => console.error('At least one failed:', error));

// Promise.allSettled - Wait for all, regardless of outcome
Promise.allSettled(promises)
  .then(results => {
    results.forEach(result => {
      if (result.status === 'fulfilled') {
        console.log('Success:', result.value);
      } else {
        console.log('Error:', result.reason);
      }
    });
  });

// Promise.race - First to complete
Promise.race(promises)
  .then(winner => console.log('First:', winner))
  .catch(error => console.error(error));

// Promise.any - First to succeed
Promise.any(promises)
  .then(first => console.log('First success:', first))
  .catch(error => console.error('All failed:', error));
```

### 2. Async/Await

**Basic Usage:**
```typescript
interface User {
  id: number;
  name: string;
}

interface Post {
  id: number;
  title: string;
}

// Async function always returns a Promise
async function fetchUser(id: number): Promise<User> {
  const response = await fetch(`/api/users/${id}`);
  const user: User = await response.json();
  return user;
}

// Error handling with try/catch
async function getUserData(id: number): Promise<{ user: User; posts: Post[] } | null> {
  try {
    const user = await fetchUser(id);
    const posts = await fetchUserPosts(user.id);
    return { user, posts };
  } catch (error) {
    console.error('Error fetching data:', error);
    return null;
  }
}

// Sequential vs Parallel execution
async function sequential(): Promise<[User, User]> {
  const user1 = await fetchUser(1);  // Wait
  const user2 = await fetchUser(2);  // Then wait
  return [user1, user2];
}

async function parallel(): Promise<[User, User]> {
  const [user1, user2] = await Promise.all([
    fetchUser(1),
    fetchUser(2)
  ]);
  return [user1, user2];
}
```

**Advanced Patterns:**
```typescript
// Async IIFE
(async () => {
  const result = await someAsyncOperation();
  console.log(result);
})();

// Async iteration
async function processUsers(userIds: number[]): Promise<void> {
  for (const id of userIds) {
    const user = await fetchUser(id);
    await processUser(user);
  }
}

// Top-level await (ES2022)
const config = await fetch('/config.json').then(r => r.json());

// Retry logic
async function fetchWithRetry(url: string, retries: number = 3): Promise<Response> {
  for (let i = 0; i < retries; i++) {
    try {
      return await fetch(url);
    } catch (error) {
      if (i === retries - 1) throw error;
      await new Promise(resolve => setTimeout(resolve, 1000 * (i + 1)));
    }
  }
  throw new Error('Max retries exceeded');
}

// Timeout wrapper
async function withTimeout<T>(promise: Promise<T>, ms: number): Promise<T> {
  const timeout = new Promise<never>((_, reject) =>
    setTimeout(() => reject(new Error('Timeout')), ms)
  );
  return Promise.race([promise, timeout]);
}
```

## Functional Programming Patterns

### 1. Array Methods

**Map, Filter, Reduce:**
```typescript
interface User {
  id: number;
  name: string;
  age: number;
  active: boolean;
}

const users: User[] = [
  { id: 1, name: 'John', age: 30, active: true },
  { id: 2, name: 'Jane', age: 25, active: false },
  { id: 3, name: 'Bob', age: 35, active: true }
];

// Map - Transform array
const names: string[] = users.map(user => user.name);
const upperNames: string[] = users.map(user => user.name.toUpperCase());

// Filter - Select elements
const activeUsers: User[] = users.filter(user => user.active);
const adults: User[] = users.filter(user => user.age >= 18);

// Reduce - Aggregate data
const totalAge: number = users.reduce((sum, user) => sum + user.age, 0);
const avgAge: number = totalAge / users.length;

// Group by property
interface GroupedUsers {
  active?: User[];
  inactive?: User[];
}

const byActive: GroupedUsers = users.reduce((groups, user) => {
  const key = user.active ? 'active' : 'inactive';
  return {
    ...groups,
    [key]: [...(groups[key as keyof GroupedUsers] || []), user]
  };
}, {} as GroupedUsers);

// Chaining methods
const result: string = users
  .filter(user => user.active)
  .map(user => user.name)
  .sort()
  .join(', ');
```

**Advanced Array Methods:**
```typescript
// Find - First matching element
const user: User | undefined = users.find(u => u.id === 2);

// FindIndex - Index of first match
const index: number = users.findIndex(u => u.name === 'Jane');

// Some - At least one matches
const hasActive: boolean = users.some(u => u.active);

// Every - All match
const allAdults: boolean = users.every(u => u.age >= 18);

// FlatMap - Map and flatten
interface UserWithTags {
  name: string;
  tags: string[];
}

const userTags: UserWithTags[] = [
  { name: 'John', tags: ['admin', 'user'] },
  { name: 'Jane', tags: ['user'] }
];
const allTags: string[] = userTags.flatMap(u => u.tags);

// From - Create array from iterable
const str = 'hello';
const chars: string[] = Array.from(str);
const numbers: number[] = Array.from({ length: 5 }, (_, i) => i + 1);

// Of - Create array from arguments
const arr: number[] = Array.of(1, 2, 3);
```

### 2. Higher-Order Functions

**Functions as Arguments:**
```typescript
// Custom forEach
function forEach<T>(array: T[], callback: (item: T, index: number, arr: T[]) => void): void {
  for (let i = 0; i < array.length; i++) {
    callback(array[i], i, array);
  }
}

// Custom map
function map<T, U>(array: T[], transform: (item: T) => U): U[] {
  const result: U[] = [];
  for (const item of array) {
    result.push(transform(item));
  }
  return result;
}

// Custom filter
function filter<T>(array: T[], predicate: (item: T) => boolean): T[] {
  const result: T[] = [];
  for (const item of array) {
    if (predicate(item)) {
      result.push(item);
    }
  }
  return result;
}
```

**Functions Returning Functions:**
```typescript
// Currying
const multiply = (a: number) => (b: number): number => a * b;
const double = multiply(2);
const triple = multiply(3);

console.log(double(5));  // 10
console.log(triple(5));  // 15

// Partial application
function partial<T extends unknown[], U extends unknown[], R>(
  fn: (...args: [...T, ...U]) => R,
  ...args: T
): (...moreArgs: U) => R {
  return (...moreArgs: U) => fn(...args, ...moreArgs);
}

const addThree = (a: number, b: number, c: number): number => a + b + c;
const add5 = partial(addThree, 5);
console.log(add5(3, 2));  // 10

// Memoization
function memoize<T extends unknown[], R>(fn: (...args: T) => R): (...args: T) => R {
  const cache = new Map<string, R>();
  return (...args: T): R => {
    const key = JSON.stringify(args);
    if (cache.has(key)) {
      return cache.get(key)!;
    }
    const result = fn(...args);
    cache.set(key, result);
    return result;
  };
}

const fibonacci: (n: number) => number = memoize((n: number): number => {
  if (n <= 1) return n;
  return fibonacci(n - 1) + fibonacci(n - 2);
});
```

### 3. Composition and Piping

```typescript
// Function composition
const compose = <T>(...fns: Array<(arg: T) => T>) =>
  (x: T): T => fns.reduceRight((acc, fn) => fn(acc), x);

const pipe = <T>(...fns: Array<(arg: T) => T>) =>
  (x: T): T => fns.reduce((acc, fn) => fn(acc), x);

// Example usage
const addOne = (x: number): number => x + 1;
const doubleNum = (x: number): number => x * 2;
const square = (x: number): number => x * x;

const composed = compose(square, doubleNum, addOne);
console.log(composed(3));  // ((3 + 1) * 2)^2 = 64

const piped = pipe(addOne, doubleNum, square);
console.log(piped(3));  // ((3 + 1) * 2)^2 = 64

// Practical example
interface UserInput {
  name: string;
  email: string;
  age: string;
}

interface ProcessedUser {
  name: string;
  email: string;
  age: number;
}

const processUser = pipe<UserInput>(
  user => ({ ...user, name: user.name.trim() }),
  user => ({ ...user, email: user.email.toLowerCase() }),
  user => ({ ...user, age: user.age }) as unknown as UserInput
);

const inputUser: UserInput = {
  name: '  John  ',
  email: 'JOHN@EXAMPLE.COM',
  age: '30'
};
const processed = processUser(inputUser);
```

### 4. Pure Functions and Immutability

```typescript
interface CartItem {
  id: string;
  price: number;
}

interface Cart {
  items: CartItem[];
  total: number;
}

// Impure function (modifies input) - AVOID
function addItemImpure(cart: Cart, item: CartItem): Cart {
  cart.items.push(item);
  cart.total += item.price;
  return cart;
}

// Pure function (no side effects) - PREFERRED
function addItemPure(cart: Cart, item: CartItem): Cart {
  return {
    ...cart,
    items: [...cart.items, item],
    total: cart.total + item.price
  };
}

// Immutable array operations
const numbers: readonly number[] = [1, 2, 3, 4, 5];

// Add to array
const withSix: number[] = [...numbers, 6];

// Remove from array
const withoutThree: number[] = numbers.filter(n => n !== 3);

// Update array element
const doubled: number[] = numbers.map(n => n === 3 ? n * 2 : n);

// Immutable object operations
interface SimpleUser {
  name: string;
  age: number;
  email?: string;
}

const simpleUser: SimpleUser = { name: 'John', age: 30 };

// Update property
const olderUser: SimpleUser = { ...simpleUser, age: 31 };

// Add property
const withEmail: SimpleUser = { ...simpleUser, email: 'john@example.com' };

// Remove property
const { age, ...withoutAge } = simpleUser;

// Deep cloning (simple approach)
const deepClone = <T>(obj: T): T => JSON.parse(JSON.stringify(obj));

// Better deep cloning
const structuredCloneObj = <T>(obj: T): T => structuredClone(obj);
```

## Modern Class Features

```typescript
// Class syntax with TypeScript
class User {
  // Private fields
  #password: string;

  // Public fields with types
  id: number;
  name: string;

  // Static field
  static count: number = 0;

  constructor(id: number, name: string, password: string) {
    this.id = id;
    this.name = name;
    this.#password = password;
    User.count++;
  }

  // Public method
  greet(): string {
    return `Hello, ${this.name}`;
  }

  // Private method
  #hashPassword(password: string): string {
    return `hashed_${password}`;
  }

  // Getter
  get displayName(): string {
    return this.name.toUpperCase();
  }

  // Setter
  set password(newPassword: string) {
    this.#password = this.#hashPassword(newPassword);
  }

  // Static method
  static create(id: number, name: string, password: string): User {
    return new User(id, name, password);
  }
}

// Inheritance
class Admin extends User {
  role: string;

  constructor(id: number, name: string, password: string, role: string) {
    super(id, name, password);
    this.role = role;
  }

  greet(): string {
    return `${super.greet()}, I'm an admin`;
  }
}
```

## Modules (ES6)

```typescript
// Exporting
// math.ts
export const PI: number = 3.14159;

export function add(a: number, b: number): number {
  return a + b;
}

export class Calculator {
  multiply(a: number, b: number): number {
    return a * b;
  }
}

// Default export
export default function multiply(a: number, b: number): number {
  return a * b;
}

// Importing
// app.ts
import multiply, { PI, add, Calculator } from './math';

// Rename imports
import { add as sum } from './math';

// Import all
import * as Math from './math';

// Dynamic imports
const module = await import('./math');
const { add: addFn } = await import('./math');

// Conditional loading
declare const condition: boolean;
if (condition) {
  const module = await import('./feature');
  module.init();
}

// Type-only imports
import type { SomeType } from './types';
import { someFunction, type AnotherType } from './utils';
```

## Iterators and Generators

```typescript
// Custom iterator
interface Range {
  from: number;
  to: number;
  [Symbol.iterator](): Iterator<number>;
}

const range: Range = {
  from: 1,
  to: 5,

  [Symbol.iterator](): Iterator<number> {
    let current = this.from;
    const last = this.to;

    return {
      next(): IteratorResult<number> {
        if (current <= last) {
          return { done: false, value: current++ };
        } else {
          return { done: true, value: undefined };
        }
      }
    };
  }
};

for (const num of range) {
  console.log(num);  // 1, 2, 3, 4, 5
}

// Generator function
function* rangeGenerator(from: number, to: number): Generator<number> {
  for (let i = from; i <= to; i++) {
    yield i;
  }
}

for (const num of rangeGenerator(1, 5)) {
  console.log(num);
}

// Infinite generator
function* fibonacci(): Generator<number, void, unknown> {
  let [prev, curr] = [0, 1];
  while (true) {
    yield curr;
    [prev, curr] = [curr, prev + curr];
  }
}

// Async generator
async function* fetchPages<T>(url: string): AsyncGenerator<T[]> {
  let page = 1;
  while (true) {
    const response = await fetch(`${url}?page=${page}`);
    const data: T[] = await response.json();
    if (data.length === 0) break;
    yield data;
    page++;
  }
}

for await (const page of fetchPages<User>('/api/users')) {
  console.log(page);
}
```

## Modern Operators

```typescript
interface UserWithAddress {
  name: string;
  address?: {
    city: string;
    zipCode?: string;
  };
  method?: () => void;
}

// Optional chaining
const userWithAddr: UserWithAddress = { name: 'John', address: { city: 'NYC' } };
const city: string | undefined = userWithAddr?.address?.city;
const zipCode: string | undefined = userWithAddr?.address?.zipCode;  // undefined

// Function call
const result: void | undefined = userWithAddr.method?.();

// Array access
const arr: number[] = [1, 2, 3];
const first: number | undefined = arr?.[0];

// Nullish coalescing
const value1: string = null ?? 'default';      // 'default'
const value2: string = undefined ?? 'default'; // 'default'
const value3: number = 0 ?? 100;               // 0 (not 100)
const value4: string = '' ?? 'default';        // '' (not 'default')

// Logical assignment
let a: string | null = null;
a ??= 'default';  // a = 'default'

let b: number = 5;
b ??= 10;  // b = 5 (unchanged)

const obj = { count: 0 };
obj.count ||= 1;  // obj.count = 1
obj.count &&= 2;  // obj.count = 2
```

## Performance Optimization

```typescript
// Debounce
function debounce<T extends (...args: unknown[]) => void>(
  fn: T,
  delay: number
): (...args: Parameters<T>) => void {
  let timeoutId: ReturnType<typeof setTimeout>;
  return (...args: Parameters<T>) => {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => fn(...args), delay);
  };
}

declare function search(query: string): void;
const searchDebounced = debounce(search, 300);

// Throttle
function throttle<T extends (...args: unknown[]) => void>(
  fn: T,
  limit: number
): (...args: Parameters<T>) => void {
  let inThrottle = false;
  return (...args: Parameters<T>) => {
    if (!inThrottle) {
      fn(...args);
      inThrottle = true;
      setTimeout(() => inThrottle = false, limit);
    }
  };
}

declare function handleScroll(): void;
const scrollThrottled = throttle(handleScroll, 100);

// Lazy evaluation
function* lazyMap<T, U>(iterable: Iterable<T>, transform: (item: T) => U): Generator<U> {
  for (const item of iterable) {
    yield transform(item);
  }
}

// Use only what you need
const nums: number[] = [1, 2, 3, 4, 5];
const doubledLazy = lazyMap(nums, x => x * 2);
const firstDoubled = doubledLazy.next().value;  // Only computes first value
```

## Best Practices

1. **Use const by default**: Only use let when reassignment is needed
2. **Prefer arrow functions**: Especially for callbacks
3. **Use template literals**: Instead of string concatenation
4. **Destructure objects and arrays**: For cleaner code
5. **Use async/await**: Instead of Promise chains
6. **Avoid mutating data**: Use spread operator and array methods
7. **Use optional chaining**: Prevent "Cannot read property of undefined"
8. **Use nullish coalescing**: For default values
9. **Prefer array methods**: Over traditional loops
10. **Use modules**: For better code organization
11. **Write pure functions**: Easier to test and reason about
12. **Use meaningful variable names**: Self-documenting code
13. **Keep functions small**: Single responsibility principle
14. **Handle errors properly**: Use try/catch with async/await
15. **Enable strict mode**: Use TypeScript strict compiler options

## Common Pitfalls

1. **this binding confusion**: Use arrow functions or bind()
2. **Async/await without error handling**: Always use try/catch
3. **Promise creation unnecessary**: Don't wrap already async functions
4. **Mutation of objects**: Use spread operator or Object.assign()
5. **Forgetting await**: Async functions return promises
6. **Blocking event loop**: Avoid synchronous operations
7. **Memory leaks**: Clean up event listeners and timers
8. **Not handling promise rejections**: Use catch() or try/catch
