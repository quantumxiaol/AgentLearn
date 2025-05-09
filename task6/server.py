from fastapi import FastAPI, Query, HTTPException
from typing import List
import uvicorn
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from MCPtool.testtool import getPrimeinNumN

app = FastAPI()

# 路由装饰器@app.get("/primes")
@app.get("/primes", response_model=list[int])
async def primes(limit: int = Query(..., description="查询指定范围内的质数")):
    if limit < 2:
        raise HTTPException(status_code=400, detail="Limit must be at least 2.")
    return getPrimeinNumN(limit)

# limit 参数是必需的（Query(...) 中的省略号表示必填字段），并且它应该是一个整数。
# 客户端需要通过查询参数的形式提供这个值（例如：/primes?limit=100）。

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)