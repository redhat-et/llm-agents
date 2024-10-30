from typing import Any, List, Mapping, Optional

import httpx
from langchain.callbacks.manager import CallbackManagerForLLMRun
from langchain.llms.base import LLM
from langchain_core.messages import HumanMessage
from langchain_openai.chat_models import ChatOpenAI

from react_agent.constants import OPENAI_IGNORE_SSL, OPENAI_MODEL, OPENAI_URI


class CustomOpenAI(LLM):
    """Class to define interaction with the hosted OpenAI instance at a specified URI without SSL verification."""

    base_url: str
    model: str
    api_key: str
    http_client: httpx.Client = None
    temperature: float = 0.8

    @property
    def _llm_type(self) -> str:
        return "custom"

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ):
        # Create the request
        llm = ChatOpenAI(
            base_url=self.base_url, model=self.model, api_key=self.api_key, http_client=self.http_client, temperature=self.temperature
        )
        request = [HumanMessage(content=prompt)]
        response = llm.invoke(request, stop=stop, **kwargs).content
        return response

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """Get the identifying parameters."""
        return {"base_url": self.base_url, "model": self.model}


verify = False if OPENAI_IGNORE_SSL else True
http_client = httpx.Client(verify=verify)

chat_llm = ChatOpenAI(base_url=OPENAI_URI, model=OPENAI_MODEL, http_client=http_client, temperature=0, api_key="NONE")
completion_llm = CustomOpenAI(base_url=OPENAI_URI, model=OPENAI_MODEL, http_client=http_client, temperature=0, api_key="NONE")