"""Define agents."""

from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, PromptTemplate

from react_agent.constants import REACT_PROMPT
from react_agent.common.llm import chat_llm, completion_llm
from react_agent.tools import import_tools

def react_agent():
    """Create a ReAct agent."""
    response_format = "agent"
    tools = import_tools(common_tools_kwargs={"response_format": response_format})
    prompt = PromptTemplate.from_template(REACT_PROMPT)
    agent = create_react_agent(completion_llm, tools, prompt, stop_sequence=["Observation:"])
    agent_executor = AgentExecutor(name="ReActAgent", agent=agent, tools=tools, handle_parsing_errors=True)
    return agent_executor