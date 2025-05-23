# 结果

>MCP server连接成功
MCP server session已建立
MCP server session已初始化
可用工具: ['test_hello_get', 'img_aug_img_aug_post', 'getPrimesinN_primes_post']
Final answer: 描述图片内容：
图片中展示了一辆带有"EMT Madrid"标识的电动巴士，巴士主体为蓝色并有白色文字和标识。车身上有“cero emisiones”的字样，表明该车为零排放车辆，车头显示路线为"M1 SOL SEVILLA"。巴士在街道上停放，旁边有人行走。
关于增强处理工具的调用：
- 工具名称：`img_aug_img_aug_post`
- 使用参数：`{"img_url":"https://tts-cdn.voicedream.com/voi/vtks/4bb324219d5d13beb1ae198d67e94512.aac", "tool_call_id":"增强处理请求"}`
- 报错信息：调用失败，状态码422，错误信息详述了一个类型错误，`img_url`应该是一个有效的字符串。
200以内的素数：
- [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199]

>fastapi server的输出为
INFO:     127.0.0.1:7168 - "POST /img_aug HTTP/1.1" 422 Unprocessable Entity
INFO:     127.0.0.1:7169 - "GET /primes?limit=200 HTTP/1.1" 200 OK

这说明LLM能够使用素数这个工具，而不能使用图片增强。可能是因为素数在HumanMessage明确给出，而img_url并不是明确给出的。prompt使用有误，原来的prompt为：

        message = HumanMessage(
            content=[
                {"type": "text", "text": "请帮我描述下面图片中的内容"},
                {"type": "text", "text": "然后请帮我把这张图片增强处理一下，返回图片"},        
                {"type": "text", "text": "请告诉我输入给你的图片链接，以及你通过mcp tool工具调用的图片链接"}, 
                {"type": "text", "text": "现在MCP tool有些问题，你先告诉我你得到的和mcp有关的全部信息，特别是工具定义和参数说明，以帮助我调试分析问题"},  
                {"type": "text", "text": "请告诉我200以内的素数有哪些"},
                {"type": "text", "text": "如果调用MCP tool工具有错，返回详细的报错信息，特别是你试图使用什么MCP tool，又是如何使用的？"},
                {"type": "image_url", "image_url": {"url": image_url}},
            ]
        )

这样无法让LLM了解如何使用mcp tool。

我又让LLM输出Mcp工具的使用方法。

>LLM 输出：
可用工具: ['test_hello_get', 'img_aug_img_aug_post', 'getPrimesinN_primes_post']
Final answer: ### Image Description
The image depicts a city street with a modern electric minibus from the EMT Madrid service. The bus is decorated with signs indicating it is an environmentally friendly option, featuring phrases like "cero emisiones" (zero emissions). The background consists of a traditional European building with balconies and green shutters.
Image Enhancement Error
There was an error when attempting to enhance the image using the `img_aug_img_aug_post` tool. The error message was:
```
Error calling img_aug_img_aug_post. Status code: 422. Response: {"detail":"{\"detail\":[{\"type\":\"string_type\",\"loc\":[\"body\"],\"msg\":\"Input should be a valid string\",\"input\":{\"img_url\":\"https://example.com/image\"}}]}"}
Please fix your mistakes.
```
It seems that there was an issue with the image URL format provided not being a valid string as expected by the tool.
Prime Numbers up to 200
The prime numbers up to 200 are:
[2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199].

>mcp server 输出
Error calling img_aug_img_aug_post
Traceback (most recent call last):
  File "C:\Users\liuxi\anaconda3\envs\yolo\Lib\site-packages\fastapi_mcp\server.py", line 435, in _execute_api_tool
    raise Exception(
Exception: Error calling img_aug_img_aug_post. Status code: 422. Response: {"detail":"{\"detail\":[{\"type\":\"string_type\",\"loc\":[\"body\"],\"msg\":\"Input should be a valid string\",\"input\":{\"img_url\":\"https://example.com/image\"}}]}"}
INFO:     127.0.0.1:7261 - "POST /mcp/messages/?session_id=f9664a8556f44bd88b1d250db1b6dec5 HTTP/1.1" 202 Accepted

>fastapi server 输出
INFO:     127.0.0.1:7262 - "POST /img_aug HTTP/1.1" 422 Unprocessable Entity
INFO:     127.0.0.1:7263 - "GET /primes?limit=200 HTTP/1.1" 200 OK

这说明LLM调用MCP tools失败，原因是LLM调用时传递的url是错误的。

如果不检测url，做空逻辑。会报Input should be a valid string。
>LLM输出：
传入的图片URL是：https://cdn.discordapp.com/attachments/1103845294727391308/1168307992971376781/WhatsApp_Image_2023-10-24_at_18.36.09.jpeg?ex=65573469&is=6534e369&hm=b9ff84ca2fd5786004011050e6f7f27fc91b239188d67e6d80a048c7ad4ad882&

>mcp server 输出：
Error calling img_aug_img_aug_post
Traceback (most recent call last):
  File "C:\Users\liuxi\anaconda3\envs\yolo\Lib\site-packages\fastapi_mcp\server.py", line 435, in _execute_api_tool
    raise Exception(
Exception: Error calling img_aug_img_aug_post. Status code: 422. Response: {"detail":"{\"detail\":[{\"type\":\"string_type\",\"loc\":[\"body\"],\"msg\":\"Input should be a valid string\",\"input\":{\"img_url\":\"https://cdn.discordapp.com/attachments/1103845294727391308/1168307992971376781/WhatsApp_Image_2023-10-24_at_18.36.09.jpeg?ex=65573469&is=6534e369&hm=b9ff84ca2fd5786004011050e6f7f27fc91b239188d67e6d80a048c7ad4ad882&\"}}]}"}

请求有些问题，现在改过来了。
如果不判断url的有效性，LLM可以调用工具，尽管传入的参数是错误的。

>LLM 输出
描述图片内容：
图片中显示了一条城市街道，上面有一个白色和蓝色相间的公共交通电动车，车辆上写有"cero emisiones"（零排放）标志，提示其为一辆电动车。背景中是一个黄色的建筑物，并且街道上有树、几根交通标志杆，以及行人正在走路。
图片增强处理结果：
我已经通过工具调用对图片进行了增强处理，调用使用的工具是`functions.img_aug_img_aug_post`，传入的参数分别是`img_url`为`https://image.url/path/to/photo.jpg`，`tool_call_id`为`123abc`。
200以内的素数：
200以内的素数有：2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199。

还是可以找到工具，就是调用有问题。需要改prompt。