分别调用OpenAI、Langchain、Langgraph三种方式

得到输出

# 1. OpenAI

    通过OpenAI创建一个client，用response = client.chat.completions.create调用得到回答。

# 2. Langchain
    
    从 LangChain 0.1.17 开始，LLMChain 被标记为过时，
    使用 RunnableSequence 或直接使用管道操作符 | 来构建链。


    1. text

    我使用 langchain_openai来创建llm

    2. image

    我使用 vit 将图片Token化，然后把Token拼接在prompt后面，再输入给LLM。



# 3. Langgraph

    LangGraph 的核心是将 agent 的工作流建模为图。您可以通过以下三个关键组件来定义 agent 的行为：

    状态 (State)：graph 的核心，表示应用程序当前快照的共享数据结构，它是所有节点唯一且共同的输入。状态可以是任何 Python 类型，但通常是 TypedDict 或 Pydantic BaseModel(字典类型)。

    节点 (Nodes)：Python 函数，用于编码代理的逻辑。它们接收当前的状态作为输入，执行某些计算或功能，并返回更新后的状态。

    边 (Edges)：Python 函数，根据当前的状态确定下一个要执行的节点。它们可以是条件分支或固定的转换。

    使用LangGraph构建工作流的步骤如下：
        初始化模型和工具
        定义图的状态信息
        定义图节点
        定义图的入口节点和边关系
        编译图
        执行图

