# 🤖 **LLM Agent Hub**

Welcome to the **LLM Agent Hub**! This repository hosts all resources, research, code, and experiments related to building and deploying **LLM-powered agents** such as developing autonomous agents, exploring routing strategies, or integrating function-calling capabilities.

---

## **Contents**
In this repository you will find details about LLM agents, example code for setting up an agent, example code for deploying it in cloud based environments, use cases for LLM agents and other insights/results from our experiments.

- **📂 Agent Types**  
  - ReAct Agents (Reason + Action Agents)  
  - Router-Based Agents  
  - Function-Calling Agents  
  - LangGraph-based Agents  

- **🔧 Tools and Integrations**  
  - API Integration Examples (e.g., OpenAI, LangChain)  
  - External Tools (Databases, Search Engines, etc.)  
  - Frameworks for Agent Development  

- **📝 Research and Resources**  
  - Use Cases and Real-World Examples 
  - Results, insights and findings

- **📦 Code Samples and Projects**  
  - Example code scripts for implementing LLM agents, tools, function calling
  - Example deployment setup using Podman/OpenShift 

---

## 💡 **What Are LLM Agents?**
LLM agents combine the power of large language models (LLMs) with external tools, APIs, and logic-based reasoning. They go beyond simple text generation, using **actions and decisions** to interact with external environments, solve problems, and automate workflows. 

LLM agents can operate across a wide range of scenarios, from automating tasks and retrieving information to dynamically interacting with users or systems in real-time. Depending on their design, they may follow predefined workflows, reason through complex decisions (as in ReAct agents), or call external functions to enhance their capabilities. This flexibility makes them suitable for various use cases, such as virtual assistants, product recommendations, process automation, and troubleshooting support.

### Components of an LLM Agent

The main components of an LLM-powered agent application are:

- **Agent** - Agent is the main controller which works with various components to manage tasks.
- **Tool** - Tools are external functions the agent can use to complete specific tasks such as a web search function, weather prediction function, calculator function etc
- **Memory** - Split into short-term memory and long-term memory, the agent uses short-term memory to keep track of what’s happening in the current conversation or task. Long-term memory helps the agent remember past interactions or knowledge over a longer period
- **Planning component** - This is where the agent really thinks through complex tasks. You’ll notice elements like reflection, self-criticism, and chain of thought reasoning. These help the agent break tasks into smaller steps and plan how to complete them effectively
- **LLM** -  An LLM as the computational engine which takes in the prompt—that’s the input from the user—and processes it. The agent uses the LLM to make sense of instructions and generate responses

<img width="544" alt="Screenshot 2024-10-24 at 10 47 37 AM" src="https://github.com/user-attachments/assets/9bf548fa-aead-4018-9f2d-581a612b1e80">

### Types of LLM Agents

LLM agents come in various forms, each designed to address different types of tasks and interactions.

- **Router-based agents** - direct queries to the appropriate tools or models by dynamically selecting the best path based on the input, ensuring efficient task execution 
- **ReAct agents** - combine reasoning and action, using intermediate thought steps to analyze problems, decide on the next course of action, and interact with tools iteratively
- **LangGraph with ReAct** - extends the capabilities of ReAct agents further by structuring workflows as decision trees or graphs, enabling complex reasoning paths with multiple steps or conditions, enhancing problem-solving through both logic and sequential actions
- **Function calling agents** - leverage LLMs that have the ability to trigger external functions, such as API calls, databases, or other services, expanding their capabilities beyond text generation eg: [granite-20b-functioncalling](ibm-granite/granite-20b-functioncalling)

---


