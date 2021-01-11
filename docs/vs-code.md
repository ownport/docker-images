# How to use docker images/containers with VS Code

There are short notes from https://code.visualstudio.com/docs/ site. For more detail information please visit VS Code docs web site.

## How it works

The remote container extension uses the files in the `.devcontainer` folder, namely `devcontainer.json`, and an optional `Dockerfile` or `docker-compose.yml`, to create your dev containers.

First your image is built from the supplied Docker file or image name. Then a container is created and started using some of the settings in the `devcontainer.json`. Finally your Visual Studio Code environment is installed and configured again according to settings in the `devcontainer.json`.

Once all of this is done, your local copy of Visual Studio Code connects to the Visual Studio Code Server running inside of your new dev container.

## Create a devcontainer.json file

VS Code's container configuration is stored in a `devcontainer.json` file. You can also specify any extensions to install once the container is running or post-create commands to prepare the environment. The dev container configuration is either located under `.devcontainer/devcontainer.json` or stored as a `.devcontainer.json` file (note the dot-prefix) in the root of your project.

You can use any image, Dockerfile, or set of Docker Compose files as a starting point. Here is a simple example that uses one of the pre-built VS Code Development Container images:
```json
{
  "image": "mcr.microsoft.com/vscode/devcontainers/typescript-node:0-12",
  "forwardPorts": [3000],
  "extensions": ["dbaeumer.vscode-eslint"]
}
```

Selecting the Remote-Containers: Add Development Container Configuration Files... command from the Command Palette (F1) will add the needed files to your project as a starting point, which you can further customize for your needs. The command lets you pick a pre-defined container configuration from a list based on your folder's contents, reuse an existing Dockerfile, or reuse an existing Docker Compose file.

## References

- https://code.visualstudio.com/docs/remote/containers-tutorial
- https://code.visualstudio.com/docs/remote/containers
- https://code.visualstudio.com/docs/remote/devcontainerjson-reference
