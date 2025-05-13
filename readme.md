# Agent 学习笔记

毕业了，工作了三个月跑路考研了，现在在给导师干活。

笑点解析：实习工资比跑路前工作到手要多，住的好（三室两卫一厅住两个人），管早午饭。

项目大方向是Agent，让大模型能用工具来解决一些问题。

这是我用来学习Langchain、Langgraph、MCP等的；以及探索LLM如何变成VLLM，让它能看图片，具备一定的多模态能力。进而通过图片来判断一些场景。


# 任务

- [x] 了解OpenAI、Langchain、Langgraph三种调用方式
- [x] 将图片输给LLM ([文档](imageToken/readme.md))
  - [ ] 拼接Token到prompt中
    - 方法：采用Vit提取特征Token化，然后拼接prompt，然后输入给LLM
    - 结果：效果一般,OpenAI GPT-4o说这样它理解不了图片
    - 改进：换成原生多模态的模型可能会好，但那样就需要对模型进行SFT微调了。
  - [ ] 原生多模态的模型通过API调用输入图片  
    - [x] OpenAI GPT-4o理解图片
    - [x] 使用LangChain理解图片 ([文档](task4/readme.md))([结果](task4/result.md))
- [ ] 模型API直接调用
  - [x] OpenAI的API完成对话([文档](task1/readme.md))
  - [ ] 考虑使用某种方法能够输入图片，或者使用VLLM模型
- [ ] 使用Langchian调用LLM
  - [x] 使用提示模板(Prompt Template)
  - [x] 使用json或structured output([文档](task2/readme.md))
  - [x] 使用Memory组件完成多轮对话，比如修改上次输出(修改小说)([结果](task2/result.md))
    - 存在的问题：修改小说时是将memory中的的小说拿出来放到prompt中，不清楚这是否符合我预先的假设 
- [ ] 使用Langgraph调用LLM
  - [x] 使用提示模板(Prompt Template)
  - [x] 使用json或structured output([文档](task3/readme.md))
  - [x] 使用监督者节点，写小说、按照要求修改小说，使用state记忆上下文([结果](task3/result.md))
  - [ ] 使用checkpoint记忆上下文
  - [ ] 修改节点，增加功能
- [ ] Tools调用
  - [x] 使用openai function call([文档](task5/readme.md))
  - [x] 使用langchain tools([结果](task5/result.md))
  - [x] 对比使用工具的LLM和原生的LLM
  - [ ] 写一些小工具，图片预处理、目标检测、深度估计等
  - [x] 搭建MCP Server ([文档](task7/readme.md))
  - [x] 使用MCP server来调用Tools([结果](task7/result.md))
  - [ ] LLM调用工具
- [ ] 搭建服务端和客户端
  - [x] 了解FastApi和flask([文档](task6/readme.md))
  - [x] 使用FastApi和flask创建服务端和客户端，测试联通，调用自己的工具([结果](task6/result.md))
  - [ ] 使用FastApi部署服务
- [ ] AgentKit使用
  - [ ] 了解AgentKit
  - [ ] 了解manus
- [ ] 实现简单项目
  - [ ] 根据图片写短篇故事
    - [ ] 目标检测
- [ ] 还在增加……

# 目录
### [task1](task1)-[调用OpenAI的API](task1/readme.md)
### [task2](task2)-[使用Langchian调用LLM](task2/readme.md)
### [task3](task3)-[使用Langgraph调用LLM](task3/readme.md)
### [task4](task4)-[使用Langchain处理图片](task4/readme.md)
### [task5](task5)-[Tools调用](task5/readme.md) function call+tools
### [task6](task6)-[搭建服务端和客户端](task6/readme.md)
### [task7](task7)-[使用MCP tool和MCP server](task7/readme.md)


# [报错、警告和处理方法](error.md)