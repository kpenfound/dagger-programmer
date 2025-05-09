from typing import Annotated
from dagger import dag, Doc, Directory, function, Module, object_type

@object_type
class DaggerProgrammer:
    model: Annotated[str | None, Doc("LLM model to use")] = None
    dagger_version: Annotated[str, Doc("version of the dagger CLI to use")] = "v0.18.5"
    @function
    async def translate(
        self,
        module: Annotated[Module, Doc("The dagger module to translate")],
        language: Annotated[str, Doc("The language to translate the module to")],
        dependencies: Annotated[list[Directory], Doc("Dependencies required for the module")] = [],
        skip_test: Annotated[bool, Doc("Skip running tests after translating")] = False,
    ) -> Directory:
        """Returns a dagger module in the specified language translated from the provided module"""
        # read the current module
        source_mod_sdk = await module.sdk().source()
        source_mod_name = await module.name()

        # Create a mod/workspace for the translated sdk
        ws = dag.module_workspace(
                language,
                source_mod_name,
                dagger_version=self.dagger_version,
                dependencies=dependencies
            )

        source_mod_file = (
            await module.source().directory(".")
            .file(
                await dag.module_helper()
                .get_sdk_main_file(source_mod_sdk, source_mod_name)
            )
            .contents()
        )

        environment = (
            dag.env()
            .with_module_workspace_input("workspace", ws, "workspace to develop dagger modules")
            .with_string_input("source_mod_sdk", source_mod_sdk, "")
            .with_string_input("source_mod_file", source_mod_file, "")
            .with_string_input("language", language, "")
            .with_module_workspace_output("output", "the workspace containing the translated module")
        )
        # translate the source mod to the target sdk
        work = (
            dag
            .llm(model=self.model)
            .with_env(environment)
            .with_prompt(await ws.get_sdk_reference(source_mod_sdk))
            .with_prompt(await ws.get_sdk_reference(language))
            .with_prompt_file(dag.current_module().source().file("prompt_translator.md"))
            .env().output("output").as_module_workspace()
        )

        # Check again that test passes because LLMs lie
        if (not skip_test) and (await work.test() != "TEST PASSED"):
            raise Exception("Translated module did not pass test")

        # return work output
        return work.workspace()

    @function
    async def write_examples(
        self,
        module: Annotated[Module, Doc("The dagger module to write examples for")],
    ) -> Directory:
        """Writes examples in all supported languages for the provided module and returns the directory containing them"""
        # write example in the Go
        example_lang = "go"
        source_mod_schema = await dag.module_helper().get_module_schema(module)
        source_mod_name = await module.name()
        source_mod_dir = module.source().directory(".")
        ws = dag.module_workspace(
            example_lang,
            "example",
            dependencies=[source_mod_dir],
            dagger_version=self.dagger_version
        )

        environment = (
            dag.env()
            .with_module_workspace_input("workspace", ws, "workspace to develop dagger modules")
            .with_string_input("source_mod_schema", source_mod_schema, "")
            .with_module_workspace_output("output", "the workspace containing the example module")
        )

        example_work = (
            dag
            .llm(model=self.model)
            .with_env(environment)
            .with_prompt(await ws.get_examples_reference())
            .with_prompt_file(dag.current_module().source().file("prompt_exampler.md"))
            .env().output("output").as_module_workspace()
        )

        # # make sure the first example works
        if await example_work.test() != "TEST PASSED":
            raise Exception("Generated example did not pass test")
        example = example_work.workspace()
        example_mod = self.convert_example_to_module(example, source_mod_name, example_lang)
        dep_swapped_example = (
            self.fake_example_mod(example, source_mod_name, example_lang)
            .with_directory(f"{source_mod_name}", source_mod_dir)
            .as_module()
        )
        # translate that example to the other languages
        all_examples = dag.directory().with_directory(f"examples/{example_lang}", example_mod)

        for sdk in ["python", "typescript", "php", "java"]: # initial example is Go
            translated_example = await self.translate(dep_swapped_example, sdk, dependencies=[source_mod_dir], skip_test=False)
            translated_mod = self.convert_example_to_module(translated_example, source_mod_name, sdk)
            all_examples = all_examples.with_directory(f"examples/{sdk}", translated_mod)

        # return the directory including all the examples
        return all_examples

    def convert_example_to_module(self, example: Directory, dependency: str, sdk: str) -> Directory:
        """Generates the dagger.json and other files needed for a module"""
        return example.with_new_file("dagger.json", f'''
{{
    "name": "example",
    "engineVersion": "{self.dagger_version}",
    "sdk": "{sdk}",
    "dependencies": [
    {{
        "name": "{dependency}",
        "source": "../..",
        "pin": ""
    }}
    ],
    "source": "."
}}
''')

    def fake_example_mod(self, example: Directory, dependency: str, sdk: str) -> Directory:
        """Generates the dagger.json and other files needed for a module"""
        return example.with_new_file("dagger.json", f'''
{{
    "name": "example",
    "engineVersion": "{self.dagger_version}",
    "sdk": "{sdk}",
    "dependencies": [
    {{
        "name": "{dependency}",
        "source": "./{dependency}",
        "pin": ""
    }}
    ],
    "source": "."
}}
''')
