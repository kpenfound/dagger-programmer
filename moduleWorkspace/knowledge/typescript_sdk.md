# Using the Dagger Typescript SDK

All queries chain from the global 'dag' variable
Assume `dag` is available globally.

In Typescript, you must `import { dag, object, func } from "@dagger.io/dagger";` as well as the other Dagger types you are using.

## Chaining and Fields

Object types directly translate to struct types, and have methods for each field.

```typescript
dag.container() // container
    .withExec(["sh", "-c", "echo hey > ./some-file"]) // container
    .file("./some-file") // file
```

Calling a method that returns an object type is always lazy, and never returns
an error:

```typescript
const myFile = dag.container() // container
    .withExec(["sh", "-c", "echo hey > ./some-file"]) // container
    .file("./some-file") // file
```

## Arguments

When a field's argument is non-null ('String!') and does not have a default
('String! = ...'), it is a REQUIRED argument. These are passed as regular
method arguments:

```typescript
dag.container()
    .withExec(["echo", "hey"]) // args: [String!]!
    .file("./some-file") // path: String!
```

When a field's argument is nullable ('String', '[String!]') or has a default
('String! = "foo"'), it is an OPTIONAL argument. These are passed in an optional object:

```typescript
dag.container().
    withExec(["start"], { useEntrypoint: true })
```

When a field ONLY has optional arguments, just pass the optional object:

```typescript
dag.container().
    withExec(["run"]).
    asService({ experimentalPrivilegedNesting: true })
```
