# 对Base64编码的图片进行处理，并返回处理后的图片
from PIL import Image
import base64
import io

import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from imageToken.imageUrl  import image_to_base64,base64_to_image,imageData_to_base64,open_image
# 将respond中的图片(base64)进行增强，返回增强后的图片(base64)
# 目前的增强只是按比例缩小图片，避免太大了

def aug_image_base64(image_base64):
    image = base64_to_image(image_base64)
    image = aug_image(image)
    return imageData_to_base64(image)

def aug_image(image_data):
    # 按长宽比例，将长边缩小到768以下（整数比例），短边按比例缩小
    width, height = image_data.size
    if width > height:
        new_width = 768
        new_height = int(height * (new_width / width))
    else:
        new_height = 768
        new_width = int(width * (new_height / height))
    
    image_data = image_data.resize((new_width, new_height), Image.Resampling.LANCZOS)


    return image_data

