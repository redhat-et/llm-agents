# Instructions

## Pre-Requisites

In order to run the Streamlit UI locally on your laptop, the following must be installed:
* `poetry`
* `oc` (optional)

**Initial Steps**

* Clone the repository to your local system via `git clone git@github.com:redhat-et/llm-agents.git`

* Change directory to the project `cd llm-agents`

* Install the project dependencies `poetry install`

## Local Usage

To run the setup locally, follow the steps below:

1. Change directory to the streamlit folder `cd streamlit`

2. In a new terminal, run `poetry run streamlit run intro.py` to spin up the Stremalit UI.

3. Navigate to the URL where the Streamlit UI app is running in your browser i.e it would be running at `http://localhost:8500`

4. Congrats! You now have a Streamlit UI app running locally! 🥳 You can now interact with the LLM agent by providing your questions/inputs through the UI and view the outputs/responses being generated.


## OpenShift Deployment
If you would like to deploy the Streamlit application on an OpenShift/Kubernetes cluster you can find the documentation and resources in [streamlit/openshift](https://github.com/redhat-et/llm-agents/tree/main/streamlit/openshift).
