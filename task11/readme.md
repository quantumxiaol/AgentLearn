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