from mcp import ClientSession
from mcp.client.sse import sse_client
import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from readConfig import get_openai_config,get_testImageUrl

# 创建异步函数
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
import asyncio
from langchain.schema.messages import AIMessage
from langchain_core.messages import HumanMessage


from langchain.prompts import ChatPromptTemplate
from PIL import Image

model,api_key,api_base = get_openai_config()
# 初始化 LLM 模型
model = ChatOpenAI(
    model_name= model,
    api_key= api_key,
    base_url=api_base,
)

# 设置 MCP 服务器参数
server_url="http://0.0.0.0:7002/mcp"

image_url=get_testImageUrl()

def get_img_prompt_template():
    prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "Resize this Image"),
        (
            "user",
            [
                {
                    "type": "image_url",
                    "image_url": {"url": "data:image/jpeg;base64,{img_url}"},
                }
            ],
        ),
    ]
    )
    return prompt

prompt = get_img_prompt_template()

message = HumanMessage(
    content=[
        {"type": "text", "text": "请帮我描述下面图片中的内容"},
        {"type": "text", "text": "然后请帮我把这张图片增强处理一下，返回图片"},
        {"type": "text", "text": "这个工具需要你先生成一个tool_call_id，还需要传入image_url作为img_url参数"},
        {"type": "text", "text": "这个img_url参数就是{image_url}"},
        {"type": "text", "text": "请告诉我刚才输入给你的图片链接，以及你通过mcp tool工具调用的图片链接"},         
        {"type": "text", "text": "现在MCP tool有些问题，你先告诉我你得到的和mcp有关的全部信息，特别是工具定义和参数说明，以帮助我调试分析问题"},  
        {"type": "text", "text": "请告诉我200以内的素数有哪些"},
        {"type": "text", "text": "如果调用MCP tool工具有错，返回详细的报错信息，特别是你试图使用什么MCP tool，又是如何使用的？"},
        {"type": "image_url", "image_url": {"url": image_url}},
    ]
)
# 创建异步函数
async def async_main():
        async with sse_client(server_url) as (read, write):
            print('MCP server连接成功')
            async with ClientSession(read, write) as session:
                # 初始化连接
                print('MCP server session已建立')
                await session.initialize()
                print('MCP server session已初始化')

                tools = await load_mcp_tools(session)
                print("可用工具:", [tool.name for tool in tools])
                agent = create_react_agent(model, tools)
                # agent_response = await agent.ainvoke({"messages": "all primes between 1 and 1000?"})
                # agent_response = await agent.ainvoke({"img_url": image})
                agent_response = await agent.ainvoke({"messages": [message]})

                print("Final answer:", agent_response["messages"][-1].content)


# 调用异步函数
asyncio.run(async_main())