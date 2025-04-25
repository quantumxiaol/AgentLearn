# Agent 学习笔记

毕业了，工作了三个月跑路考研了，现在在给导师干活。

笑点解析：实习工资比跑路前工作到手要多，住的好（三室两卫一厅住两个人），管早午饭。

项目大方向是Agent，让大模型能用工具来解决一些问题。

这是我用来学习Langchain和Langgraph的，以及探索LLM如何变成VLM，就是让它能看图片，有一定的多模态能力。通过图片来判断一些场景。


# 任务

- [x] 了解OpenAI、Langchain、Langgraph三种调用方式
- [x] 将图片输给LLM ([文档](imageToken/readme.md))
  - 方法：采用Vit提取特征Token化，然后拼接prompt，然后输入给LLM
  - 结果：效果一般,OpenAI GPT-4o说它理解不了图片
  - 改进：换成原生多模态的模型可能会好，但那样就需要对模型进行SFT微调了。
- [ ] 模型API直接调用
  - [x] OpenAI的API完成对话([文档](task1/readme.md))
  - [ ] 考虑使用某种方法能够输入图片，或者使用VLm模型
- [ ] 使用Langchian调用LLM
  - [x] 使用提示模板(Prompt Template)
  - [x] 使用json或structured output([文档](task2/readme.md))
  - [ ] 使用Memory组件完成多轮对话，比如修改上次输出
- [ ] 使用Langgraph调用LLM
  - [x] 使用提示模板(Prompt Template)
  - [ ] 使用json或structured output
  - [ ] 修改节点，增加功能
- [ ] 还在增加……




# 学习过程中遇到的报错

### 1

> openai\_base_client.py", line 1057, in _request raise self._make_status_error_from_response(err.response) from None
openai.InternalServerError: 502 Bad Gateway

api_base_url是用来代理的，网络不好的时候需要用这个，否则模型会无响应

### 2

> Error code: 400 - {'error': {'message': "Missing required parameter: 'prompt'.(request id:    )", 'type': 'invalid_request_error', 'param': 'prompt', 'code': 'missing_required_parameter'}}

这是一开始Langchain中ChatOpenAI和OpenAI没搞明白的，当时照着创建模板prompt，使用OpenAI就说缺失prompt，用ChatOpenAI的时候就好了。

### 3

>This model's maximum context length is 128000 tokens. However, your messages resulted in 901994 
tokens. Please reduce the length of the messages

这是用Vit把图片变成Token，然后拼接prompt后喂给LLM，这个Token数太大了。
后面先预处理图片，再用量化方法把Token降下来了。不过大模型还是理解不了图像。

### 4

>langchain_openai\chat_models\base.py:1660: UserWarning: Received a Pydantic BaseModel V1 schema. This 
is not supported by method="json_schema". Please use method="function_calling" or specify schema via JSON Schema or Pydantic V2 BaseModel. Overriding to method="function_calling".
  warnings.warn()

langchain_openai 库在处理 Pydantic 的 BaseModel 时检测到使用的是 Pydantic V1 的模型定义，而当前的 langchain 或 openai 集成可能需要 Pydantic V2 或其他兼容的方式（如 JSON Schema 或 function_calling 方法）。

### 5

>解析json格式失败

在prompt中，让模型要严格输出json格式。不过有时会返回markdown格式的json，如

    ```json
    {
        "answer": "The capital of japan is Tokyo."
    }
    ```
使用一个函数，如果是marrkdown格式的json，就去掉开头结尾的，再用正则化去掉非法字符。

|ASCII范围  |描述|
|----------|----|
|\x00-\x08|	空字符（NUL）、响铃（BEL）等|
|\x0b-\x0c|	垂直制表符（VT）、换页符（FF）|
|\x0e-\x1f|	其他控制字符（如 ESC、CAN 等）|

