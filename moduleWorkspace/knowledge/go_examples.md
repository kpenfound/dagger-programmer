## Overview

A Dagger Example module is a normal Dagger module that calls the functions of the module you're creating examples for.
An example module has a function for each function in the assignment module that shows how it can be used.

All queries chain from the global 'dag' variable
Assume `dag` is available globally.

Your example module's name is `example`.
Your example module's import line must be `import "dagger/example/internal/dagger"`

## Function naming scheme

By adhering to the following function naming schemes, the functions will be properly associated with the functions
in the module you are creating examples for.

If you have a module called 'Foo' and a function called 'Bar', you can create the following functions in your example module:
- A function 'Foo_Baz' will create a top level example for the 'Foo' module called Baz.
- A function 'FooBar' will create an example for function 'Bar'.
- Functions 'FooBar_Baz' will create a Baz example for the function 'Bar'.

## Go SDK Usage

Object types directly translate to struct types, and have methods for each field.

```go
dag.Container(). // *Container
    WithExec([]string{"sh", "-c", "echo hey > ./some-file"}). // *Container
    File("./some-file") // *File
```

Calling a method that returns a scalar or list takes a `context.Context`
argument and returns an `error`. Note the `ctx` is passed to the final method
and not the constructor of the object:

```go
func (m *Example) FooBar(ctx context.Context) (string, error) {
	stdout, err := dag.Container().
	WithExec([]string{"echo", "Hello, world!"]).
	Stdout(ctx)
	if err != nil {
		return "", err
	}
	return stdout, nil
}
```

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

When passing Opts structs to another module called Foo with a function Baz,
the Opts struct will be named after the receiving type ('Foo') and the field ('Bar'):

```go
dag.Foo().
	Bar(dagger.FooBarOpts{
		Baz: true, // baz: Boolean = false
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

## Example reference

Consider the "proxy" module:

```xml
<module name='proxy' description=''>
        <function name='service' description='Get the proxy Service' returns='Service!'>
        </function>
        <function name='withService' description='Add a service to proxy' returns='Proxy!'>
                <arg name='service' type='Service!' description='A content-addressed service providing TCP connectivity.' />
                <arg name='name' type='String!' description='' />
                <arg name='frontend' type='Integer!' description='' />
                <arg name='backend' type='Integer!' description='' />
                <arg name='isTcp' type='Boolean!' description='' />
        </function>
</module>
```

The example module for the proxy module would look like this:

```go
// Proxy examples in Go
package main

import "dagger/example/internal/dagger"

type Example struct{}

// Example for WithService function
func (m *Example) ProxyWithService(service *dagger.Service) *dagger.Service {
	return dag.Proxy().
		WithService(
			service,     // Dagger service to proxy
			"MyService", // Name of the service
			8080,        // Port for the proxy to listen on
			80,          // Port for the proxy to forward to
		).Service()
}

// Example for Service function
func (m *Example) ProxyService(serviceA *dagger.Service, serviceB *dagger.Service) *dagger.Service {
	return dag.Proxy().
		WithService(
			serviceA,   // Dagger service to proxy
			"ServiceA", // Name of the service
			8080,       // Port for the proxy to listen on
			80,         // Port for the proxy to forward to
		).
		WithService(
			serviceB,   // Dagger service to proxy
			"ServiceB", // Name of the service
			8081,       // Port for the proxy to listen on
			80,         // Port for the proxy to forward to
		).
		Service() // Return a Dagger service proxying to multiple services
}
```
