# 目的
使用C/S模式，到时候可以让Agent在后台，前端显示输出。
# 概念
FastAPI 是一个现代、快速（高性能）的 Web 框架，用于构建 API。

Uvicorn 是一个用于运行 ASGI (Asynchronous Server Gateway Interface) 应用的超高速服务器。

Flask 是一个用 Python 编写的轻量级 WSGI（Web Server Gateway Interface）Web 应用框架。
## FastAPI的@app 装饰器
### @app.get()
处理 HTTP GET 请求。

    @app.get("/")
    def read_root():
        return {"message": "Hello, World!"}
当用户访问根路径 / 时，返回一个 JSON 响应 {"message": "Hello, World!"}。

### @app.post()
处理 HTTP POST 请求，通常用于提交数据。

    from fastapi import Body

    @app.post("/items/")
    async def create_item(item: dict = Body(...)):
        return {"item": item}
接收客户端发送的一个 JSON 对象，并将其作为响应的一部分返回。
### @app.put()
处理 HTTP PUT 请求，通常用于更新已有资源。

    @app.put("/items/{item_id}")
    async def update_item(item_id: int, item: dict):
        return {"item_id": item_id, "updated_item": item}
### @app.delete()
处理 HTTP DELETE 请求，用于删除资源。

    @app.delete("/items/{item_id}")
    async def delete_item(item_id: int):
        return {"message": f"Item {item_id} deleted"}
### 路径参数 {variable_name}
在 URL 中定义变量部分，可以接收动态值。

    @app.get("/items/{item_id}")
    async def read_item(item_id: int):
        return {"item_id": item_id}
### 查询参数 Query()
从 URL 查询字符串中提取参数。

    from fastapi import Query

    @app.get("/items/")
    async def read_items(q: str = Query(None, max_length=50)):
        return {"q": q}
### 请求体 Body()
从请求体中提取数据，常用于 POST 和 PUT 请求。

### 响应模型 response_model
指定 API 的响应格式，帮助自动验证和序列化响应数据。

    from typing import List

    @app.get("/items/", response_model=List[Item])
    async def read_items():
        return [{"name": "Foo", "description": "A Foo Item"}]
### 依赖注入 Depends()
用于依赖注入，例如身份验证、数据库连接等。

    from fastapi import Depends

    async def common_parameters(q: str = None, skip: int = 0, limit: int = 10):
        return {"q": q, "skip": skip, "limit": limit}

    @app.get("/items/")
    async def read_items(commons: dict = Depends(common_parameters)):
        return commons
## 使用方法
每个装饰器都需要指定一个路径作为其第一个参数。可以使用标准的 URL 模式，也可以包含路径参数。例如，@app.get("/items/{item_id}") 定义了一个接受动态 item_id 的 GET 路由。

## 作用
这些装饰器的主要作用是简化 Web 应用程序的开发流程，通过声明式的语法定义 HTTP 路由及其处理逻辑。它们不仅提高了代码的可读性，还使得 FastAPI 可以自动生成交互式的 API 文档（如 Swagger UI 和 ReDoc），这大大方便了 API 的测试和调试工作。


# 运行
## FastAPI
运行`python ./task6/server.py`创建服务端，运行`curl "http://127.0.0.1:8000/primes?limit=100"`测试接收，或者新开终端运行`python ./task6/client.py`。

运行[结果](result.md)

## Flask
运行`python ./task6/flaskServer.py`创建服务端，运行`curl "http://127.0.0.1:5000/primes?limit=100"`测试接收