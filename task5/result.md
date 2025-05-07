# 结果
## 使用OpenAI function call
>choices=[Choice(finish_reason='function_call', index=0, logprobs=None, message=ChatCompletionMessage(content=None, refusal=None, role='assistant', annotations=None, audio=None, function_call=FunctionCall(arguments='{"num":100}', name='getPrimeinNumN'), tool_calls=None), content_filter_results={})], created=1746599568, model='gpt-4o', object='chat.completion', service_tier=None, system_fingerprint='fp_ee1d74bde0', usage=CompletionUsage(completion_tokens=18, prompt_tokens=71, total_tokens=89, completion_tokens_details=CompletionTokensDetails(accepted_prediction_tokens=None, audio_tokens=None, reasoning_tokens=None, rejected_prediction_tokens=None), prompt_tokens_details=PromptTokensDetails(audio_tokens=None, cached_tokens=None)), prompt_filter_results=[{'prompt_index': 0, 'content_filter_results': {'hate': {'filtered': False, 'severity': 'safe'}, 'self_harm': {'filtered': False, 'severity': 'safe'}, 'sexual': {'filtered': False, 'severity': 'safe'}, 'violence': {'filtered': False, 'severity': 'safe'}}}]

成功调用函数！
结果是： [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]


## 使用langchain.tools tool

> Entering new AgentExecutor chain...
To find the prime numbers within 100, I will use the tool that provides a list of prime numbers up to a given number.

Action: getPrimeinNumN_tool
Action Input: 100
Observation: 小于等于 100 的质数有: [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
Thought:I now know the final answer. 

Final Answer: 100以内的质数有: [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]

> Finished chain.

最终回答：
100以内的质数有: [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]

