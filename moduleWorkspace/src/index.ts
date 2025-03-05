/**
 * A generated module for DagWorkspace functions
 */
import {
  Container,
  dag,
  Directory,
  object,
  func,
  ReturnType,
} from "@dagger.io/dagger";

@object()
export class ModuleWorkspace {
  /*
   * The workspace directory
   */
  @func()
  workspace: Directory;
  sdk: string;
  name: string;
  dependencies: Directory[];
  daggerVersion: string;

  constructor(
    /*
     * module SDK
     */
    sdk: string,
    /*
     * module name
     */
    name: string,
    /*
     * module dependencies
     */
    dependencies: Directory[] = [],
    /*
     * Dagger Version
     */
    daggerVersion = "latest",
    /*
     * Workspace directory
     */
    workspace?: Directory,
  ) {
    this.sdk = sdk;
    this.name = name;
    this.dependencies = dependencies;
    this.daggerVersion = daggerVersion;
    this.workspace = workspace ?? dag.directory();
  }
  /**
   * Writes the module code to the workspace
   * @param content The updated module code
   */
  @func()
  async write(content: string): Promise<ModuleWorkspace> {
    // NOTE: constraining this to the default file path for now to keep things simple
    // To develop module examples or more complicated modules, this will need to be unlocked
    this.workspace = this.workspace.withNewFile(
      await dag.moduleHelper().getSdkMainFile(this.sdk, this.name),
      content,
    );
    return this;
  }

  /**
   * Reads the module code from the workspace
   */
  @func()
  async read(): Promise<string> {
    return await this.workspace
      .file(await dag.moduleHelper().getSdkMainFile(this.sdk, this.name))
      .contents();
  }

  /**
   * Test if a module works by outputting the module functions
   */
  @func()
  async test(): Promise<string> {
    const dagger = await this.daggerCommand();
    const functions = dagger.withExec(["/usr/local/bin/dagger", "functions"], {
      experimentalPrivilegedNesting: true,
      expect: ReturnType.Any,
    });
    if ((await functions.exitCode()) != 0) {
      return this.trimDaggerError(await functions.stderr());
    }
    return "TEST PASSED"; // Just return passed. Functions output is confusing
  }

  /**
   * Get SDK reference information for developing with a Dagger SDK
   * @param sdk Dagger SDK language to get reference for
   */
  @func()
  async getSdkReference(sdk: string): Promise<string> {
    const daggerDocs = dag
      .git("https://github.com/dagger/dagger")
      .head()
      .tree()
      .directory("docs/current_docs/");

    // Messing around with changing which snippets are included. Dont want to overload the LLM with too much info
    const snippets: { [key: string]: string } = {
      // "multi stage build": "/cookbook/snippets/builds/multi-stage-build",
      // "cache volumes": "/cookbook/snippets/builds/cache",
      // "secret variables": "/cookbook/snippets/secret-variable",
      "bind services to containers": "/api/snippets/services/bind-services",
      // "expose services to the host": "/api/snippets/services/expose-dagger-services-to-host",
    };

    // FIXME: ideally cookbook snippets would follow module structure too
    const snippetSdkPaths: { [key: string]: string } = {
      go: "main.go",
      python: "main.py",
      typescript: "index.ts",
      php: "src/MyModule.php",
      java: "src/main/java/io/dagger/modules/mymodule/MyModule.java",
    };
    // TODO: also include full sdk reference?
    let reference = await dag
      .currentModule()
      .source()
      .file(`knowledge/${sdk}_sdk.md`)
      .contents();

    reference += `\n\n## Reference snippets:\n\n`;
    for (const snippet in snippets) {
      const code = await daggerDocs
        .file(`${snippets[snippet]}/${sdk}/${snippetSdkPaths[sdk]}`)
        .contents();
      reference += `\n${snippet}:\n<code>\n${code}\n</code>\n`;
    }
    return reference;
  }

  /**
   * Get reference information on writing an example module for a dagger module
   */
  @func()
  async getExamplesReference(): Promise<string> {
    return await dag
      .currentModule()
      .source()
      .file("knowledge/go_examples.md")
      .contents();
  }

  // Helper to get a container that can execute dagger commands on our module
  async daggerCommand(): Promise<Container> {
    let mod = dag
      .container()
      .from("alpine")
      .withExec(["apk", "add", "curl"])
      .withEnvVariable("DAGGER_VERSION", this.daggerVersion)
      .withExec([
        "sh",
        "-c",
        "curl -fsSL https://dl.dagger.io/dagger/install.sh | BIN_DIR=/usr/local/bin sh",
      ])
      .withWorkdir("/mod")
      .withExec(["dagger", "init", "--name", this.name, "--sdk", this.sdk], {
        experimentalPrivilegedNesting: true,
      });
    for (const dep of this.dependencies) {
      const depName = "./" + (await dep.asModule().name());
      mod = mod
        .withDirectory(depName, dep)
        .withExec(["dagger", "install", depName], {
          experimentalPrivilegedNesting: true,
        });
    }
    return mod.withFile(
      await dag.moduleHelper().getSdkMainFile(this.sdk, this.name),
      this.workspace.file(
        await dag.moduleHelper().getSdkMainFile(this.sdk, this.name),
      ),
    );
  }

  trimDaggerError(error: string): string {
    const sep = "ModuleSource.asModule: Module!";
    const parts = error.split(sep);
    if (parts.length > 1) {
      return parts[1];
    }
    return error;
  }
}
