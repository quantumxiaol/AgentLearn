# 结果

## LLM OpenAI 回答

使用PromptTemplate

content='图片描述: 图片中心是一只正在享用巧克力的猫咪，画面背景以绿色的植物为主，显得生机盎然。猫咪旁边放置了一些未打开的巧克力盒，周围环境清新自然，仿佛是
春天的午后。猫咪的姿态显得非常悠闲，尾巴轻轻甩动，给人一种愉悦的感觉。' additional_kwargs={'refusal': None} response_metadata={'token_usage': {'completion_tokens': 97, 'prompt_tokens': 13158, 'total_tokens': 13255, 'completion_tokens_details': {'accepted_prediction_tokens': None, 'audio_tokens': None, 'reasoning_tokens': None, 'rejected_prediction_tokens': None}, 'prompt_tokens_details': {'audio_tokens': None, 'cached_tokens': None}}, 'model_name': 'gpt-4o', 'system_fingerprint': 'fp_ee1d74bde0', 'id': 'chatcmpl-BRVS9xvUxbBIZV8Bdpuk86epwvQye', 'finish_reason': 'stop', 'logprobs': None} id='run-7937c733-e6c2-437d-b75b-ec89842881df-0' usage_metadata={'input_tokens': 13158, 'output_tokens': 97, 'total_tokens': 13255, 'input_token_details': {}, 'output_token_details': 
{}}

我的测试图片是yolo自带的测试图片bus.jpg，不知道怎么能变成猫咪；变成Base64输入的Token也太高了，因为这个图片是用Base64编码的放进去的，而且也没能理解内容。

使用prompt = ChatPromptTemplate.from_messages

'The image shows a small electric bus with a blue and white design, labeled as part of the EMT (Empresa Municipal de Transportes) in Madrid, indicating it operates on the M1 line connecting Sol and Sevilla. The bus has a label that reads "cero emisiones," highlighting its zero-emission attribute. The 
side of the bus features a graphic incorporating a green leaf and the phrase "movidos por electricamEMT" which translates to "moved by electric EMT," suggesting its environmentally friendly operation. The bus is parked on a street beside a yellow residential building with balconies. There are people walking on the sidewalk, dressed in casual winter clothing, such as coats and sneakers. The setting appears to be a sunny day with some shadows cast on the pavement, and there\'s a small tree with green leaves visible on the side of the street.

'input_tokens': 800, 'output_tokens': 169, 'total_tokens': 969


## OpenAI 回答
图片展示了一辆印有“cero emisiones”（零排放）的蓝色公交车，侧面标记为“EMT Madrid”，说明这是马德里的电动公交车。车身外观现代，车窗上还有环保标志。背景是一栋黄色建筑，带有绿门窗和阳台。人行道上行人穿着休闲服装正在走过，阳光明媚照映在场景中。
prompt_tokens=815, total_tokens=950
这个结果是正常的

使用url访问图片

>content='The image shows a street scene in an urban area, specifically in Madrid, Spain. Prominently displayed is an electric public transport vehicle, a bus operated by EMT Madrid. The bus is branded with the words "cero emisiones," which translates to "zero emissions," indicating that it is environmentally friendly. The design includes green leaf imagery alongside the text "electricam EMT," further emphasizing its eco-friendly nature. The bus route is marked as "M1 Sol/Sevilla" on its destination display. \n\nThe street is paved and there are pedestrians walking along the sidewalk. The weather appears to be sunny, as indicated by the shadows and the people’s clothing, which consists of casual attire suitable for mild weather. In the 
background, the facade of a building is visible, showcasing typical Spanish architecture with features such as balconies and tall windows. The traffic sign, partially visible, suggests there might be restrictions or information relevant to the location. Overall, the scene conveys a modern urban environment that is increasingly focused on sustainability.' additional_kwargs={'refusal': None} response_metadata={'token_usage': {'completion_tokens': 203, 'prompt_tokens': 800, 'total_tokens': 1003, 'completion_tokens_details': {'accepted_prediction_tokens': None, 'audio_tokens': None, 'reasoning_tokens': None, 'rejected_prediction_tokens': None}, 
usage_metadata={'input_tokens': 800, 'output_tokens': 203, 'total_tokens': 1003, 'input_token_details': {}, 'output_token_details': {}}