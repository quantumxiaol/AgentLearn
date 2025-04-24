from langchain.prompts import PromptTemplate
from langchain.prompts import ChatPromptTemplate
from langchain_community.llms import GPT4All
from langchain_openai import OpenAI, ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
import yaml
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import imageToken.imageTokenizer


def langchain_LLM(model,apikey,url, image_tokenizer):
    # 构造提示模板
    prompt_template = PromptTemplate(
        input_variables=["image_tokenizer"],
        template="""
        根据以下图片Token，描述图片并输出图片描述：。
        图片Token: {image_tokenizer}
        
        输出格式：
        图片描述:
        """
    )
    # 图片描述: {image_description}
    
    llm = ChatOpenAI(model=model, 
                 api_key=apikey,
                 openai_api_base=url,
                 timeout=120
                 )


    # 填充提示并生成结果
    prompt = prompt_template.format(image_tokenizer=image_tokenizer)

    # 计算token数
    token_count = len(prompt.split())
    # print(f"Token count: {token_count}")
    # print(prompt)
    response = llm.invoke(prompt)
    response=response.content


    return response

if __name__ == "__main__":
    img_path = "bus.jpg"

    # 获取当前脚本所在的目录
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # 获取上级目录
    parent_dir = os.path.dirname(current_dir)

    # 拼接 config.yaml 的完整路径
    config_path = os.path.join(parent_dir, "config.yaml")
    # 读取 config.yaml 文件
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
        # 获取 OpenAI 配置
    openai_config = config.get("OpenAI", {})
    model = openai_config.get("model")
    api_key = openai_config.get("api_key")
    api_base = openai_config.get("api_base")

    img=imageToken.imageTokenizer.preprocess_image(img_path)
    image_tokenizer = imageToken.imageTokenizer.imgTokenizer_quantize(img)
    
    imgdiscription = imageToken.imageTokenizer.imgToText(img)
    print(imgdiscription)

    # response = langchain_LLM(model,api_key,api_base, image_tokenizer)

    # print(response)


