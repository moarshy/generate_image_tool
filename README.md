# Generate Image Tool

This is a Naptha tool module for generating images using the Stability API. Tool modules can be run independently or used by agents. 

Naptha [Modules](https://docs.naptha.ai/NapthaModules/overview) are the building blocks of multi-agent applications, which enable them to run across multiple nodes.


## Usage

### Run the Tool

```bash
naptha run tool:generate_image_tool -p "prompt='expansive landscape rolling greens with gargantuan yggdrasil, intricate world-spanning roots towering under a blue alien sky, masterful, ghibli'"
```

### Run an Agent that uses the Tool

The [Generate Image Agent](https://github.com/NapthaAI/generate_image_agent) is an example of an agent that uses the generate image tool. In this case, the generate_image module is set as the default tool in the generate_image_agent/configs/tool_deployments.json file.

```bash
naptha run agent:generate_image_agent -p "prompt='expansive landscape rolling greens with gargantuan yggdrasil, intricate world-spanning roots towering under a blue alien sky, masterful, ghibli'" --tool_node_urls "http://localhost:7001"
```

## Browse other Tool Modules

You can check out other examples of tool modules using the following CLI command with the [Naptha SDK](https://github.com/NapthaAI/naptha-sdk). 

```bash
naptha tools
```

## 🏗 Modifying or creating a new Tool Module

### 🛠 Prerequisites 

#### Install Poetry 

From the official poetry [docs](https://python-poetry.org/docs/#installing-with-the-official-installer):

```bash
curl -sSL https://install.python-poetry.org | python3 -
export PATH="/home/$(whoami)/.local/bin:$PATH"
```

### 🔧 Making Changes to the Module

Before deploying a new or updated module to a Naptha node, you should iterate on improvements with the module locally. 

### Clone and Install the Module

Clone the repo using:

```bash
git clone https://github.com/NapthaAI/<module_name>
cd <module_name>
```

Create a copy of the .env file:

```bash
cp .env.example .env
```

If your module calls others modules (e.g. using Agent(), Tool(), or Environment()), you need to set a ```PRIVATE_KEY``` in the .env file (e.g. this can be the same as the ```PRIVATE_KEY``` you use with the Naptha SDK). If using Stability, make sure to set the ```STABILITY_API_KEY``` environment variable.

You can install the module using:

```bash
poetry install
```

#### Making Changes to the Code

The main place to make changes to the code is in the ```run.py``` file. This is the default entry point that will be used when the module run is initiated. The run function can instantiate a class (e.g. an agent class) or call a function. 

#### Making Changes to the Configs

You can make changes to the configs in the ```configs``` folder. For example:

**MODEL**: If you would like to use a different model, you can change the ```llm_config['config_name']``` in the ```tool_deployments.json``` file (the ```config_name``` must match the ```config_name``` in the ```llm_configs.json``` file). 

## 🧪 Testing the Module

After making changes to the module, testing usually involves the following steps:

1. Test the module locally without the Naptha Node
2. Test the module on a local Naptha Node (with a local Hub)
3. Test the module on a hosted Naptha Node (with the hosted Naptha Hub)

### 🖥️ Test the Module Locally without Node

You can run the module using:

```bash
poetry run python <module_name>/run.py
```

Now you can iterate on the module and commit your changes. When ready, you can push to your GitHub account or IPFS (or both). Make sure to change the remote origin. Also add a new module version number using e.g.:

```bash
git tag v0.1
```

```bash
git push --tags
```

### 🌐 Test the Module on a Local Node (with a Local Hub)

For this step, you will need to:

1. Run your own Naptha Node and Hub. Follow the instructions [here](https://github.com/NapthaAI/node) (still private, please reach out if you'd like access at team@naptha.ai) to run your own Naptha Node and Hub. To run a local Hub, set ```LOCAL_HUB=True``` in the .env file for the NapthaAI/node repository.
2. Install the Naptha SDK using the [instructions here](https://github.com/NapthaAI/naptha-sdk). To use the SDK with your local node and hub, set ```NODE_URL=http://localhost:7001``` and ```HUB_URL=ws://localhost:3001/rpc``` in the .env file for the NapthaAI/naptha-sdk repository.

#### Register the new or updated Tool on a local Hub

```bash
naptha tools tool_name -p "description='Tool description' module_url='ipfs://QmNer9SRKmJPv4Ae3vdVYo6eFjPcyJ8uZ2rRSYd3koT6jg'" 
```

Make sure to replace the placeholder descriptions and URLs with your own. To check that the tool module is registered correctly, you can run ```naptha tools```.

#### Running the Tool on a local Naptha Node

Once the tool is registered on the Hub, you can run it on a local Naptha Node using the Naptha SDK:

```bash
naptha run tool:tool_name -p "tool_name='func', tool_input_data='nice picture of a cat...'" 
```

For troubleshooting, see the Troubleshooting section in NapthaAI/node for checking the logs.

### ☁️ Test the Tool on a hosted Node (with the hosted Naptha Hub)

## 💰 Bounties and Microgrants

Have an idea for a cool tool module to build? Get in touch at team@naptha.ai.
