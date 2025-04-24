
from langchain_openai import OpenAI, ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langchain.prompts import PromptTemplate


import yaml
import os
import sys


# 定义状态
# 状态可以是任何 Python 类型，但通常是 TypedDict 或 Pydantic BaseModel(字典类型)。
class NovelGenerationState(TypedDict):
    theme: str  # 主题
    novel: str  # 生成的小说
# 定义生成短篇小说的节点函数
def generate_novel(state: NovelGenerationState, model, apikey, url):
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

    # 初始化LLM
    llm = ChatOpenAI(
        model=model,
        api_key=apikey,
        openai_api_base=url,
        timeout=120
    )

    # 填充提示并生成结果
    theme = state["theme"]  # 从状态字典中获取主题
    prompt = prompt_template.format(theme=theme)
    response = llm.invoke(prompt).content

    # 更新状态
    state["novel"] = response
    return state

# 定义工作流
def langgraph_LLM_gpt(model, apikey, url, theme):
    # 创建状态图
    workflow = StateGraph(NovelGenerationState)

    # 添加生成小说的节点
    workflow.add_node("generate_novel", lambda state: generate_novel(state, model, apikey, url))

    # 显式添加边
    # workflow.add_edge(START, "generate_novel")  # 从 START 到 generate_novel
    # workflow.add_edge("generate_novel", END)   # 从 generate_novel 到 END

    # 设置入口和出口
    workflow.set_entry_point("generate_novel")
    workflow.set_finish_point("generate_novel")

    # 编译图
    graph = workflow.compile()

    # 初始化状态
    initial_state = {"theme": theme, "novel": ""}

    # 执行图
    final_state = graph.invoke(initial_state)

    # 返回生成的小说
    return final_state["novel"]

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
        response = langgraph_LLM_gpt(model,api_key,api_base, user_input)

        print(f"小说: {response}")



