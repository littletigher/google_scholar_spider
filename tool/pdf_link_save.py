import io

import requests
from minio import Minio
from minio.error import S3Error
from PIL import Image
import io
from dotenv import find_dotenv, load_dotenv
import os

# Load environment variables from .env file
env_dist = os.environ
load_dotenv(find_dotenv('.env'))
minio_url = env_dist.get('minio_url')  # e.g., 'play.min.io'
access_key =  env_dist.get('miaccess_key')
secret_key =  env_dist.get('misecret_key')
bucket_name =  env_dist.get('bucket_name')
# Initialize MinIO client
client = Minio(
    minio_url,
    access_key=access_key,
    secret_key=secret_key,
    secure=False  # Use False if the server does not support HTTPS
)

# Create a bucket if it doesn't exist
try:
    if not client.bucket_exists(bucket_name):
        client.make_bucket(bucket_name)
    print(f"Bucket '{bucket_name}' is ready.")
except S3Error as err:
    print(f"Error creating bucket: {err}")

# def save_to_local(file_path,file_save_path):
#     # send_headers = {
#     #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
#     #     "Connection": "keep-alive",
#     #     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
#     #     "Accept-Language": "zh-CN,zh;q=0.8"}
#     response = requests.get(file_path)
#     bytes_io = io.BytesIO(response.content)
#     with open(file_save_path, mode='wb') as f:
#         f.write(bytes_io.getvalue())
#         print('%s.PDF,下载成功！' % (file_save_path))

def save_to_local(file_path,file_save_path):
    with requests.get(file_save_path, stream=True) as r:
        r.raise_for_status()
        with open(file_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

# save pdf to minio
def save_to_minio(file_path, file_save_path):
    response = requests.get(file_path, stream=True)
    if response.status_code != 200:
        print(f"Failed to download PDF, status code: {response.status_code}")
        exit(1)
    try:
        # 使用BytesIO作为内存缓冲区来处理文件内容
        file_stream = io.BytesIO()
        for chunk in response.iter_content(chunk_size=8192):
            file_stream.write(chunk)
        # 重置缓冲区指针到开始位置，以便于再次读取
        file_stream.seek(0)

        # 直接从内存缓冲区上传到MinIO
        client.put_object(bucket_name, file_save_path, file_stream, length=int(response.headers['Content-Length']),
                          content_type=response.headers['Content-Type'])
        print(f"Successfully uploaded PDF from {file_path} to {bucket_name}/{file_save_path}")
    except S3Error as err:
        print(f"Error occurred while uploading to MinIO: {err}")
    finally:
        # 清理，关闭文件流
        file_stream.close()
    # print('文件上传成功！')
