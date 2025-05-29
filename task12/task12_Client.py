import requests

# 设置服务端地址
url = "http://127.0.0.1:1145/ask"

def ask_question(question: str):
    """
    发送问题到服务端，并获取回答。
    
    :param question: 用户提出的问题
    :return: 服务端返回的回答
    """
    payload = {
        "question": question
    }
    
    try:
        # 发送POST请求
        response = requests.post(url, json=payload)
        
        # 检查响应状态码
        if response.status_code == 200:
            answer = response.json().get("answer")
            print(f"Answer: {answer}")
        else:
            print(f"Error: Received status code {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.RequestException as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    # 示例问题
    # question = input("请输入您的问题：")
    question ="东海帝王的特殊称号如何获取？"
    ask_question(question)