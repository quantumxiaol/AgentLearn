from langchain.prompts import PromptTemplate
from langchain.prompts import ChatPromptTemplate
from langchain_community.llms import GPT4All
from langchain_openai import OpenAI, ChatOpenAI
from openai import OpenAI as OpenAIClient
from langchain_core.messages import HumanMessage, SystemMessage
from langchain.schema.runnable import RunnableSequence
import base64
import io
import yaml
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from imageToken.imageUrl import image_to_base64
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from readConfig import get_openai_config

def get_img_prompt_template():
    prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "Describe the image provided"),
        (
            "user",
            [
                {
                    "type": "image_url",
                    "image_url": {"url": "data:image/jpeg;base64,{img_url}"},
                }
            ],
        ),
    ]
    )
    return prompt

def get_img_prompt_template_v2():
    prompt_template = PromptTemplate(
        input_variables=["img_url"],
        template="""
        根据以下图片，描述图片并输出图片描述，图片使用Base64编码：
        "image_url": f"data:image/jpeg;base64,{img_url}"
        
        输出格式：
        图片描述:
        """
    )
    return prompt_template
def langchain_LLM(model,apikey,url, img_url):
    # 构造提示模板
    prompt_template = get_img_prompt_template()
    # prompt_template = get_img_prompt_template_v2()
    # 图片描述: {image_description}
    
    llm = ChatOpenAI(model=model, 
                 api_key=apikey,
                 openai_api_base=url,
                 timeout=120
                 )

    # 填充提示并生成结果
    # prompt = prompt_template.format(img_url=img_url)

    chain =prompt_template|llm
    response = chain.invoke({"img_url": img_url})


    return response
# OpenAI回答
def get_img_discribe(base64_image,client ,prompt):

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ]
    )

    # return response.choices[0].message.content
    return response


if __name__ == "__main__":
    img_path = "bus.jpg"

    model,api_key,api_base = get_openai_config()

    image_data = image_to_base64(img_path)

    # client = OpenAIClient(api_key=api_key, base_url=api_base)
    # response = get_img_discribe(image_data,client,"根据以下图片，描述图片并输出图片描述：。")


    response = langchain_LLM(model,api_key,api_base, image_data)

    print(response)


