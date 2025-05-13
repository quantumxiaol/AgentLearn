from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from MCPtool.testtool import getPrimeinNumN

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from readConfig import get_openai_config

# Initialize FastMCP server
mcp = FastMCP("PrimeGet", version="1.1.4514")

# 工具
#mcp.tool() 将函数注册为 mcp tool 工具
@mcp.tool(
    name='getPrimes',
    description='寻找正整数N以内的质数'
)
def getPrimeinNumN_Mcptool(n: int) -> Any:
    print("调用了 getPrimes 工具，参数 n =", n)
    return getPrimeinNumN(n)

if __name__ == "__main__":
    mcp.run(transport="stdio")