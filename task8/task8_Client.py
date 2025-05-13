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
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from imageToken.imageUrl  import image_to_base64,base64_to_image,imageData_to_base64,open_image

model,api_key,api_base = get_openai_config()
# 初始化 LLM 模型
model = ChatOpenAI(
    model_name= model,
    api_key= api_key,
    base_url=api_base,
)
ServerPath=[r"C:\work\AgentLearn\task8\task8_Server.py"]
# 设置 MCP 服务器参数
server_params = StdioServerParameters(
    # 确保这是正确的 python 解释器
    command="python",
    # 确保这是 server.py 的完整绝对路径
    args=ServerPath,  
)

# image = image_to_base64(r"test.jpg")
# image = open_image("test.jpg")
# image.resize((512, 512* image.height//image.width))
# image = imageData_to_base64(image)
# print(image)
# print(len(image))

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
        # {"type": "text", "text": "请帮我把这张图片缩小一下，返回Base64编码的图片"},
        {"type": "text", "text": "请帮我描述图片内容"},
        # {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_url}"}},
        {"type": "image_url", "image_url": {"url": image_url}},
    ]
)
# 创建异步函数
async def async_main():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await load_mcp_tools(session)
            print("可用工具:", [tool.name for tool in tools])
            # agent = create_react_agent(model=model, tools=tools,prompt=prompt)
            agent = create_react_agent(model, tools)
            # agent_response = await agent.ainvoke({"messages": "all primes between 1 and 1000?"})
            # agent_response = await agent.ainvoke({"img_url": image})
            agent_response = await agent.ainvoke({"messages": [message]})

            print("Final answer:", agent_response["messages"][-1].content)
            # img = base64_to_image(agent_response["messages"][-1].content)
            # img.save("Agentoutput.jpg")


# 调用异步函数
asyncio.run(async_main())