"""
Source Code:  https://github.com/inclusionAI/AWorld/blob/main/mcp_servers

Browser MCP Server

This module provides MCP server functionality for browser automation and interaction.
It handles tasks such as web scraping, form submission, and automated browsing.

Main functions:
- browse_url: Opens a URL and performs specified actions
- submit_form: Fills and submits forms on web pages

{
  "mcpServers": {
    "browser-server": {
      "transport": "SSE",
      "url": "http://localhost:8888/sse"
    }
  }
}

Error: ToolException('Error executing tool browser_use: 
1 validation error for BrowserSession
browser  
Input should be an instance of Browser 
[type=is_instance_of, input_value=BrowserSession(...), 
input_type=BrowserSession]
For further information visit https://errors.pydantic.dev/2.10/v/is_instance_of')

browser=browser.browser instead of browser=browser

"""

import json
import os
import sys
import traceback

from browser_use import Agent
from browser_use.agent.views import AgentHistoryList
from browser_use.browser.browser import Browser, BrowserConfig
from browser_use.browser.context import BrowserContext, BrowserContextConfig
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from mcp.server.fastmcp import FastMCP
from pydantic import Field

# from aworld.logs.util import logger

mcp = FastMCP("browser-server")
browser_system_prompt = """
===== NAVIGATION STRATEGY =====
1. START: Navigate to the most authoritative source for this information
   - For general queries: Use Google with specific search terms
   - For known sources: Go directly to the relevant website

2. EVALUATE: Assess each page methodically
   - Scan headings and highlighted text first
   - Look for data tables, charts, or official statistics
   - Check publication dates for timeliness

3. EXTRACT: Capture exactly what's needed
   - Take screenshots of visual evidence (charts, tables, etc.)
   - Copy precise text that answers the query
   - Note source URLs for citation

4. DOWNLOAD: Save the most relevant file to local path for further processing
   - Save the text if possible for futher text reading and analysis
   - Save the image if possible for futher image reasoning analysis
   - Save the pdf if possible for futher pdf reading and analysis

5. ROBOT DETECTION:
   - If the page is a robot detection page, abort immediately
   - Navigate to the most authoritative source for similar information instead

===== EFFICIENCY GUIDELINES =====
- Use specific search queries with key terms from the task
- Avoid getting distracted by tangential information
- If blocked by paywalls, try archive.org or similar alternatives
- Document each significant finding clearly and concisely

Your goal is to extract precisely the information needed with minimal browsing steps.
"""

load_dotenv()
@mcp.tool(description="Perform browser actions using the browser-use package.")
async def browser_use(
    task: str = Field(description="The task to perform using the browser."),
) -> str:
    """
    Perform browser actions using the browser-use package.
    Args:
        task (str): The task to perform using the browser.
    Returns:
        str: The result of the browser actions.
    """
    browser = Browser(
        config=BrowserConfig(
            headless=False,
            new_context_config=BrowserContextConfig(
                disable_security=True,
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                minimum_wait_page_load_time=10,
                maximum_wait_page_load_time=30,
            ),
        )
    )
    browser_context = BrowserContext(
        # config=BrowserContextConfig(
        #     trace_path=os.getenv("LOG_FILE_PATH") + "/browser_trace.log"
        # ),
        browser=browser.browser,
        # browser=browser,
    )
    agent = Agent(
        task=task,
        llm=ChatOpenAI(
            model=os.getenv("LLM_MODEL_NAME"),
            api_key=os.getenv("LLM_API_KEY"),
            base_url=os.getenv("LLM_BASE_URL"),
            model_name=os.getenv("LLM_MODEL_NAME"),
            # openai_api_base=os.getenv("LLM_BASE_URL"),
            # openai_api_key=os.getenv("LLM_API_KEY"),
            temperature=1.0,
        ),
        browser_context=browser_context,
        browser=browser,
        extend_system_message=browser_system_prompt,
    )
    try:
        browser_execution: AgentHistoryList = await agent.run(max_steps=50)
        if (
            browser_execution is not None
            and browser_execution.is_done()
            and browser_execution.is_successful()
        ):
            exec_trace = browser_execution.extracted_content()
            # logger.info(
            #     ">>> 🌏 Browse Execution Succeed!\n"
            #     f">>> 💡 Result: {json.dumps(exec_trace, ensure_ascii=False, indent=4)}\n"
            #     ">>> 🌏 Browse Execution Succeed!\n"
            # )
            print(f"Result: {json.dumps(exec_trace, ensure_ascii=False, indent=4)}")
            return browser_execution.final_result()
        else:
            return f"Browser execution failed for task: {task}"
    except Exception as e:
        # logger.error(f"Browser execution failed: {traceback.format_exc()}")
        return f"Browser execution failed for task: {task} due to {str(e)}"
    finally:
        await browser.close()
        # logger.info("Browser Closed!")


def main():
    load_dotenv()
    print("Starting Browser MCP Server...", file=sys.stderr)
    print(mcp.custom_route, file=sys.stderr)
    # mcp.run(transport="stdio")
    # ,host="0.0.0.0", port=8080
    # mcp.run(transport="sse",mount_path="/sse")
    mcp.run(transport="sse")
    # 输出路由信息
    # print(mcp.custom_route, file=sys.stderr)


# Make the module callable
def __call__():
    """
    Make the module callable for uvx.
    This function is called when the module is executed directly.
    """
    main()


sys.modules[__name__].__call__ = __call__

# Run the server when the script is executed directly
if __name__ == "__main__":
    main()