import requests
from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel, Field
from fastapi_mcp import FastApiMCP
from langchain_community.utilities.requests import JsonRequestsWrapper
from typing import Dict, Union
from typing_extensions import Any
from langchain_core.tools import InjectedToolCallId
from typing import Annotated
from enum import StrEnum
from typing_extensions import Literal
from langchain_core.utils.pydantic import TypeBaseModel
from fastapi import Form
class ImgAugRequest(BaseModel):
    tool_call_id: Annotated[str, InjectedToolCallId]
    img_url: str = Body(..., description="需要进行图像增强处理的图片 URL", title='需要预处理进行图像增强的图片url地址')

class PrimeRequest(BaseModel):
    tool_call_id: Annotated[str, InjectedToolCallId]
    num:  int = Field(..., description="要获取的素数范围", title='要获取的素数范围')

app = FastAPI(title="MCP Proxy Server")
BASE_URL="http://127.0.0.1:7001"

@app.get("/hello")
def test():
    return {"message": "Hello, World!"}

@app.post("/img_aug", description="对图像进行各种增强处理")
async def img_aug(request: ImgAugRequest): 
    response = requests.post(
        f"{BASE_URL}/img_aug",
        # json={"img_url": request.img_url}
        json=request.img_url
    )
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    
@app.post("/primes", description="获取N以内的素数")
def getPrimesinN(limit: int):
    response = requests.get(f"{BASE_URL}/primes", params={"limit": limit})
    return response.json()

mcp = FastApiMCP(app)
mcp.mount(mount_path="/mcp")