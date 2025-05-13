# 报错

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

### 6
>The class `LLMChain` was deprecated in LangChain 0.1.17 and will be removed in 1.0. Use :meth:`~RunnableSequence, e.g., `prompt | llm`` instead.
  write_chain = LLMChain(

LangChain 0.1.17 版本开始弃用 LLMChain，推荐使用更灵活的 RunnableSequence。
RunnableSequence 是一种基于管道（pipeline）的设计，允许你将多个组件（如提示模板、模型调用等）串联起来。

### 7
>    response = write_chain.invoke({
               ^^^^^^^^^^^^^^^^^^^^
    pydantic\main.py", line 253, in __init__
    validated_self = self.__pydantic_validator__.validate_python(data, self_instance=self)
                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
pydantic_core._pydantic_core.ValidationError: 1 validation error for Generation
text
  Input should be a valid string [type=string_type, input_value=Novel(occurrence_time='...樱花下的邂逅》'), input_type=Novel]
    For further information visit https://errors.pydantic.dev/2.11/v/string_type

Generation 的限制：
Generation 类的 text 字段必须是字符串类型。
当使用 with_structured_output(Novel) 时，链的输出是一个 Pydantic 模型对象（Novel），而不是字符串。这导致了 ValidationError。

### 8

>langgraph.errors.InvalidUpdateError: Expected dict,

langgraph 期望节点返回一个字典（dict），但 superviser 函数返回了一个字符串

### 9
>Checkpointer requires one or more of the following 'configurable' keys: ['thread_id', 'checkpoint_ns', 'checkpoint_id']

### 10
>    image_data = base64.b64encode(img).decode('utf-8')
                 ^^^^^^^^^^^^^^^^^^^^^
  File "anaconda3\envs\yolo\Lib\base64.py", line 58, in b64encode
    encoded = binascii.b2a_base64(s, newline=False)
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
TypeError: a bytes-like object is required, not 'Image'

base64.b64encode() 方法需要的是字节类型的输入

### 11

>openai.RateLimitError: Error code: 429 - {'error': {'message': '当前分组上游负载已饱和，请稍后再试 (request id: 2025042913372369276548BME6E0jc)', 'type': 'invalid_request_error', 'param': 'messages', 'code': 'context_length_exceeded'}}

这个是openai的限流问题，传给的Token太多了

# 警告

### 1

>LangChainDeprecationWarning: As of langchain-core 0.3.0, LangChain uses pydantic v2 internally. The langchain_core.pydantic_v1 module was a compatibility shim for pydantic v1, and should no longer be used. Please update the code to import from Pydantic directly.

For example, replace imports like: `from langchain_core.pydantic_v1 import BaseModel`
with: `from pydantic import BaseModel`
or the v1 compatibility namespace if you are working in a code base that has not been fully upgraded to pydantic 2 yet.         from pydantic.v1 import BaseModel

### 2

>langchain_task2_Momory.py:152: LangChainDeprecationWarning: The method `Chain.run` was deprecated in langchain 0.1.0 and will be removed in 1.0. Use :meth:`~invoke` instead.
  response = write_chain.run({

需要替代API