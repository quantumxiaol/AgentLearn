from fastapi import FastAPI, Query, HTTPException,Body
from typing import List
import uvicorn
import os
import sys
import urllib.request
from urllib.error import HTTPError, URLError

def getPrimeinNumN(num):
    """
    This function returns a list of prime numbers up to the given number.
    """
    num = int(num)  
    def is_prime(n):
        if n < 2:
            return False
        for i in range(2, int(n ** 0.5) + 1):
            if n % i == 0:
                return False
        return True
    return [n for n in range(2, num + 1) if is_prime(n)]

def img_augment(image_url: str)-> str:
    """
    This function takes an image as input and returns the augmented image.
    """
    # Add your image augmentation logic here
    return image_url


app = FastAPI()

# 路由装饰器@app.get("/primes")
@app.post("/img_aug", response_model=str)
async def img_aug(image_url: str = Body(..., description="需要进行图像增强处理的图片 URL", title='需要预处理进行图像增强的图片url地址')):
    # 访问image_url，不能访问报错（路径不存在）。
    try:
        response = urllib.request.urlopen(image_url)
    except HTTPError as e:
        print("HTTP Error:", e.code, e.reason)
    except URLError as e:
        print("URL Error:", e.reason)
    return img_augment(image_url)


# limit 参数是必需的（Query(...) 中的省略号表示必填字段），并且它应该是一个整数。
# 客户端需要通过查询参数的形式提供这个值（例如：/primes?limit=100）。
@app.get("/primes", response_model=list[int])
async def primes(limit: int = Query(..., description="查询指定范围内的质数")):
    if limit < 2:
        raise HTTPException(status_code=400, detail="Limit must be at least 2.")
    return getPrimeinNumN(limit)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=7001)