import os, sys
from PIL import Image

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from readConfig import get_openai_config,get_aliOss_config
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from imageToken.imageUrl_OSSAli  import upload_image,get_image_url,image_exist


if __name__ == '__main__':
    path="test.jpg"
    access_key_id,access_key_secret,bucket_name=get_aliOss_config()
    url=upload_image(path,None,bucket_name,access_key_id,access_key_secret)
    print(url)
    res=image_exist(path,bucket_name,access_key_id,access_key_secret)
    print(res)
    image_url=get_image_url(path,bucket_name,access_key_id,access_key_secret)
    print(image_url)