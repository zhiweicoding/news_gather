# -*- coding=utf-8
import json

from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
from qcloud_cos.cos_exception import CosClientError, CosServiceError
import sys
import os
import logging
from fastapi import APIRouter
from entity.base_response import BaseResponse
import uuid
import requests
import tempfile
from entity.base_receive import UploadReceive

router = APIRouter()

# 正常情况日志级别使用 INFO，需要定位时可以修改为 DEBUG，此时 SDK 会打印和服务端的通信信息
logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)

secret_id = os.environ['COS_SECRET_ID']
secret_key = os.environ['COS_SECRET_KEY']
region = 'ap-guangzhou'
token = None
scheme = 'https'

domain = os.environ['COS_ENDPOINT']
bucket_name = os.environ['COS_BUCKET']
cdn_url = os.environ['COS_CDN_URL']
config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Token=token, Scheme=scheme)
client = CosS3Client(config)


@router.post("/")
async def init(upload_entity: UploadReceive):
    temp_path: str = download_file_to_temp(upload_entity.download_url, upload_entity.suffix)
    uuid_str: str = str(uuid.uuid1())
    print(f"temp_path: {temp_path}")
    upload_response = upload_file(temp_path, uuid_str + '.' + upload_entity.suffix,
                                  meta_data=dict(cell_id=upload_entity.cell_id))

    print(f"upload_response:{json.dumps(upload_response)}")

    return BaseResponse(code=200, message="success",
                        data=dict(url=cdn_url + uuid_str + "." + upload_entity.suffix)).json()


def download_file_to_temp(url: str, suffix: str):
    # 使用 requests 获取文件数据
    response = requests.get(url, stream=True)

    # 检查请求是否成功
    if response.status_code == 200:
        # 使用 tempfile 创建一个临时文件
        with tempfile.NamedTemporaryFile(delete=False, suffix='.' + suffix) as tmp_file:
            # 写入数据到临时文件
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:  # 过滤掉保持连接的新块
                    tmp_file.write(chunk)
            # 返回临时文件的路径
            return tmp_file.name
    else:
        print(f"Failed to download: status code {response.status_code}")
        return None


def upload_file(file_path: str, key: str, meta_data: dict = None):
    try:
        response = client.upload_file(
            Bucket=bucket_name,
            Key=key,
            LocalFilePath=file_path,
            Metadata=meta_data
        )
        return response
    except CosServiceError as e:
        print(e.get_error_code())
        print(e.get_error_msg())
        print(e.get_resource_location())
        return None
    except CosClientError as e:
        return None
