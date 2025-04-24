import openai
from openai import OpenAI
import yaml
import os
import sys


# 旧版openai库
# def chat_with_model(prompt):
#     response = openai.ChatCompletion.create(
#         model="gpt-4o",  
#         messages=[
#             {"role": "system", "content": "你是一个有帮助的助手。"},
#             {"role": "user", "content": prompt}
#         ]
#     )
#     return response['choices'][0]['message']['content']

# 与模型交互



def chat_with_model(client,prompt):

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "你是一个有帮助的助手。"},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    # 获取当前脚本所在的目录
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # 获取上级目录
    parent_dir = os.path.dirname(current_dir)

    # 拼接 config.yaml 的完整路径
    config_path = os.path.join(parent_dir, "config.yaml")

    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
        # 获取 OpenAI 配置
    openai_config = config.get("OpenAI", {})
    model = openai_config.get("model")
    api_key = openai_config.get("api_key")
    api_base = openai_config.get("api_base")

    client = OpenAI(api_key=api_key, base_url=api_base)

    print("开始与 OpenAI 模型对话！输入 'exit' 来结束对话。")
    while True:
        user_input = input("您: ")
        if user_input.lower() in ["退出", "exit"]:
            print("对话结束。再见！")
            break
        response = chat_with_model(client,user_input)
        print(f"模型: {response}")

