# Dagger Programmer 🤖

## An AI Agent specialized in Dagger modules.

### What is this?
This is an agent specialized in working with Dagger modules. It can handle tasks like translating, writing examples, and maybe soon writing new functions.

TODO: add gif

### How do I try it?
Start a dev Dagger Engine with LLM support using:
https://docs.dagger.io/ai-agents#initial-setup

$ Start Dagger Shell:
```
dagger
```

⋈ Load the module
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

- Write new functions for a module
- Generate an entire module to Daggerize an application
- ???
