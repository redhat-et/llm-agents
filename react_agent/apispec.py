from typing import Optional

from pydantic import BaseModel


class ReActRequest(BaseModel):
    """Request for ReAct endpoint."""

    prompt: str
    tools: list[str] = []


class ReActResponse(BaseModel):
    """Response for ReAct endpoint."""

    answer: str | dict
    tools_used: list[str] = []