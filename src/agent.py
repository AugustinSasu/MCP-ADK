import os
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StreamableHTTPConnectionParams
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from config.get_config import cfg
from src.prompts import *

LLM_MODEL = cfg.MODEL.NAME

root_agent = Agent(
    model=LiteLlm(model='ollama_chat/' + LLM_MODEL),
    name="system_administration",
    description=(
        description
    ),
    instruction=instruction,
    tools=[
        MCPToolset(
            connection_params=StreamableHTTPConnectionParams(
                url=os.getenv("MCP_SERVER_URL", "http://localhost:8080/mcp")
            )
        )
    ],
)
