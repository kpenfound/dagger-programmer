import re
from dagger import function, Module, object_type, TypeDef

@object_type
class ModuleHelper:
    @function
    def get_sdk_main_file(self, sdk: str, name: str) -> str:
        """Get the main SDK file path for the given module name and SDK"""
        return {
            "go": "main.go",
            "python": f"src/{to_python_case(name)}/main.py",
            "typescript": "src/index.ts",
            "php": f"src/{to_pascal_case(name)}.php",
            "java": f"src/main/java/io/dagger/modules/{to_pascal_case(name).lower()}/{to_pascal_case(name)}.java"
        }[sdk]

    @function
    async def get_module_schema(self, mod: Module) -> str:
        """Get the schema of a module represented as an XML string"""
        mod_name = await mod.name()
        mod_description = await mod.description()
        mod_objects = await mod.objects()
        schema = f"\n<module name='{mod_name}' description='{mod_description}'>"
        for obj in mod_objects:
            funcs = await obj.as_object().functions()
            for func in funcs:
                func_name = await func.name()
                func_description = await func.description()
                func_return_type = await self.get_type_name(func.return_type())
                schema += f"\n\t<function name='{func_name}' description='{func_description}' returns='{func_return_type}'>"
                func_args = await func.args()
                for arg in func_args:
                    arg_name = await arg.name()
                    arg_type = await self.get_type_name(arg.type_def())
                    arg_description = await arg.description()
                    schema += f"\n\t\t<arg name='{arg_name}' type='{arg_type}' description='{arg_description}' />"
                schema += "\n\t</function>"
        return schema + "\n</module>"

    @function
    async def get_type_name(self, type: TypeDef) -> str:
        opt = "!"
        if await type.optional():
            opt = ""
        """Get the type name of a TypeDef"""
        kind = await type.kind()
        if kind == "OBJECT_KIND":
            return await type.as_object().name() + opt
        if kind == "SCALAR_KIND":
            return await type.as_scalar().name() + opt
        if kind == "ENUM_KIND":
            return await type.as_enum().name() + opt
        if kind == "INPUT_KIND":
            return await type.as_input().name() + opt
        if kind == "STRING_KIND":
            return "String" + opt
        if kind == "INTEGER_KIND":
            return "Integer" + opt
        if kind == "BOOLEAN_KIND":
            return "Boolean" + opt
        if kind == "LIST_KIND":
            return "List" + opt
        if kind == "VOID_KIND":
            return "Void" + opt

        return "UNKNOWN"

def to_python_case(input_string: str) -> str:
    return input_string.replace("-", "_")

def to_pascal_case(input_string: str) -> str:
  """
  Converts a string with spaces, hyphens, or underscores into PascalCase.

  PascalCase (or UpperCamelCase) means the first letter of each
  compound word is capitalized, and there are no separators.

  Args:
    input_string: The string to convert. Can contain spaces, hyphens (-),
                  or underscores (_).

  Returns:
    The PascalCase version of the string, or an empty string if the
    input results in no words after splitting.
  """
  if not input_string:
      return ""

  # Split the string by space, hyphen, or underscore
  # The regex '[ _-]+' matches one or more occurrences of space, underscore, or hyphen
  words = re.split('[ _-]+', input_string)

  # Capitalize the first letter of each word and join them
  # Filter out any empty strings that might result from multiple delimiters
  pascal_case_string = ''.join(word.capitalize() for word in words if word)

  return pascal_case_string
