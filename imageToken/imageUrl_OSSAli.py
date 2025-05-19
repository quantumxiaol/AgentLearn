# 将图片上传到阿里云的OSS，返回访问url。
# 创建OSS bucket，创建子账号，授权子账号读写，授权公共读
# https://{bucket-name}.oss-cn-beijing.aliyuncs.com/file-name

import oss2

import os,sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from readConfig import get_aliOss_config

access_key_id, access_key_secret, bucket_name = get_aliOss_config()
def upload_image(image_path,object_name, bucket_name, access_key_id, access_key_secret, endpoint='oss-cn-beijing.aliyuncs.com'):
    """上传图片
    :param image_path: 图片路径
    :param bucket_name: 阿里云OSS的bucket名称
    :param access_key_id: 阿里云OSS的access_key_id
    :param access_key_secret: 阿里云OSS的access_key_secret
    :param endpoint: 区域节点，如 oss-cn-beijing.aliyuncs.com
    """
    # image_path 形如  /Users/username/Desktop/image.png，image_name 只要image.png
    # image_name = os.path.basename(image_path)
    if object_name==None:
        object_name = os.path.basename(image_path)

    # 阿里云主账号AccessKey拥有所有API的访问权限，建议遵循最小权限原则，创建并使用RAM账号进行API访问。
    auth = oss2.Auth(access_key_id, access_key_secret)
    # 创建Bucket对象，指定Endpoint，以及Bucket名称
    bucket = oss2.Bucket(auth, 'http://oss-cn-beijing.aliyuncs.com', bucket_name)

    # 上传文件
    result = bucket.put_object_from_file(object_name, image_path)

    if result.status == 200:
        # 返回图片的访问URL
        return f"https://{bucket_name}.{endpoint}/{object_name}"
    else:
        raise Exception(f"Upload failed with status code {result.status}")
    
# 返回已有图片的url
def get_image_url(image_path,bucket_name, access_key_id, access_key_secret, endpoint='oss-cn-beijing.aliyuncs.com'):
    """获取图片的访问URL
    :param image_path: 图片路径
    :param bucket_name: 阿里云OSS的bucket名称
    :param access_key_id: 阿里云OSS的access_key_id
    :param access_key_secret: 阿里云OSS的access_key_secret
    """
    image_name = os.path.basename(image_path)
    auth = oss2.Auth(access_key_id, access_key_secret)
    bucket = oss2.Bucket(auth, 'http://oss-cn-beijing.aliyuncs.com', bucket_name)
    url = bucket.sign_url('GET', image_name, 3600)
    if url:
        url=url.split('?')[0]
        return url
    else :
        raise Exception("Failed to get image URL")

def image_exist(image_path,bucket_name, access_key_id, access_key_secret, endpoint='oss-cn-beijing.aliyuncs.com'):
    """
    判断图片是否已经存在
    :param image_path: 图片路径
    :param bucket_name: 阿里云OSS的bucket名称
    :param access_key_id: 阿里云OSS的access_key_id
    :param access_key_secret: 阿里云OSS的access_key_secret
    """
    image_name = os.path.basename(image_path)
    auth = oss2.Auth(access_key_id, access_key_secret)
    bucket = oss2.Bucket(auth, 'http://oss-cn-beijing.aliyuncs.com', bucket_name)
    result = bucket.object_exists(image_name)
    if result:
        return True
    
    return False