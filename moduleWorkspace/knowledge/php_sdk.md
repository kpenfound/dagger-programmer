# Using the Dagger PHP SDK

All queries chain from the global 'dag()' variable
Assume `dag()` is available globally.

In PHP, you must `use function Dagger\dag;` as well as the other Dagger types you are using.

## Chaining and Fields

Object types directly translate to struct types, and have methods for each field.

```php
dag()->container() # container
    ->withExec(['sh', '-c', 'echo hey > ./some-file']) # container
    ->file('./some-file'); # file
```

Calling a method that returns an object type is always lazy, and never returns
an error:

```php
my_file = dag()->container() # container
    ->withExec(['sh', '-c', 'echo hey > ./some-file']) # container
    ->file('./some-file'); # file
```

## Arguments

When a field's argument is non-null ('String!') and does not have a default
('String! = ...'), it is a REQUIRED argument. These are passed as regular
method arguments:

```php
dag()->container()
    ->withExec(['echo', 'hey']) # args: [String!]!
    ->file('./some-file'); # path: String!
```

When a field's argument is nullable ('String', '[String!]') or has a default
('String! = 'foo''), it is an OPTIONAL argument. These are passed in as named arguments:

```php
dag()->container()
    ->withExec(['start'], useEntrypoint: true);
```

When a field ONLY has optional arguments, just pass the named arguments:

```php
dag()->container()
    ->withExec(['run'])
    ->asService(experimentalPrivilegedNesting: true);
```

## Inline Documentation

Dagger modules can be documented in 3 ways:
1. Module documentation goes at the top of the file
2. Function method documentation describes what a function does
3. Function argument documentation describes what each argument is for

Below is a simple module that includes all of this documentation:

```php
<?php

declare(strict_types=1);

namespace DaggerModule;

use Dagger\Attribute\{DaggerObject, DaggerFunction, Doc};

#[DaggerObject]
#[Doc('A simple example module to say hello.')]
class MyModule
{
    #[DaggerFunction]
    #[Doc('Return a greeting')]
    public function hello(
        #[Doc('Who to greet')]
        string $name,
        #[Doc('The greeting to display')]
        string $greeting
    ): string {
        return "{$greeting} {$name}";
    }

    #[DaggerFunction]
    #[Doc('Return a loud greeting')]
    public function loudHello(
        #[Doc('Who to greet')]
        string $name,
        #[Doc('The greeting to display')]
        string $greeting
    ): string {
        return strtoupper("{$greeting} {$name}");
    }
}
```
