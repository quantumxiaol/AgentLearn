import requests
import uuid
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from readConfig import get_testImageUrl

image_url=get_testImageUrl()

local_url='http://0.0.0.0:7002/img_aug'
request_body = {
    "tool_call_id": str(uuid.uuid4()),  # 生成一个随机的UUID作为tool_call_id
    "img_url": image_url
}
# response = requests.post(local_url, headers=headers, data=data)
response = requests.post(local_url, json=request_body)

print("local server")
print("Status Code:", response.status_code)
print("Response Body:", response.json())