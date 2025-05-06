# Using the Dagger Java SDK

All queries chain from the global 'dag' variable
Assume `dag` is available globally.

In Java, you must `import static io.dagger.client.Dagger.dag;`

## Chaining and Fields

Object types directly translate to struct types, and have methods for each field.

```java
dag.container() // *Container
    .withExec(List.of("sh", "-c", "echo hey > ./some-file")) // *Container
    .file("./some-file"); // *File
```

Calling a method that returns an object type is always lazy, and never returns
an error:

```java
File myFile = dag.container() // *Container
    .withExec(List.of("sh", "-c", "echo hey > ./some-file")) // *Container
    .file("./some-file"); // *File
```

Calling a method that returns a scalar or list takes a `context.Context`
argument and returns an `error`:

```java
String stdout = dag.container()
    .withExec(List.of("echo", "Hello, world!"))
    .stdout();
```

Calling a field that returns `Void` just returns `error` instead of `(Void, error)`:

```java
service.Stop();
```

## Arguments

When a field's argument is non-null ('String!') and does not have a default
('String! = ...'), it is a REQUIRED argument. These are passed as regular
method arguments:

```java
dag.container()
    .withExec(List.of("echo", "hey")) // args: [String!]!
    .file("./some-file"); // path: String!
```

When a field's argument is nullable ('String', '[String!]') or has a default
('String! = "foo"'), it is an OPTIONAL argument. These are passed in an 'Opts'
struct named after the receiving type ('Container') and the field ('.withExec'):

```java
dag.container()
    .withExec(List.of("start"), new Container.WithExecArguments().withUseEntrypoint(true));
```

When a field ONLY has optional arguments, just pass the 'Opts' struct:

```java
dag.container()
    .withExec(List.of("run"))
    .asService(new Container.AsServiceArguments().withExperimentalPrivilegedNesting(true));
```

## Inline Documentation

Dagger modules can be documented in 3 ways:
1. Module documentation goes at the top of the file
2. Function method documentation describes what a function does
3. Function argument documentation describes what each argument is for

Below is a simple module that includes all of this documentation:

```java
package io.dagger.modules.mymodule;

import io.dagger.module.annotation.Function;
import io.dagger.module.annotation.Object;

@Object
public class MyModule {
  /**
   * Return a greeting.
   *
   * @param name Who to greet
   * @param greeting The greeting to display
   */
  @Function
  public String hello(String name, String greeting) {
    return greeting + " " + name;
  }

  /**
   * Return a loud greeting.
   *
   * @param name Who to greet
   * @param greeting The greeting to display
   */
  @Function
  public String loudHello(String name, String greeting) {
    return greeting.toUpperCase() + " " + name.toUpperCase();
  }
}
```
