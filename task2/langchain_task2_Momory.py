from langchain.prompts import PromptTemplate
from langchain.prompts import ChatPromptTemplate
from langchain_community.llms import GPT4All
from langchain_openai import OpenAI, ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain.chains import LLMChain
from langchain.schema.runnable import RunnableSequence
from typing import Optional
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain.memory import ConversationBufferMemory
import yaml
import os
import sys
import json
import re
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from readConfig import get_openai_config
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

memory = ConversationBufferMemory()
def get_update_prompt_template():
    return ChatPromptTemplate.from_template(
        """
        你是一个小说编辑助手。请根据以下要求修改小说内容：
        {instructions}
        当前小说内容如下：
        {novel_content}

        """
    )

def get_write_prompt_template():
    prompt_template = PromptTemplate(
        input_variables=["theme"],
        template="""
        根据以下主题theme，输出相关的短篇小说，同时输出小说内容：
        主题: {theme}

        """
    )
    return prompt_template

def get_prompt_template():
    return ChatPromptTemplate.from_template(
        """
        根据以下指令执行任务：
        如果指令是 '写小说'，请根据主题theme生成一篇相关的短篇小说，并严格按照以下结构返回结果。
        如果指令是 '修改小说'，请根据提供的修改指令对当前小说内容进行修改，并严格按照以下结构返回结果。
        
        {instructions}
        
        当前小说内容如下（如果适用）：
        {novel_content}
        
        请严格按照以下结构返回结果：
        {format_instructions}
        """
    )
# 构建主链
def build_main_chain_v0(model, api_key, api_base):
    llm = ChatOpenAI(
        model=model,
        api_key=api_key,
        openai_api_base=api_base,
        timeout=120
    )
    llm = llm.with_structured_output(Novel)

    
    # 写小说的链
    write_prompt = get_write_prompt_template()
    # write_chain = LLMChain(
    #     llm=llm,
    #     prompt=write_prompt,
    #     memory=memory,
    # )
    write_chain = write_prompt | llm
    
    # 修改小说的链
    update_prompt = get_update_prompt_template()
    # update_chain = LLMChain(
    #     llm=llm,
    #     prompt=update_prompt,
    #     memory=memory,
    # )
    update_chain = update_prompt | llm
    
    return write_chain, update_chain

def build_main_chain(model, api_key, api_base):
    llm = ChatOpenAI(
        model=model,
        api_key=api_key,
        openai_api_base=api_base,
        timeout=120
    )
    
    prompt = get_write_prompt_template()
    chain = LLMChain(
        llm=llm,
        prompt=prompt,
        memory=memory,
        output_key="novel"
    )
    
    return chain


if __name__ == "__main__":

    # 获取配置
    model, api_key, api_base = get_openai_config()

    print("开始用 OpenAI 模型生成相关主题的小说！输入 'exit' 来结束对话。")
    # 构建主链
    write_chain, update_chain = build_main_chain_v0(model, api_key, api_base)

    while True:
        user_input = input("请输入小说主题 (或输入 'exit' 结束): ")
        if user_input.lower() in ["退出", "exit"]:
            print("对话结束。再见！")
            break

        # 写小说
        print(f"正在生成关于 '{user_input}' 的小说...")
        response = write_chain.invoke({
            "theme": user_input,
        })
        # current_novel = json.loads(response)  # 将响应解析为字典
        # print(f"生成的小说内容: {json.dumps(current_novel, ensure_ascii=False, indent=2)}")
        print(f"小说: {response}")

        # 是否修改小说
        modify_input = input("是否需要修改小说内容？(是/否): ")
        if modify_input.lower() in ["否", "不"]:
            continue

        # 修改小说
        while True:
            instructions = input("请输入修改指令（例如：将主人公的名字从 '目白麦昆' 修改为 '东海帝王'）: ")
            if instructions.lower() in ["退出", "exit"]:
                break

            # 更新小说内容
            # "format_instructions": Novel.schema_json()
            # novel_content = json.dumps(current_novel, ensure_ascii=False)
            novel_content = response
            response = update_chain.invoke({
                "instructions": instructions,
                "novel_content": novel_content,

            })
            print(f"修改后的小说: {response}")

            # 是否继续修改
            continue_modify = input("是否继续修改小说？(是/否): ")
            if continue_modify.lower() in ["否", "不"]:
                break



