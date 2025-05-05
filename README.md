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

### Translation

Translate a Module from one SDK to another. This is useful for tasks like maintaining the Dagger documentation where you need the same code in multiple languages.

⋈ Load the module in
```
cd github.com/kpenfound/dagger-programmer
```

The agent can translate a Dagger module from it's original language to any other supported Dagger SDK.

⋈ Run the translate function:
```
translate github.com/shykes/hello typescript | terminal
```

The agent can generate example usage for a Dagger module in the format recognized by the Daggerverse. This means creating a module at `examples/{sdk}` for each supported SDK. The example module shows how to use each function in the original module.

⋈ Generate examples for a module.
```
write-examples github.com/shykes/hello | terminal
```

#### What's next?

- Assist in developing a module
- Generate an entire module based on a detailed prompt
- Generate an entire module to Daggerize an application just by looking at the application
