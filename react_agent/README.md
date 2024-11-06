# Instructions

## Pre-Requisites

In order to run the ReAct agent setup locally on your laptop, the following must be installed:
* `poetry`
* `oc` (optional)
* [Ollama](https://ollama.com/)

**Initial Steps**

* Clone the repository to your local system via `git clone git@github.com:redhat-et/llm-agents.git`

* Change directory to the project `cd llm-agents`

* Install the project dependencies `poetry install`

## Local Usage

To run the setup locally, follow the steps below:

1. Create a copy of the `sample.env` and rename it as `.env`, then fill in any environment variables
    * The `sample.env` is configured to use Ollama by default, so if you are using that as your LLM provider you don't need to change anything after copying. If you want to use any other LLM then you will need to update `OPENAI_URI` with the model serving endpoint.

2. The `config.yaml` provided in the repo has an example for a dummy `Constitution Tool`. Update the `config.yaml` with information for any tool/API endpoints you'd like the ReAct agent to interact with.

***NOTE**: If you do not wish to use any APIs, remove the "tools" header completely.*

3. If using Ollama, ensure that the model specified in `OPENAI_MODEL` has been pulled into your Ollama instance with `ollama pull <model>`. You can view all the models available in your Ollama instance by running `ollama list` and ensure that the model name in `OPENAI_MODEL` is the same as the ones listed. 

4. Run `ollama serve`. If you get an error like "Port 11434 already in use" then Ollama is running and you can move to the next step. 

5. In a new terminal, run `poetry run mlflow server` to spin up a local [MLFlow](https://mlflow.org/) tracking server. MlFlow is an open source tool for managing the Machine Learning Lifecycle and we are using it to log the traces/outputs of the LLM agent application. Update the `.env` by setting: a) `MLFLOW_TRACKING_URI` to the local server URL, b) `MLFLOW_TRACKING_TOKEN` can be commented out if using a local instance, c) `MLFLOW_EXPERIMENT_NAME` to your given experiment name. If you wish to use your own hosted MLFlow deployment, ensure to update the `.env` with their respective values. Navigate to the MLFlow URL to view the MLFlow UI and you will see the outputs being logged under the experiment name `ReAct Agent` -> click on the `Traces` tab.

6. If you wish to deploy your own MLFlow application on an OpenShift/Kubernetes cluster, you can view the GitHub repo [here](https://github.com/redhat-et/mlflow-openshift). This repo contains all the code and documentation neded for setting up the MLFlow application.

7. In a new terminal, run `poetry run python react_agent/api.py` to spin up the agent API server.

8. Congrats! You now have a ReAct agent server running locally! 🥳 If you would like to setup a simple UI to interact with the agent server you can find more details on setting up a Streamlit UI application [here](https://github.com/redhat-et/llm-agents/tree/main/streamlit/README.md).

## Adding Tools for the ReAct agent

There are two ways you can add tools to the ReAct agent's toolbelt. 
Please note that for any of these tools, currently only a single input and a single output is supported.
We may add support for structured inputs in the future.

### Option 1: Custom Python Tool (Easiest)
To create a custom Python tool, open `react_agent/tools`.
Here you will see a few different categories of tools already defined.
In the `math.py` file, you'll see the most basic definition of a tool called `ComputeSquareTool`, which computes the square of a number.
You can use this tool as an example for your tool.

```python
from typing import Optional, Type

from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field

class ComputeSquareInput(BaseModel):
    """Compute square tool input structure."""

    number: int = Field(description="number to square")


class ComputeSquareTool(BaseTool):
    """Tool for computing the square of a number."""

    name: str = "compute_square_tool"
    description: str = "Compute the square of a number"
    args_schema: Type[BaseModel] = ComputeSquareInput

    def _run(self, number: str, run_manager: Optional[CallbackManagerForToolRun] = None):
        """Use the tool."""
        return float(number) ** 2

    async def _arun(self, number: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("Tool does not support async")
```
The `name` and `description` of the tool are provided to the LLM when it is invoked and describes what the tool is and what it can be used for.

The `args_schema` describes the inputs the tool expects from the LLM and should be a pydantic class like the `ComputeSquareToolInput`.
For the agents we've defined, only a single input can be passed to the tool.
There are other agents that can support structured inputs (multi-input) but the ones in this PoC do not support that.

The execution of the tool happens in the `_run` method.
The `_run` method should take the input you described in your `args_schema` as a string and return a value that the agent can use to make its next decision.
Values returned by the tool will be converted to a string before being used by the agent.

### Option 2: Add an API
If you have a running API (like a websearch API), you can provide it as a tool to the ReAct agent.
Currently this only supports APIs with JSON inputs and outputs.
We have provided a sample `config.yaml` file, you can replace it with the config for your tool.
You need the following fields in any tools you define (unless it says "Optional").

```yaml
tools:
  - name: "constitution_tool" # A unique name for your tool
    description: "Answers questions about the U.S. Constitution." # A sentence or two describing the purpose of your tool
    url: "https://www.my.app/v1/completions" # URL to your API endpoint
    config:
      method: 'POST' # Type of request (POST, GET, etc)
      headers: # Headers to send with the request
        'Content-Type': 'application/json' # Content type must be application/json
        'Authorization': 'Basic 12345' # Optional: Authorization header (base64 encoded)
      body: # Key value pairs to send to the endpoint
        prompt: '{{prompt}}' # The agent's prompt to the tool will be injected anywhere a {{prompt}} is present
        other-key: 'constant-value' # Optional: Any other key-value pairs to send
      responseParser: 'json.answer' # Path to the answer to return to the agent
      responseMetadata: # Optional: Any metadata in the response to capture for use in responseFormat
        - name: 'sources' # Metadata name
          loc: 'json.sources' # Metadata path in the response
      responseFormat: # Formats to provide the response from the tool to the agent, must have agent and json keys
        agent: '{{response}}' # Response to give to the ReAct agent, the response parsed with the responseParser will be injected anywhere a {{response}} is present
        json: # Response to give to the Router agent, which will in turn be given to the user
          - "response" # The response parsed with responseParser
          - "sources" # Optional: any additional keys to return. Must match one of the name fields in responseMetadata
    examples: # Optional: Not implemented, provide some example questions your tool can answer
      - "What is the definition of a citizen in the U.S. Constitution?"
      - "What article describes the power of the judiciary branch?"
```

## OpenShift Deployment
If you would like to deploy the LLM agent application on an OpenShift/Kubernetes cluster you can find the documentation and resources in [react-agent/openshift](https://github.com/redhat-et/llm-agents/tree/main/react_agent/openshift).
