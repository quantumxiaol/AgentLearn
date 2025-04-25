from langchain.prompts import PromptTemplate
from langchain.prompts import ChatPromptTemplate
from langchain_community.llms import GPT4All
from langchain_openai import OpenAI, ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain.chains import LLMChain
from typing import Optional
from langchain_core.pydantic_v1 import BaseModel, Field
import yaml
import os
import sys
import json
import re

# 结构化输出 Structured Output
# LLMs 能够生成任意文本。这使得模型能够对各种输入做出适当的响应，
# 但在某些使用场景下，将 LLM 的输出限制为特定格式或结构会更有用。这就是所谓的结构化输出。
# structured_llm = llm.with_structured_output(Novel)
class Novel(BaseModel):
    """要告诉用户的短篇小说。"""

    occurrence_time: str = Field(description="故事发生的时间")
    place: str = Field(description="故事发生的地点")
    person: str = Field(description="涉及的人物")
    cause: str = Field(description="事情的起因")
    process: str = Field(description="事情的经过")
    result: str = Field(description="事情的结果")
    novel: str = Field(description="小说正文")


def clean_json_content(json_content):
    """
    清理 JSON 内容中的非法字符。
    """
    # 移除所有不可见的控制字符（除了制表符、换行符和回车符）
    json_content = re.sub(r'[\x00-\x08\x0b-\x0c\x0e-\x1f]', '', json_content)
    return json_content
def parse_json_response(response_content):
    """
    解析模型返回的内容，支持 Markdown 样式的 JSON 和严格的 JSON。
    """
    # 去掉首尾空白字符
    response_content = response_content.strip()

    # 检查是否是严格的 JSON 格式    
    response_content = clean_json_content(response_content)


    # 判断是否是 Markdown 样式的 JSON（以 ```json 开头并以 ``` 结尾）
    if response_content.startswith("```json") and response_content.endswith("```"):
        # 提取 ```json 和 ``` 之间的内容
        json_content = response_content[7:-3].strip()
    else:
        # 直接使用原始内容作为 JSON
        json_content = response_content

    # 检查是否为空
    if not json_content:
        raise ValueError("模型未返回有效的 JSON 内容")

    # 尝试解析 JSON
    try:
        return json.loads(json_content)
    except json.JSONDecodeError as e:
        raise ValueError(f"JSON 解析失败，请检查模型输出格式。原始内容: {response_content}") from e

# 使用提示模板+langchain+Memory+structured_outputs
def langchain_LLM_chain(model,apikey,url, theme):
    # 构造提示模板
    prompt_template = PromptTemplate(
        input_variables=["theme"],
        template="""
        根据以下主题theme，输出相关的短篇小说，同时生成小说的摘要，包括小说故事发生的时间、发生的地点、涉及的人物，以及事情的起因、经过、结果：。
        主题: {theme}
        
        输出格式：
        小说摘要:
        时间：
        地点:
        人物:
        起因:
        经过:
        结果:
        小说正文:
        """
    )

    
    llm = ChatOpenAI(model=model, 
                 api_key=apikey,
                 openai_api_base=url,
                 timeout=120
                 )


    # 使用链式调用生成响应
    chain = prompt_template | llm
    response = chain.invoke({"theme": theme})

    token_usage = response.response_metadata.get("token_usage", {})

    completion_tokens = token_usage.get("completion_tokens", 0)
    prompt_tokens = token_usage.get("prompt_tokens", 0)
    total_tokens = token_usage.get("total_tokens", 0)

    print(f"Completion Tokens: {completion_tokens}")
    print(f"Prompt Tokens: {prompt_tokens}")
    print(f"Total Tokens: {total_tokens}")

    response=response.content

    return response

