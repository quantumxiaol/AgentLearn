
from langchain_openai import OpenAI, ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langchain.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langgraph.checkpoint.memory import MemorySaver

import yaml
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from readConfig import get_openai_config

class Novel(BaseModel):
    occurrence_time: str = Field(description="故事发生的时间")
    place: str = Field(description="故事发生的地点")
    person: str = Field(description="涉及的人物")
    cause: str = Field(description="事情的起因")
    process: str = Field(description="事情的经过")
    result: str = Field(description="事情的结果")
    novel: str = Field(description="小说正文")

# 定义状态
# 状态可以是任何 Python 类型，但通常是 TypedDict 或 Pydantic BaseModel(字典类型)。
class NovelGenerationState(TypedDict):
    user_input: str
    novel: Novel
    next_step: str

def get_update_prompt_template():
    prompt =PromptTemplate(
        input_variables=["instructions","novel_content"],
        template=
        """
        你是一个小说编辑助手。请根据以下要求修改小说内容：
        {instructions}\n
        当前小说内容如下：
        {novel_content}

        """
    )
    return prompt
    

def get_write_prompt_template():
    prompt_template = PromptTemplate(
        input_variables=["theme"],
        template="""
        根据以下主题theme，输出相关的短篇小说，同时输出小说内容：
        主题: {theme}

        """
    )
    return prompt_template

def get_model(model, apikey, url):
    # 初始化LLM
    llm = ChatOpenAI(
        model=model,
        api_key=apikey,
        openai_api_base=url,
        timeout=120
    )
    llm = llm.with_structured_output(Novel)
    return llm

# 定义生成短篇小说的节点函数
def generate_novel(state: NovelGenerationState,llm):
    print("Generate Novel Called!")
    # 构造提示模板
    prompt_template = get_write_prompt_template()


    # 填充提示并生成结果
    # theme = state["theme"]  # 从状态字典中获取主题
    theme = state["user_input"]
    prompt = prompt_template.format(theme=theme)
    response = llm.invoke(prompt)

    # 更新状态
    state["novel"] = response
    state["next_step"] = "superviser"  # 设置下一个步骤为监督者
    print(f"小说内容： {state['novel']}")

    return state

def update_novel(state: NovelGenerationState,llm):
    print("Update Novel Called!")
    if not state.get("novel"):
        raise ValueError("无法修改小说，因为小说内容为空！")
    if not state.get("user_input"):
        raise ValueError("无法修改小说，因为修改内容为空！")
    # 构造提示模板
    prompt_template = get_update_prompt_template()

    # 填充提示并生成结果
    novel_content = state["novel"]  # 从状态字典中获取小说内容
    instructions = "请根据以下要求修改小说内容：\n" + state["user_input"]  # 从状态字典中获取修改指令

    prompt = prompt_template.format(instructions=instructions, novel_content=novel_content)
    print(f"prompt: {prompt}")
    response = llm.invoke(prompt)
    # print(f"小说内容： {state['novel']}")
    print(f"修改后的小说内容： {response}")

    # 添加修改后的小说内容到状态字典中
    state["novel"] = response
    state["next_step"] = "superviser"  # 设置下一个步骤为监督者
    return state

# 定义监督者函数，判断是否重开小说或者再次修改小说内容
def superviser(state: NovelGenerationState):
    print("开始用 OpenAI 模型生成相关主题的小说！"\
          "输入 '开始' 来写小说。" \
        "输入 'exit' 来结束对话。" \
        "或者输入 '修改' 来修改小说内容，" \
        "输入 '重开' 来重新生成小说。")
    user_input=input("请输入指令：")

    print(f"superviser Called!")
    print(f"小说内容： {state['novel']}")
    # 判断用户输入是否包含"修改小说"或"重开小说"
    if "修改" in user_input or "modify" in user_input.lower():
        user_input = input("请输入修改内容：")
        state["user_input"] = user_input 
        print(f"修改内容： {state['user_input']}")
        state["next_step"] = "update_novel"
        return state
    elif "开始" in user_input or "remake" in user_input.lower():
        user_input = input("请输入小说主题：")
        state["user_input"] = user_input
        print(f"小说主题： {state['user_input']}")
        state["next_step"] = "generate_novel"
        
        return state
    elif user_input.lower() in ["退出", "exit"]:
        state["next_step"] = END
        return state
    
    else:
        print("无效的输入，请重新输入。")
        state["next_step"] = "superviser"
        return state

def router(state):
    next_step = state.get("next_step")
    if next_step == "generate_novel":
        print("开始生成小说！")
        return "generate_novel"
    elif next_step == "update_novel":
        print("开始修改小说！")
        return "update_novel"
    else:
        return END

memory = MemorySaver()
# 定义工作流
def langgraph_LLM_gpt(model, apikey, url):
    # 获取用户输入

    # 获取模型
    llm = get_model(model, apikey, url)
    # checkpoint = MemorySaver()

    # 创建状态图
    workflow = StateGraph(NovelGenerationState)

    # 添加生成小说的节点
    workflow.add_node("generate_novel", lambda state: generate_novel(state, llm))

    # 添加修改小说的节点
    workflow.add_node("update_novel", lambda state: update_novel(state, llm))

    # 添加监督者节点
    workflow.add_node("superviser", lambda state: superviser(state))

    # 显式添加边
    workflow.add_edge(START, "superviser")
    workflow.add_edge("generate_novel", "superviser")
    workflow.add_edge("update_novel", "superviser")  

    # 使用 add_conditional_edges 处理分支逻辑


    workflow.add_conditional_edges("superviser", router)

    # 设置入口和出口
    # workflow.set_entry_point("generate_novel")
    # workflow.set_finish_point("generate_novel")

    # 编译图
    # graph = workflow.compile(checkpointer=memory)
    graph = workflow.compile()

    # 初始化状态
    initial_state = {"user_input": "", "novel": None, "next_step": "superviser"}



    # 执行图
    final_state = graph.invoke(initial_state)



    # 返回生成的小说
    return final_state["novel"]

if __name__ == "__main__":

    # 获取配置
    model, api_key, api_base = get_openai_config()

    response = langgraph_LLM_gpt(model,api_key,api_base)

    print(f"小说: {response}")



