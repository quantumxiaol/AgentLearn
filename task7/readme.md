# 目的
使用MCP tools

    pip install mcp
    pip install mcp-server
    pip install langchain-mcp-adapters

# 概念
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

# 运行
在一个终端运行`python task7\task7_mcpServer.py`

在另一个终端运行`python task7\task7_langchainClient.py`