def langchain_LLM_chain_structured_output(model,apikey,url, theme):
    # 构造提示模板
    prompt_template = PromptTemplate(
        input_variables=["theme"],
        template="""
        根据以下主题theme，输出相关的短篇小说，同时生成小说的摘要，包括小说故事发生的时间、发生的地点、涉及的人物，以及事情的起因、经过、结果：。
        主题: {theme}
        
        输出格式：
        小说摘要:
        时间：
        地点:
        人物:
        起因:
        经过:
        结果:
        小说正文:
        """
    )

    
    llm = ChatOpenAI(model=model, 
                 api_key=apikey,
                 openai_api_base=url,
                 timeout=120
                 )
    structured_llm = llm.with_structured_output(Novel)

    # 使用链式调用生成响应
    chain = prompt_template | structured_llm
    response = chain.invoke({"theme": theme})

    # token_usage = response.response_metadata.get("token_usage", {})

    # completion_tokens = token_usage.get("completion_tokens", 0)
    # prompt_tokens = token_usage.get("prompt_tokens", 0)
    # total_tokens = token_usage.get("total_tokens", 0)

    # print(f"Completion Tokens: {completion_tokens}")
    # print(f"Prompt Tokens: {prompt_tokens}")
    # print(f"Total Tokens: {total_tokens}")

    # response=response.content

    return response

def langchain_LLM_chain_json(model,apikey,url, theme):
    # 构造提示模板
    prompt_template = PromptTemplate(
        input_variables=["theme"],
        template="""
        根据以下主题theme，输出相关的短篇小说，以 JSON 格式返回结果。

        同时生成小说的摘要，包括小说故事发生的时间、发生的地点、涉及的人物，以及事情的起因、经过、结果。
        主题: {theme}

        请严格按照以下 JSON 格式返回数据，不要省略任何字段：
        JSON 格式要求如下：
        {{
            "occurrence_time": "故事发生的时间",
            "place": "故事发生的地点",
            "person": "涉及的人物",
            "cause": "事情的起因",
            "process": "事情的经过",
            "result": "事情的结果",
            "novel": "小说正文"
        }}
        """
    )

    
    llm = ChatOpenAI(model=model, 
                 api_key=apikey,
                 openai_api_base=url,
                 timeout=120
                 )


    # 使用链式调用生成响应
    chain = prompt_template | llm
    response = chain.invoke({"theme": theme})


    response_json = parse_json_response(response.content)


    token_usage = response.response_metadata.get("token_usage", {})

    completion_tokens = token_usage.get("completion_tokens", 0)
    prompt_tokens = token_usage.get("prompt_tokens", 0)
    total_tokens = token_usage.get("total_tokens", 0)

    print(f"Completion Tokens: {completion_tokens}")
    print(f"Prompt Tokens: {prompt_tokens}")
    print(f"Total Tokens: {total_tokens}")



    return response_json


if __name__ == "__main__":


    # 获取当前脚本所在的目录
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # 获取上级目录
    parent_dir = os.path.dirname(current_dir)

    # 拼接 config.yaml 的完整路径
    config_path = os.path.join(parent_dir, "config.yaml")
    # 读取 config.yaml 文件
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
        # 获取 OpenAI 配置
    openai_config = config.get("OpenAI", {})
    model = openai_config.get("model")
    api_key = openai_config.get("api_key")
    api_base = openai_config.get("api_base")

    print("开始用 OpenAI 模型生成相关主题的小说！输入 'exit' 来结束对话。")
    while True:
        user_input = input("主题: ")
        if user_input.lower() in ["退出", "exit"]:
            print("对话结束。再见！")
            break
        # response = langchain_LLM_chain(model,api_key,api_base, user_input)
        # print(f"小说: {response}")
        
        # response = langchain_LLM_chain_structured_output(model,api_key,api_base, user_input)
        # print(f"小说: {response}")

        response = langchain_LLM_chain_json(model,api_key,api_base, user_input)

        # 打印解析后的内容
        print("小说摘要:")
        print(f"时间: {response['occurrence_time']}")
        print(f"地点: {response['place']}")
        print(f"人物: {response['person']}")
        print(f"起因: {response['cause']}")
        print(f"经过: {response['process']}")
        print(f"结果: {response['result']}")
        print("小说正文:")
        print(response['novel'])



