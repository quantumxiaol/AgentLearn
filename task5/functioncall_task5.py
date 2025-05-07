from openai import OpenAI as OpenAIClient
import openai
import yaml
import os
import sys



sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from MCPtool.testtool import getPrimeinNumN

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from readConfig import get_openai_config


functions = [
    {
        "name": "getPrimeinNumN",
        "description": "获取小于等于给定数字的所有质数",
        "parameters": {
            "type": "object",
            "properties": {
                "num": {
                    "type": "integer",
                    "description": "要查询的上限数字"
                }
            },
            "required": ["num"],
        },
    }
]
def call_gpt_with_function(query):
    model,api_key,api_base = get_openai_config()
    client = OpenAIClient(api_key=api_key, base_url=api_base)

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": query}
        ],
        functions=functions,
        function_call="auto"  # 自动决定是否调用函数
    )
    # print(f"raw respond",response)
    message = response.choices[0].message
    
    # 判断是否调用了函数
    called_function = False
    result = ""

    # 判断是否有 function_call
    if message.function_call:
        function_name = message.function_call.name
        arguments = eval(message.function_call.arguments)  # JSON string -> dict

        if function_name == "getPrimeinNumN":
            called_function = True
            result = getPrimeinNumN(arguments["num"])
        else:
            result = f"未知函数 {function_name} 被调用"
    else:
        result = message.content
    return called_function, result

def call_gpt_with_no_tool(query):
    model,api_key,api_base = get_openai_config()
    client = OpenAIClient(api_key=api_key, base_url=api_base)

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": query}
        ],
    )
    return response.choices[0].message

if __name__ == "__main__":
    
    query = "请告诉我1000内的所有质数。"
    called, output = call_gpt_with_function(query)

    if called:
        print("成功调用函数,结果是：", output)
    else:
        print("调用函数失败，回答是：", output)
    
    result_no_tool = call_gpt_with_no_tool(query)
    print("没有调用函数，回答是：", result_no_tool.content)

    

