# 目的
使用Langchain来调用Tool

    pip install mcp
    pip install mcp-server

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


## MCP
MCP（Model Context Protocol，模型上下文协议）是由Anthropic推出的开源协议，旨在实现大型语言模型（LLM）与外部数据源和工具的无缝集成，用来在大模型和数据源之间建立安全双向的链接。

目标是成为 AI 领域的“HTTP 协议”，推动 LLM 应用的标准化和去中心化


## MCP Server
供客户端访问提供特定功能或数据资源/工具/prompt模板。同时由于MCP Server自己控制资源，不用把 API 密钥给 MCP Host，因此更加安全

### 架构
MCP 遵循客户端-服务器架构，其中：

1、主机是发起连接的 LLM 应用程序（Claude for Desktop或其他 AI 工具）

2、客户端在主机应用程序内部与服务器保持 1：1 连接，负责协议通信

3、服务器供客户端访问，向客户提供上下文、工具和提示。同时由于MCP Server自己控制资源，不用把 API 密钥给 MCP Host，因此更加安全


### 资源
资源表示 MCP 服务器想要向客户端提供的任何类型的数据。这可以包括：文件内容、数据库记录、API 响应、实时系统数据、截图和图片、日志文件等更多内容。每个资源由唯一的 URI 标识，并且可以包含文本或二进制数据。

    {
    uri: string;           // Unique identifier for the resource
    name: string;          // Human-readable name
    description?: string;  // Optional description
    mimeType?: string;     // Optional MIME type
    }

### 提示
MCP 中的提示是预定义的模板，可以：接受动态参数、上下文、链接多个交互 、指导特定工作流程、表面作为 UI 元素（如斜线命令）

    {
    name: string;              // Unique identifier for the prompt
    description?: string;      // Human-readable description
    arguments?: [              // Optional list of arguments
        {
        name: string;          // Argument identifier
        description?: string;  // Argument description
        required?: boolean;    // Whether argument is required
        }
    ]
    }

### 工具
MCP 中的工具允许服务器公开可由客户端调用并由 LLM 用来执行操作的可执行函数。工具的关键方面包括：

1、发现tools/list：客户端可以通过端点列出可用的工具

2、调用：使用端点调用工具tools/call，服务器执行请求的操作并返回结果

3、灵活性：工具范围从简单的计算到复杂的 API 交互

与资源一样，工具也由唯一名称标识，并可以包含说明来指导其使用。但是，与资源不同的是，工具表示可以修改状态或与外部系统交互的动态操作。

    {
    name: string;          // Unique identifier for the tool
    description?: string;  // Human-readable description
    inputSchema: {         // JSON Schema for the tool's parameters
        type: "object",
        properties: { ... }  // Tool-specific parameters
    }
    }


以上内容来自腾讯工程师 wenqing、hans

MCP工具调用流程如下：

用户发送问题 -> LLM分析可用工具 -> 客户端通过MCP服务器来执行所选工具 -> 将结果发送回LLM -> LLM根据工具返回结果和用户问题进行回答