# 目的

使用Langchain来完成一个复杂的链，能够使用内存组件，进行结构化输出。

# 概念

LangChain 的主要组件包括:模型(Models)、提示(Prompts)、索引(Indexes)、链(Chains)、代理(Agents)、内存(Memory)。

链是 LangChain 中的一个核心概念,它允许将多个组件(如提示、模型、解析器等)组合在一起,形成一个端到端的调用序列,用于完成复杂的任务。

代理(Agent)是一种能够使用工具并决定下一步行动的实体。它可以根据用户输入和当前状态,选择适当的工具来执行任务,实现更复杂的交互和问题解决。

提示模板(Prompt Template)是一种结构化的方式来创建提示。允许定义一个带有占位符的模板,然后在运行时用实际值填充这些占位符,从而生成完整的提示。

内存(Memory)组件用于在对话或交互过程中存储和检索历史信息。它允许模型或应用程序记住之前的交互,从而实现更连贯和上下文相关的对话。

输出解析器(Output Parser)是用来将语言模型的原始输出转换为结构化格式的组件。它可以将文本输出解析为特定的数据结构,如列表、字典或自定义对象。

某些 LangChain 聊天模型支持 .with_structured_output() 方法。此方法只需要一个架构作为输入，并返回一个字典或 Pydantic 对象。


# LLMChain和RunnableSequence
在 LangChain 中，LLMChain 是一个用于调用语言模型（LLM）的工具链。它的核心功能是：

接收输入（如提示模板和用户输入）。
调用语言模型生成文本。
返回生成的文本结果。
为了兼容性和灵活性，LLMChain 的输出通常会被包装为 Generation 对象。这是 LangChain 内部的一种标准化设计。

Generation 是 LangChain 中的一个类，用于表示语言模型生成的结果。它包含以下关键字段：

text：生成的文本内容（字符串类型）。
generation_info：额外的元信息（如 token 数量、日志概率等）。

这种设计的优点是：
统一格式：无论使用哪种语言模型，输出都可以被标准化为 Generation 对象。
支持多代生成：如果需要生成多个候选结果（例如 top-k 或 beam search），可以返回一个 Generation 列表。
扩展性：可以通过 generation_info 添加额外的信息，而不会破坏原有的结构。

如果启用了 memory（如 ConversationBufferMemory），output_key 的值也会被存储到记忆模块中，作为对话历史的一部分。

RunnableSequence 是 LangChain 提供的一种新的链式调用方式，旨在替代被废弃的 LLMChain。它基于管道（pipeline）的设计，允许你将多个组件（如提示模板、模型调用等）串联起来。

输出机制
RunnableSequence 的输出直接是最后一个组件的输出，不需要额外的包装（如 Generation）。具体来说：

提示模板：将输入数据格式化为提示文本。
语言模型：根据提示文本生成输出。
结构化输出：如果使用了 with_structured_output，输出将是 Pydantic 模型对象。

# Memory机制
memory 是 LangChain 中的一种机制，用于在多轮对话或链式调用中保存和传递上下文信息。

保存对话历史：
每次调用链时，输入和输出都会被存储到 memory 中。
这使得后续的调用可以访问之前的对话内容，从而实现上下文感知。

自动注入上下文：
在调用链时，memory 会自动将对话历史附加到提示模板中。

# [运行结果](result.md)