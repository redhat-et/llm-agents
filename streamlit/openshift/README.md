# OpenShift Deployment Instructions

To deploy a Streamlit UI on OpenShift, you can follow the instructions below.

## Pre-Requisites

- OpenShift CLI (`oc`) installed and configured
- (**Optional**) `kubectl` and `kustomize` installed and configured

## Deployment Instructions

### Step 1: Clone the Repository

```sh
git clone git@github.com:redhat-et/llm-agents.git
cd llm-agents/streamlit
```

### Step 2: Login to your OpenShift/Kubernetes cluster

```sh
oc login <your cluster endpoint>
```

Select the project namespace where you would like to deploy the application.

```sh
oc project <your project/namespace name>
```

### Step 3: Deploy the Streamlit app

Streamlit is a UI application that serves as the front-end interface for interacting with a LLM application. Users can input queries into the webapp, which sends these queries to the agent API server. The agent API server processes the queries, interacts with the underlying tools or models, and sends the responses back to the webapp. The webapp then displays these responses to the user. This deployment step sets up the user interface for interacting with the tool-based agents.

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

### Step 4: Accessing the Streamlit app

You can now launch the Streamlit app through the route created. To retrieve the route URL to access the app:

```sh
oc get route streamlit-route -n kubecon-agent-demo
```

### Containerfile

The Containerfiles used to build the deployment images can be found [here](https://github.com/redhat-et/llm-agents/blob/main/streamlit-Containerfile).
