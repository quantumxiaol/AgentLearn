from langchain.prompts import PromptTemplate
from langchain.prompts import ChatPromptTemplate
from langchain_community.llms import GPT4All
from langchain_openai import OpenAI, ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain.chains import LLMChain
import yaml
import os
import sys


# 使用提示模板
def langchain_LLM_gpt(model,apikey,url, theme):
    # 构造提示模板
    prompt_template = PromptTemplate(
        input_variables=["theme"],
        template="""
        根据以下主题theme，输出相关的短篇小说：。
        主题: {theme}
        
        输出格式：
        小说:
        """
    )

    
    llm = ChatOpenAI(model=model, 
                 api_key=apikey,
                 openai_api_base=url,
                 timeout=120
                 )


    # 填充提示并生成结果
    prompt = prompt_template.format(theme=theme)

    # 计算token数
    token_count = len(prompt.split())
    # print(f"Token count: {token_count}")
    # print(prompt)
    response = llm.invoke(prompt)
    response=response.content


    return response

# 使用提示模板+langchain
def langchain_LLM_chain(model,apikey,url, theme):
    # 构造提示模板
    prompt_template = PromptTemplate(
        input_variables=["theme"],
        template="""
        根据以下主题theme，输出相关的短篇小说：。
        主题: {theme}
        
        输出格式：
        小说:
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
        response = langchain_LLM_chain(model,api_key,api_base, user_input)

        print(f"小说: {response}")



