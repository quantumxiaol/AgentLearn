from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from MCPtool.imagetool import aug_image_base64

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from readConfig import get_openai_config

# Initialize FastMCP server
mcp = FastMCP("Image Tools", version="1.1.4514")

# 工具
#mcp.tool() 将函数注册为 mcp tool 工具
@mcp.tool(
    name='ResizeBase64Image',
    description='把图像长边缩小至768，短边等比缩小，输入输出都是Base64'
)
def ResizeImage_base64_Mcptool(image:str) -> Any:
    print("调用了 ResizeBase64Image 工具，参数 image =", image)
    return aug_image_base64(image)

@mcp.tool(
    name='ResizeImage_urlImage',
    description='把图像长边变为接近768，短边等比变换，输入为url的图片'
)
def ResizeImage_urlImage_Mcptool(image:str) -> Any:
    print("调用了 ResizeUrlImage 工具，参数 image =", image)
    # return aug_image_base64(image)
    pass

if __name__ == "__main__":
    mcp.run(transport="stdio")