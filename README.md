# Dagger Programmer 🤖

## An AI Agent specialized in Dagger modules.

This is an agent specialized in working with [Dagger](https://dagger.io) modules.

Current capabilities:
- Translate a module from one SDK to another
- Create examples for a module in every supported SDK

Check out the full demo below:

[![Watch the video](https://img.youtube.com/vi/Vqqz052vmHc/maxresdefault.jpg)](https://www.youtube.com/watch?v=Vqqz052vmHc)

## Usage

The following examples all use Dagger shell. To get in Dagger shell, just type `dagger`

⋈ Switch to this module in your shell
```
cd github.com/kpenfound/dagger-programmer
```

### Translation

Translate a Module from one SDK to another. This is useful for tasks like maintaining the Dagger documentation where you need the same code in multiple languages.

The `translate` function has two arguments:
- module: The path to the module that you would like translated. A module path is the directory where your dagger.json is. So if I have `./mymod/dagger.json`, I would pass in `./mymod`. Github URLs are also accepted, just like any Dagger module reference.
- language: The language to translate the module into. Valid options are go, python, typescript, php, and java.

This will output a `dagger.Directory` containing the translated module. With that Directory, you can inspect the translated files with `| terminal`, and then export them to the desired path on your host `| export ./php/`

After exporting, it is recommended to carefully evaluate the code for correctness. AI can make mistakes :)

Example:

⋈ Translate the shykes/hello module to typescript:
```
translate github.com/shykes/hello typescript | terminal
```

If the module has dependencies, specify those with the optional `--dependencies`:

⋈ Translate the shykes/hello module to typescript:
```
translate github.com/shykes/hello typescript --dependencies github.com/kpenfound/dagger-modules/proxy,./local/path/another/dependency | terminal
```

### Generate examples

The agent can generate example usage for a Dagger module in the format recognized by the Daggerverse. This means creating a module at `examples/{sdk}` for each supported SDK. The example module shows how to use each function in the original module.

The `write-examples` function has one argument:
- module: The path to the module that you would like examples for. A module path is the directory where your dagger.json is. So if I have `./mymod/dagger.json`, I would pass in `./mymod`. Github URLs are also accepted, just like any Dagger module reference.

This will output a `dagger.Directory` containing the all of the example modules. With that Directory, you can inspect the example files with `| terminal`, and then export them to the desired path on your host `| export ./examples/`

Example:

⋈ Generate examples for a the shykes/hello module:
```
write-examples github.com/shykes/hello | terminal
```

### What's next?

- Assist in developing a module
- Generate an entire module based on a detailed prompt
- Generate an entire module to Daggerize an application just by looking at the application
