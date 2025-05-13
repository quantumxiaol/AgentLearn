import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from readConfig import get_openai_config

# 创建异步函数
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
import asyncio
from langchain.schema.messages import AIMessage

model,api_key,api_base = get_openai_config()
# 初始化 LLM 模型
model = ChatOpenAI(
    model_name= model,
    api_key= api_key,
    base_url=api_base,
)
ServerPath=[r"C:\work\AgentLearn\task7\task7_mcpServer.py"]
# 设置 MCP 服务器参数
server_params = StdioServerParameters(
    # 确保这是正确的 python 解释器
    command="python",
    # 确保这是 server.py 的完整绝对路径
    args=ServerPath,  
)


# 创建异步函数
async def async_main():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await load_mcp_tools(session)
            print("可用工具:", [tool.name for tool in tools])
            agent = create_react_agent(model, tools)
            # agent_response = await agent.ainvoke({"messages": "all primes between 1 and 1000?"})
            agent_response = await agent.ainvoke({"messages": "1000以内的质数有哪些?"})
            print("Final answer:", agent_response["messages"][-1].content)


# 调用异步函数
asyncio.run(async_main())