# OpenShift Deployment Instructions

To deploy the ReAct agent on an OpenShift cluster, you can follow the below instructions.

## Prerequisites

- OpenShift CLI (`oc`) installed and configured
- (**Optional**) `kubectl` and `kustomize` installed and configured

## Deployment Instructions

### Step 1: Clone the Repository

```sh
git clone git@github.com:redhat-et/llm-agents.git
cd llm-agents/react_agent
```

### Step 2: Deploy the ReAct Agent API Server

The agent API server is responsible for handling requests and interacting with the LLM. It exposes endpoints for different functionalities of the tool-based agent. The API server processes incoming requests, sends them to the appropriate tools or models, and returns the results to the clients. This deployment step sets up the necessary backend infrastructure for the ReAct agent.


```sh
oc apply -f openshift/deployment.yaml
```

```sh
oc apply -f openshift/service.yaml
```

```sh
oc apply -f openshift/route.yaml
```

```sh
oc apply -f openshift/configmap.yaml
```

### Containerfile

The Containerfiles used to build the deployment images can be found [here](https://github.com/redhat-et/llm-agents/blob/main/react-agent-Containerfile)
