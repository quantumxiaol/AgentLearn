# 目的
使用url向LLM传递图片，使用[fastapi_mcp](https://github.com/tadata-org/fastapi_mcp)将fastapi server自动转为mcp server。
# 概念
这个库可以自动把api服务挂载成mcp tool。

    app = FastAPI()
    mcp = FastApiMCP(app)
    # Mount the MCP server directly to your FastAPI app
    mcp.mount()
# 运行

运行`python task11\task11_fastapiServer.py`创建api server，url为http://127.0.0.1:7001

运行`python task11\task11_mcpServerRun.py`把api server挂载为mcp server，url为l为http://127.0.0.1:7002/mcp

运行`python task11\task11_Client.py`测试LLM调用MCP tools。

运行`python task11\testFastapi.py`测试mcp server的接口情况。

# 结果
MCP tools有三个，['test_hello_get', 'img_aug_img_aug_post', 'getPrimesinN_primes_post']
可以使用getPrimesinN_primes_post返回素数，但是使用img_aug_img_aug_post会报错。
[详细输出](result.md)

task11\task11_Client.py输出

        MCP server连接成功
        MCP server session已建立
        MCP server session已初始化
        可用工具: ['test_hello_get', 'img_aug_img_aug_post', 'getPrimesinN_primes_post']
        Final answer: 1. 图片链接：您提供的图片链接是 [https://.com/bus.jpg](https://.com/bus.jpg)。
        1. 增强处理工具的调用：工具使用名称是 `functions.img_aug_img_aug_post`，通过该工具处理图片，输入的 `img_url` 参数也是 [https://.com/bus.jpg](https://.com/bus.jpg)。
        2. 关于MCP tool工具调用：
        - 使用的工具名称：`multi_tool_use.parallel`
        - 工具用途：允许并行调用多个工具。
        - 工具定义和参数说明：它包含多个工具调用，其中每个调用需要指定工具名称以及传递的参数。
        1. 200以内的素数：2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199。

        没有发生调用错误，所以无法提供详细的报错信息。在这个过程中，我使用了 `multi_tool_use.parallel` 来同时调用图片增强和素数计算的功能。

task11\task11_mcpServerRun.py后端输出

        INFO:     127.0.0.1:20603 - "POST /img_aug HTTP/1.1" 200 OK
        INFO:     127.0.0.1:20604 - "GET /primes?limit=200 HTTP/1.1" 200 OK