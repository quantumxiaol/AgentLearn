# 目的

使用Langgarph来完成一个复杂的图，能够使用节点组成网络，进行结构化输出。

-写小说-修改小说-

# 概念

## 图（Graphs）

图是 LangGraph 的核心概念，用于将智能体（Agent）的工作流建模为图结构。图由节点（Nodes）和 边（Edges）组成。节点代表工作流中的具体操作或任务，而边则定义了这些任务之间的流转逻辑。边通常是一个 Python 函数，基于当前的状态（State）决定下一步执行哪个节点或一组节点。定义一个图的示例如下：

    from langgraph import StateGraph

    # 定义状态
    class WorkflowState:
        def __init__(self, input_text=""):
            self.input_text = input_text
            self.processed_text = ""

    # 初始化图
    workflow = StateGraph(WorkflowState)

## 状态（State）

状态是 LangGraph 中的一个中心对象，用于在图的不同节点之间传递信息。每个图都有一个全局状态，所有节点都可以读取或修改这个状态。StateGraph 是 LangGraph 提供的一个类，用于表示整个图的结构，并通过传入一个状态定义来初始化。

    def process_input(state):
        # 修改状态
        state.processed_text = state.input_text.upper()
        return state

    # 将状态处理函数绑定到节点
    workflow.add_node("process_input", process_input)

## 节点（Nodes）

节点是图的基本组成部分，每个节点代表一个独立的任务或功能模块。节点可以是简单的函数，也可以是更复杂的逻辑，例如调用外部 API、执行推理任务或与其他智能体交互。

    def greet_user(state):
        print(f"Hello! Your input was: {state.input_text}")
        return state

    # 添加节点到图
    workflow.add_node("greet_user", greet_user)

## 边（Edges）

边定义了节点之间的流转逻辑，决定了工作流的执行路径。边通常是基于当前状态的条件判断函数，动态地选择下一步执行的节点。

    def decide_next_step(state):
        if len(state.input_text) > 10:
            return "process_input"
        else:
            return "greet_user"

    # 添加边
    workflow.add_edge("*", decide_next_step)

## 多代理协作（Multi-Agent Collaboration）

LangGraph 支持多个智能体（Agents）之间的协作，使得复杂任务可以通过多个独立代理的分工完成。这种协作机制特别适合需要动态调整工作流的应用场景。

    # 定义第一个子图
    subgraph_1 = StateGraph(WorkflowState)
    subgraph_1.add_node("agent_1_task", lambda state: state)

    # 定义第二个子图
    subgraph_2 = StateGraph(WorkflowState)
    subgraph_2.add_node("agent_2_task", lambda state: state)

    # 主图协调子图
    main_graph = StateGraph(WorkflowState)
    main_graph.add_node("subgraph_1", subgraph_1.run)
    main_graph.add_node("subgraph_2", subgraph_2.run)

## 循环图（Cyclic Graphs）

LangGraph 提供了一种简单的方式来创建循环图，这种图结构非常适合需要反复迭代的任务。循环图允许工作流在某些条件下返回到之前的节点，从而实现动态调整和优化。

    def check_completion(state):
        if state.processed_text == "":
            return "process_input"
        else:
            return "end"

    # 添加循环边
    workflow.add_edge("process_input", check_completion)
    workflow.add_edge("check_completion", "process_input")

## PromptTemplate
单轮的，不需要维护上下文。
例如：生成文章、翻译、摘要提取等。

    # 定义模板
    template = "根据以下主题生成一段短文：\n主题: {topic}"
    prompt_template = PromptTemplate(input_variables=["topic"], template=template)

    # 填充模板
    prompt = prompt_template.format(topic="人工智能")
    print(prompt)

## ChatPromptTemplate
涉及多轮对话，需要维护聊天上下文。
例如：聊天机器人、客服系统、虚拟助手等。

    # 定义模板
    template = ChatPromptTemplate.from_messages([
        SystemMessage(content="你是一个智能助手，帮助用户解答问题。"),
        HumanMessage(content="你好，我想了解人工智能的发展历史。"),
        ("ai", "{ai_response}"),  # 动态插入 AI 的回复
    ])

    # 填充模板
    prompt = template.format(ai_response="人工智能起源于20世纪50年代，经历了多次技术革新。")
    print(prompt)