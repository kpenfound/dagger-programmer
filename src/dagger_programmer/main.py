from typing import Annotated
from dagger import dag, Doc, Directory, function, Module, object_type

@object_type
class DaggerProgrammer:
    model: Annotated[str | None, Doc("LLM model to use")] = None
    dagger_version: Annotated[str, Doc("version of the dagger CLI to use")] = "v0.16.2"
    @function
    async def translate(
        self,
        mod: Annotated[Module, Doc("The dagger module to translate")],
        language: Annotated[str, Doc("The language to translate the module to")],
        dependencies: Annotated[list[Directory], Doc("Dependencies required for the module")] = [],
    ) -> Directory:
        """Returns a dagger module in the specified language translated from the provided module"""
        # read the current module
        source_mod_sdk = await mod.sdk().source()
        source_mod_name = await mod.name()

        # Create a mod/workspace for the translated sdk
        ws = dag.module_workspace(
                language,
                source_mod_name,
                dagger_version=self.dagger_version,
                dependencies=dependencies
            )

        source_mod_file = (
            await mod.source().directory(".")
            .file(
                await dag.module_helper()
                .get_sdk_main_file(source_mod_sdk, source_mod_name)
            )
            .contents()
        )
        # translate the source mod to the target sdk
        work = (
            dag
            .llm(model=self.model)
            .with_module_workspace(ws)
            .with_prompt(await ws.get_sdk_reference(source_mod_sdk))
            .with_prompt(await ws.get_sdk_reference(language))
            .with_prompt_var("language", language)
            .with_prompt_var("source_mod_sdk", source_mod_sdk)
            .with_prompt_var("source_mod_file", source_mod_file)
            .with_prompt_file(dag.current_module().source().file("prompt_translator.txt"))
            .module_workspace()
        )

        # Check again that test passes because LLMs lie
        if await work.test() != "TEST PASSED":
            raise Exception("Translated module did not pass test")

        # return work output
        return work.workspace()

    @function
    async def write_examples(
        self,
        mod: Annotated[Module, Doc("The dagger module to write examples for")],
    ) -> Directory:
        """Writes examples in all supported languages for the provided module and returns the directory containing them"""
        # write example in the Go
        example_lang = "go"
        source_mod_schema = await dag.module_helper().get_module_schema(mod)
        source_mod_name = await mod.name()
        source_mod_dir = mod.source().directory(".")
        ws = dag.module_workspace(
            example_lang,
            "example",
            dependencies=[source_mod_dir],
            dagger_version=self.dagger_version
        )

        example_work = (
            dag
            .llm(model=self.model)
            .with_module_workspace(ws)
            .with_prompt(await ws.get_examples_reference())
            .with_prompt_var("source_mod_schema", source_mod_schema)
            .with_prompt_file(dag.current_module().source().file("prompt_exampler.txt"))
            .module_workspace()
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

        for sdk in ["python", "typescript"]: # , "php", "java"]: # started with Go
            translated_example = await self.translate(dep_swapped_example, sdk, dependencies=[source_mod_dir])
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
