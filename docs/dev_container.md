# Visual Studio Code Dev Container

Steps to open the repository in Visual Studio Code dev container:

1. Clone this repository into your local machine and open it in VS Code. Follow [this](https://docs.microsoft.com/en-us/azure/devops/user-guide/code-with-git?view=azure-devops#clone-the-repo-to-your-computer) link for instructions on how to clone a repository.

   > Note: For Windows machines, you can clone this repository into WSL for better performance. To open the cloned repository in VS Code, go to root of the repository on the WSL distribution's command line and type `code .`.

1. Build and open the repository in dev container
   1. Open VS Code Command Palette (`View` > `Command Palette`) and run the command `Remote-Containers: Reopen in Container` to open the code inside the dev container.
   1. The VS Code window will reload and start building the dev container. You will see a progress notification on the bottom right with the option to view the build log. Building the dev container for the first time will take about 10-15 min; opening the dev container after the first successful build will be much quicker.
   1. After the build completes, VS Code will automatically connect to the container. You will see the name of the dev container for the hands on lab displayed in the bottom left.

**NOTE:** If the development machine OS is `Linux`, please add the following line to the `~/.bashrc` or shell specific login files like `~/.zshrc` and log out and log back in to take effect. Open the VS Code again and start from step 2.

```bash
export DOCKER_BUILDKIT=1
export COMPOSE_DOCKER_CLI_BUILD=1
```
