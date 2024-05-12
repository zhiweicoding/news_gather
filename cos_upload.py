# -*- coding=utf-8
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
from qcloud_cos.cos_exception import CosClientError, CosServiceError
import sys
import os
import logging

# 正常情况日志级别使用 INFO，需要定位时可以修改为 DEBUG，此时 SDK 会打印和服务端的通信信息
logging.basicConfig(level=logging.INFO, stream=sys.stdout)

# 1. 设置用户属性, 包括 secret_id, secret_key, region 等。Appid 已在 CosConfig 中移除，请在参数 Bucket 中带上 Appid。Bucket 由
# BucketName-Appid 组成
secret_id = os.environ['COS_SECRET_ID']
secret_key = os.environ['COS_SECRET_KEY']   # 用户的 SecretKey，建议使用子账号密钥，授权遵循最小权限指引，降低使用风险。子账号密钥获取可参见 https://cloud.tencent.com/document/product/598/37140
region = None
                           # COS 支持的所有 region 列表参见 https://cloud.tencent.com/document/product/436/6224
token = None               # 如果使用永久密钥不需要填入 token，如果使用临时密钥需要填入，临时密钥生成和使用指引参见 https://cloud.tencent.com/document/product/436/14048
scheme = 'https'           # 指定使用 http/https 协议来访问 COS，默认为 https，可不填

endpoint = 'cos.accelerate.myqcloud.com'
config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Token=token, Scheme=scheme)
client = CosS3Client(config)

# 使用高级接口上传一次，不重试，此时没有使用断点续传的功能
response = client.upload_file(
    Bucket='examplebucket-1250000000',
    Key='exampleobject',
    LocalFilePath='local.txt',
    EnableMD5=False,
    progress_callback=None
)

# 使用高级接口断点续传，失败重试时不会上传已成功的分块(这里重试10次)
for i in range(0, 10):
    try:
        response = client.upload_file(
        Bucket='examplebucket-1250000000',
        Key='exampleobject',
        LocalFilePath='local.txt')
        break
    except CosClientError or CosServiceError as e:
        print(e)