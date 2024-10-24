import logging
import time
from typing import Optional, Type

from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


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
        time.sleep(1)  # TODO: Remove this
        return float(number) ** 2

    async def _arun(self, number: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("Tool does not support async")