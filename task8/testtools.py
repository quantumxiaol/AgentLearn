# 测试MCPtool\imagetool.py中的工具是否能够正常使用。
from PIL import Image
import base64
import io

import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from MCPtool.imagetool import aug_image, aug_image_base64,open_image
from imageToken.imageUrl  import image_to_base64,base64_to_image,imageData_to_base64

image_data = open_image("test.jpg")
image_data_base64 = imageData_to_base64(image_data)
image_data_base64_aug = aug_image_base64(image_data_base64)
image_data_aug = base64_to_image(image_data_base64_aug)

image_data_aug.save("aug_image.jpg")
image_data_aug.show()
image_data.show()