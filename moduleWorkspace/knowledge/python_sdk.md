# Using the Dagger Python SDK

All queries chain from the global 'dag' variable
Assume `dag` is available globally.

In Python, you must `from dagger import dag, function, object_type` as well as the other Dagger types you are using.

## Chaining and Fields

Object types directly translate to struct types, and have methods for each field.

```python
dag.container(). # container
    with_exec(["sh", "-c", "echo hey > ./some-file"]). # container
    file("./some-file") # file
```

Calling a method that returns an object type is always lazy, and never returns
an error:

```python
my_file = dag.container(). # container
    with_exec(["sh", "-c", "echo hey > ./some-file"]). # container
    file("./some-file") # file
```

## Arguments

When a field's argument is non-null ('String!') and does not have a default
('String! = ...'), it is a REQUIRED argument. These are passed as regular
method arguments:

```python
dag.container().
    with_exec(["echo", "hey"]). # args: [String!]!
    file("./some-file") # path: String!
```

When a field's argument is nullable ('String', '[String!]') or has a default
('String! = "foo"'), it is an OPTIONAL argument. These are passed in as named arguments:

```python
dag.container().
    with_exec(["start"], use_entrypoint=True)
```

When a field ONLY has optional arguments, just pass the named arguments:

```python
dag.container().
    with_exec(["run"]).
    as_service(experimental_privileged_nesting=True)
```
