"""Define and import tools."""

import logging

from react_agent.constants import CONFIG
from react_agent.tools.common import CommonTool
from react_agent.tools.math import ComputeSquareTool

logger = logging.getLogger(__name__)


def create_common_tools(**kwargs):
    """Create common tools."""
    logger.info("Creating Common Tools from config.yaml")
    tool_configs = CONFIG.get("tools", [])
    tools = []
    for tool_config in tool_configs:
        tool = CommonTool(**tool_config, **kwargs)
        tools.append(tool)
        logger.info(f"Created {tool_config['name']} tool")
    return tools


def import_tools(all_return_direct: bool = False, common_tools_kwargs: dict = {}):
    """Gather tools."""
    base_tools = [ComputeSquareTool()]
    common_tools = create_common_tools(**common_tools_kwargs)
    tools = base_tools + common_tools
    if all_return_direct:
        for tool in tools:
            tool.return_direct = True
    return tools