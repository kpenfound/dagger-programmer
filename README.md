# Dagger Programmer

This is an AI Agent specialized in Dagger modules.

For information using Dagger with agents, check out [Dagger for AI Agents](https://docs.dagger.io/ai-agents)

## Capabilities

### Translate

The agent can translate a Dagger module from it's original language to any other supported Dagger SDK.

For example:

```
translate github.com/shykes/hello typescript
```

### Write Examples

The agent can generate example usage for a Dagger module in the format recognized by the Daggerverse. This means creating a module at `examples/{sdk}` for each supported SDK. The example module shows how to use each function in the original module.

For example:

```
write-examples github.com/shykes/hello
```
