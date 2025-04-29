from PIL import Image
import io
import base64
import requests

# from imageToken.imageTokenizer import preprocess_image
# 将图像转换为 base64 编码的字符串
def image_to_base64(image_path):
    image = Image.open(image_path)
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    img_bytes = buffered.getvalue()
    base64_str = base64.b64encode(img_bytes).decode('utf-8')
    return base64_str

