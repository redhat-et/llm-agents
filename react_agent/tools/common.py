import json
import logging
import re
from typing import Optional, Type

import requests
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field

from react_agent.constants import ERROR_MESSAGE

logger = logging.getLogger(__name__)


# From https://stackoverflow.com/questions/2352181/how-to-use-a-dot-to-access-members-of-dictionary
class DotDict(dict):
    """Use dot notation to access dictionary attributes."""

    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

class CommonToolInput(BaseModel):
    """Tool input structure."""

    prompt: str = Field(description="should be a prompt for an AI")

class CommonTool(BaseTool):
    """Tool for interacting with external API instances."""

    name: str = Field(description="Tool name")
    description: str = Field(description="Tool description")
    args_schema: Type[BaseModel] = CommonToolInput
    response_format: str
    url: str
    config: dict

    # TODO: Implement validation

    def request(self, prompt: str):
        """Send a request to the API endpoint."""
        method = self.config["method"]
        headers = self.config["headers"]
        body = self.config["body"].copy()
        for key, value in body.items():
            if isinstance(value, str) and re.match(r"{{prompt}}", value, flags=re.MULTILINE):
                body[key] = re.sub(r"{{prompt}}", prompt, value, flags=re.MULTILINE)
        url_response = requests.request(method=method, url=self.url, headers=headers, json=body)
        if str(url_response.status_code)[0] != "2":
            url_response.raise_for_status()
        # Parse the response
        url_response_json = url_response.json()
        url_response_dotdict = DotDict(url_response_json)

        # Get the answer
        response_loc = self.config["responseParser"]
        response_loc = ".".join(response_loc.split(".")[1:]) if response_loc.startswith("json") else response_loc
        response = url_response_dotdict.__getattr__(response_loc).strip()

        # Create metadata
        metadata = {}
        metadata_fields = self.config.get("responseMetadata", None)
        if metadata_fields:
            for field in metadata_fields:
                name = field["name"]
                loc = field["loc"]
                loc = ".".join(loc.split(".")[1:]) if loc.startswith("json") else loc
                metadata[name] = url_response_dotdict.__getattr__(loc)
        return response, metadata

    def format_response(self, response: str, metadata: dict):
        """Format the response."""
        response_format = self.config["responseFormat"][self.response_format]
        if self.response_format == "json":
            formatted_response = {}
            available_fields = {"response": response} | metadata
            for key in response_format:
                value = available_fields.get(key, None)
                formatted_response[key] = value
            formatted_response = json.dumps(formatted_response)
        else:
            formatted_response = response_format
            available_fields = {"response": response} | metadata
            for key, value in available_fields.items():
                if isinstance(value, dict):
                    value = json.dumps(value)
                else:
                    value = str(value)
                formatted_response = formatted_response.replace("{{" + key + "}}", value)

        return formatted_response

    def _run(self, prompt: str, run_manager: Optional[CallbackManagerForToolRun] = None):
        """Use the tool."""
        try:
            response, metadata = self.request(prompt=prompt)
            return self.format_response(response, metadata)
        except Exception as e:
            logger.error(e)
            raise e  # TODO: remove
            return ERROR_MESSAGE

    async def _arun(self, prompt: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("Tool does not support async")