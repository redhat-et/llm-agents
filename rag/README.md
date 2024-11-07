# Steps to create the RAG tool

This readme file documents two steps:
1) Deploy a standalone Milvus vector database and populate it with sample documents that can be found in the `rag/docs` folder
2) Deploy a RAG API service that can be used as a tool by the Agent

## 1. [Milvus](https://milvus.io/docs/) Deployment and [pymilvus](https://pymilvus.readthedocs.io/) SDK Usage

This guide explains how to deploy Milvus using Kubernetes (specifically OpenShift), connect to it using the `pymilvus` SDK, and run operations on Milvus through a Jupyter Notebook.

### Prerequisites

1. **Kubernetes Cluster**: Ensure you have access to a Kubernetes cluster (e.g., OpenShift).
2. **kubectl/oc CLI**: Command-line interface to manage Kubernetes/OpenShift resources.

### Deployment Steps

#### 1. Apply Milvus Deployment YAML with the following command:

   ```bash
   kubectl apply -f vector_db/standalone_milvus.yaml
   ```

#### 2. Connecting to Milvus with pymilvus

#### Example Notebook Code to Populate a Collection

1. Open Jupyter Notebook `vector_db/vector_db_insert.ipynb` and add the Milvus host from step 1.

2. Run all the notebook cells including cells that embed the markdown [documents](./docs) and insert vectors into the Milvus collection. 

## RAG tool: Uvicorn FastAPI Deployment on OpenShift

This guide provides step-by-step instructions to build a container image for a `uvicorn` FastAPI application to expose the RAG service, push it to a container registry (Quay.io) and deploy it on OpenShift.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) or [Podman](https://podman.io/getting-started/installation) installed locally.
- An OpenShift cluster and access to it.
- An account on [Quay.io](https://quay.io/) or any other container registry.
- A `requirements.txt` file with dependencies and a `app.py` file containing the FastAPI app.

## 1. Building the Container Image

### Build the Container Image

Build the `rag/Containerfile` Container image using `docker` or `podman`:

```bash
podman build --platform linux/amd64 -t your-image-name -f Containerfile . # If using Mac OS otherwise remove --platform flag
```

## 2. Pushing the Image to Quay.io

### Push the Image
Login to Quay.io and:

```bash
podman push quay.io/your-username/your-repo:latest
```

## 3. Deploying to OpenShift

Create a deployment configuration like `rag/rag_tool_service.yaml` in OpenShift to deploy your FastAPI app using the pushed image.

### Apply the Deployment and other resources

Deploy the application to OpenShift by applying the YAML file:

```bash
oc apply -f rag_tool_service.yaml
```

### Access the Application

1. Use the service location or route created in the previous file as the tool endpoint in the [config.yaml](../config.yaml) that the agent will use. 