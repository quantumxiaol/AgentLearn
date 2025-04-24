毕业了，工作了三个月跑路考研了，现在在给导师干活。

项目大方向是Agent，让大模型能用工具来解决一些问题。

这是我用来学习Langchain和langgraph的，以及探索LLM如何变成VLM，就是让它能看图片，有一定的多模态能力。


# 任务

- [ ] 了解OpenAI、Langchain、Langgraph三种调用方式
- [ ] 将图片输给LLM
- [ ] 还在增加




# 学习过程中遇到的报错

> openai\_base_client.py", line 1057, in _request raise self._make_status_error_from_response(err.response) from None
openai.InternalServerError: 502 Bad Gateway

api_base_url是用来代理的，网络不好的时候需要用这个，否则模型会无响应

> Error code: 400 - {'error': {'message': "Missing required parameter: 'prompt'.(request id:    )", 'type': 'invalid_request_error', 'param': 'prompt', 'code': 'missing_required_parameter'}}

这是一开始Langchain中ChatOpenAI和OpenAI没搞明白的，当时照着创建模板prompt，使用OpenAI就说缺失prompt，用ChatOpenAI的时候就好了。

>This model's maximum context length is 128000 tokens. However, your messages resulted in 901994 
tokens. Please reduce the length of the messages

这是用Vit把图片变成Token，然后拼接prompt后喂给LLM，这个Token数太大了。
后面先预处理图片，再用量化方法把Token降下来了。不过大模型还是理解不了图像。
