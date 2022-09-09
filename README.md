CMYK to RGB color space mapping

### 1. Set up environment variables

Set up the following environment variable on your development PC:

| Environment Variable | Description |
| ----- | ----- |
| SIM_WORKSPACE | The workspace ID from [your workspace details](https://docs.microsoft.com/en-us/bonsai/cookbook/get-workspace-info). |
| SIM_ACCESS_KEY | The access key from [your workspace details](https://docs.microsoft.com/en-us/bonsai/cookbook/get-workspace-info). |

Make sure those environment variables have been applied in the command window that you use for the next steps.

### 2. Set up Python environment

Set up your python environment as described in the [Bonsai CLI Get started docs](https://docs.microsoft.com/en-us/bonsai/cli).
Then install the Python requirements of this sample by:

```
pip install -r requirements.txt
```

### 3. Connect local instance of the simulator

Run the simulator locally by:

```
python main.py
```

The output should say `Registered simulator` followed by--every several seconds--a line saying `Last Event: Idle`.

> NOTE: The next step uses Bonsai CLI commands.
> If you prefer, these opererations can also be performed using your [Bonsai worspace](https://preview.bons.ai/) GUI as described in [Link an unmanaged simulator to Bonsai](https://docs.microsoft.com/en-us/bonsai/guides/run-a-local-sim?tabs=bash%2Ctest-with-ui&pivots=sim-lang-python).

While main.py continues to run, open a new commmand window and use the Bonsai CLI to create a Bonsai brain and start training by:

```
bonsai brain create -n simple-adder-brain
bonsai brain version update-inkling -f machine_teacher.ink -n simple-adder-brain
bonsai brain version start-training -n simple-adder-brain
bonsai simulator unmanaged connect --simulator-name simple-adder-sim -a Train -b simple-adder-brain -c Concept
```

The output should say `Simulators Connected: 1`. After a minute or so, you should see lots of activity in the console window that
is running main.py and if you open your [Bonsai worspace](https://preview.bons.ai/) you should see that the brain named simple-adder-brain
is running training episodes. We'll complete training in a faster way in the next step, so for now you can manually stop training by:

```
bonsai brain version stop-training -n simple-adder-brain
```

Press Ctrl+C to stop the simulator running main.py in your first console window.

### 4. Build the simulator package and scale training using the cloud

> For this step, you must have Docker installed on your local machine. The community edition of Docker is available for
> [Windows](https://docs.docker.com/docker-for-windows/install), [Linux](https://docs.docker.com/engine/install), and
> [MacOS](https://docs.docker.com/docker-for-mac/install).

Build a Docker container image and push it to your registry.
In the following commands, `<SUBSCRIPTION>` and `<WORKSPACE_ACR_PATH>` should be replaced with
[your workspace details](https://docs.microsoft.com/en-us/bonsai/cookbook/get-workspace-info):

```
docker build -t simple-adder-container:latest -f Dockerfile .
docker tag simple-adder-container:latest <WORKSPACE_ACR_PATH>/simple-adder-container:latest
az acr login --subscription <SUBSCRIPTION> --name <WORKSPACE_ACR_PATH>
docker push <WORKSPACE_ACR_PATH>/simple-adder-container:latest
```

> NOTE: The next step uses Bonsai CLI commands.
> If you prefer, these opererations can also be performed using your [Bonsai worspace](https://preview.bons.ai/) GUI as described
> in [Add a training simulator to your Bonsai workspace](https://docs.microsoft.com/en-us/bonsai/guides/add-simulator?tabs=add-cli%2Ctrain-inkling&pivots=sim-platform-other).

Creating a Bonsai simulator package and running training with it by:

```
bonsai simulator package container create -n simple-adder-pkg -u <WORKSPACE_ACR_PATH>/simple-adder-container:latest --max-instance-count 25 -r 1 -m 1 -p Linux
bonsai brain version start-training -n simple-adder-brain --simulator-package-name simple-adder-pkg
```

Next, open your [Bonsai worspace](https://preview.bons.ai/) and you should see your simple-adder-brain brain is running training.
If you look in the Train tab, after a few minutes, you will see that simulators have started up and episodes are being executed.
After approximately 200,000 iterations you should see in the training graph shows 100% goal satisfaction and 100% success rate.
You can stop the training at this point or let training continue to run. It will eventually stop when it can no longer find improvements
to reach the goal in a more optimal fashion.



## Contributing

This project welcomes contributions and suggestions.  Most contributions require you to agree to a
Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us
the rights to use your contribution. For details, visit https://cla.opensource.microsoft.com.

When you submit a pull request, a CLA bot will automatically determine whether you need to provide
a CLA and decorate the PR appropriately (e.g., status check, comment). Simply follow the instructions
provided by the bot. You will only need to do this once across all repos using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.

## Trademarks

This project may contain trademarks or logos for projects, products, or services. Authorized use of Microsoft 
trademarks or logos is subject to and must follow 
[Microsoft's Trademark & Brand Guidelines](https://www.microsoft.com/en-us/legal/intellectualproperty/trademarks/usage/general).
Use of Microsoft trademarks or logos in modified versions of this project must not cause confusion or imply Microsoft sponsorship.
Any use of third-party trademarks or logos are subject to those third-party's policies.
