# 目的
使用Langchain来调用Tool

# 概念
## function_call
是 OpenAI 的 Chat Completions API 中的一项特性，允许在与模型的对话中定义一些函数（functions），然后让模型根据用户的输入决定是否调用这些函数，并且可以将函数执行的结果返回给用户。这项功能使得语言模型不仅可以生成文本回复，还可以执行特定的任务，比如查询数据库、计算数学问题或调用外部API等。

    functions = [
        {
            "type": "function",
            "function": {
                "name": "getPrimeinNumN",
                "description": "获取小于等于给定数字的所有质数",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "num": {"type": "integer", "description": "要查询的上限数字"}
                    },
                    "required": ["num"],
                },
            }
        }
    ]

## LangChain的Tool
在 LangChain 中，Tool 是一种封装了某个具体功能（例如一个函数或API）的对象。它可以被语言模型理解并在适当的时候被调用。
Agent 是使用这些工具的主要实体。它接收用户输入，决定是否需要调用某个工具，并将工具返回的结果整合到最终的回答中。

定义工具函数get_prime_in_num_n(num)，返回小于等于 num 的所有质数列表。在定义工具函数时，尽量使用 Python 的类型提示来帮助 LangChain 更好地理解和解析参数。

使用 @tool 装饰器将函数包装成一个 LangChain 工具

    @tool
    def get_prime_in_num_n_tool(num: int) -> str:
        """返回小于等于 num 的所有质数。"""
        primes = get_prime_in_num_n(num)
        return f"小于等于 {num} 的质数有: {primes}"


