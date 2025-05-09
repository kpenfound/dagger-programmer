# Using the Dagger Go SDK

All queries chain from the global 'dag' variable
Assume `dag` is available globally.

In Go, you must `import "dagger/{module_name}/internal/dagger"`

## Chaining and Fields

Object types directly translate to struct types, and have methods for each field.

```go
dag.Container(). // *Container
    WithExec([]string{"sh", "-c", "echo hey > ./some-file"}). // *Container
    File("./some-file") // *File
```

Calling a method that returns an object type is always lazy, and never returns
an error:

```go
myFile := dag.Container(). // *Container
    WithExec([]string{"sh", "-c", "echo hey > ./some-file"}). // *Container
    File("./some-file") // *File
```

Calling a method that returns a scalar or list takes a `context.Context`
argument and returns an `error`:

```go
stdout, err := dag.Container().
    WithExec([]string{"echo", "Hello, world!"]).
    Stdout(ctx)
```

Calling a field that returns `Void` just returns `error` instead of `(Void, error)`:

```go
err := service.Stop(ctx)
```

## Arguments

When a field's argument is non-null ('String!') and does not have a default
('String! = ...'), it is a REQUIRED argument. These are passed as regular
method arguments:

```go
dag.Container().
    WithExec([]string{"echo", "hey"}). // args: [String!]!
    File("./some-file") // path: String!
```

When a field's argument is nullable ('String', '[String!]') or has a default
('String! = "foo"'), it is an OPTIONAL argument. These are passed in an 'Opts'
struct named after the receiving type ('Container') and the field ('withExec'):

```go
dag.Container().
    WithExec([]string{"start"}, dagger.ContainerWithExecOpts{
        UseEntrypoint: true, // useEntrypoint: Boolean = false
    })
```

When a field ONLY has optional arguments, just pass the 'Opts' struct:

```go
dag.Container().
    WithExec([]string{"run"}).
    AsService(dagger.ContainerAsServiceOpts{
        ExperimentalPrivilegedNesting: true,
    })
```

## Inline Documentation

Dagger modules can be documented in 3 ways:
1. Module documentation goes at the top of the file
2. Function method documentation describes what a function does
3. Function argument documentation describes what each argument is for

Below is a simple module that includes all of this documentation:

```go
// A simple example module to say hello.

// Further documentation for the module here.

package main

import (
	"fmt"
	"strings"
)

type MyModule struct{}

// Return a greeting.
func (m *MyModule) Hello(
	// Who to greet
	name string,
	// The greeting to display
	greeting string,
) string {
	return fmt.Sprintf("%s, %s!", greeting, name)
}

// Return a loud greeting.
func (m *MyModule) LoudHello(
	// Who to greet
	name string,
	// The greeting to display
	greeting string,
) string {
	out := fmt.Sprintf("%s, %s!", greeting, name)
	return strings.ToUpper(out)
}
```
