"""
check mcp server and list tools

python test_mcp_client.py -u "http://127.0.0.1:1234/mcp" \
    -q "can you tell me this website is about?url http://www.inaturephysics.top"
"""

import asyncio
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from mcp.client.sse import sse_client
from langchain_openai import ChatOpenAI
from mcp import ClientSession
import argparse
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
api_base = os.getenv("OPENAI_API_BASE_URL")

model = ChatOpenAI(
    model_name='qwen-max-latest',
    api_key=api_key,
    base_url=api_base,
    temperature=0.7,
    )


server_url="http://127.0.0.1:1234/mcp"
async def async_main(server_url:str="",question:str=""):
        async with sse_client(server_url) as (read, write):
            print('MCP server连接成功')
            async with ClientSession(read, write) as session:
                # 初始化连接
                print('MCP server session已建立')
                await session.initialize()
                print('MCP server session已初始化')

                tools = await load_mcp_tools(session)
                print("可用工具:", [tool.name for tool in tools])
                
                if question != "":
                    agent = create_react_agent(model, tools)
                    agent_response = await agent.ainvoke({"messages": [question]})
                    print("Final answer:", agent_response["messages"][-1].content)
                    result = extract_tool_info(agent_response)

                    print(" Final Answer:\n", result["final_answer"])
                    print("\n Tool Calls:", result["tool_calls"])
                    print("\n Tool Results:", result["tool_results"])



def extract_tool_info(agent_response):
    tool_calls = []
    tool_results = []

    for msg in agent_response["messages"]:
        # 判断消息类型
        if isinstance(msg, AIMessage) and hasattr(msg, "tool_calls"):
            for tool_call in msg.tool_calls:
                tool_calls.append({
                    "name": tool_call["name"],
                    "arguments": tool_call["args"]
                })

        elif isinstance(msg, ToolMessage):
            tool_results.append({
                "id": msg.tool_call_id,
                "name": msg.name,
                "content": msg.content,
                "status": msg.status
            })

    # 提取最终回答
    final_answer = None
    for msg in reversed(agent_response["messages"]):
        if isinstance(msg, AIMessage):
            final_answer = msg.content
            break

    return {
        "tool_calls": tool_calls,
        "tool_results": tool_results,
        "final_answer": final_answer
    }

if __name__ == "__main__":
    arg = argparse.ArgumentParser()
    arg.add_argument("--base_url",
                     "-u", 
                     type=str, 
                     default="http://127.0.0.1:8888/sse",
                     help="MCP server base url"
                     )
    arg.add_argument("--question",
                    "-q", 
                    type=str, 
                    default="",
                    help="question to ask agent, None for donot ask"
                    )
    arg=arg.parse_args()
    asyncio.run(async_main(server_url=arg.base_url,question=arg.question))
