# 目的
使用Langchain来处理图片
让LLM理解图片
返回理解的图片内容

# 概念
由于openai的官方文档中对图片参数的需求是统一资源定位符（URL），我们需要先将自己本地的图片通过一定方式转换成URL，再使用API调用

    message = HumanMessage(
        content=[
            {"type": "text", "text": "describe this image"},
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{image_data}"},
            },
        ],
    )


或者使用Base64编码。