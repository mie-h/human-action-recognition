import os
import requests
import boto3
import botocore
from action_recognition import action_recognition

bucket = "human-action-recognition-bucket"
key = os.getenv("S3_KEY")

if not key:
    print("key is empty")
    exit()

key_input_path = os.path.split(key)[0]
video_name = os.path.split(key)[1]

local_dir = "./"
local_input_path = local_dir + video_name
s3_client = boto3.client('s3')
try:
    s3_client.download_file(bucket, key, local_input_path)
    print(f"Successfully downloaded object '{key}' from S3 bucket '{bucket}' to '{local_input_path}'.")
    object = s3_client.head_object(Bucket=bucket, Key=key)
    webhook_url = object["ResponseMetadata"]["HTTPHeaders"]["x-amz-meta-webhook_url"]
    print(f"Recieved webhook url : {webhook_url}")
except botocore.exceptions.ClientError as e:
    print(f"Error downloading object '{key}' from S3 bucket '{bucket}': {str(e)}")
    exit()


# call action recognition function
clip_len = 16
action_recognition(local_input_path, local_dir, clip_len)

# save the output video to S3
local_output_path = os.path.splitext(local_input_path)[0] + "_output.mp4"
key_output_path = "outputs/" + os.path.splitext(video_name)[0] + "_output.mp4"
try:
    print(f"upload file '{local_output_path}' to bucket '{bucket}' and key '{key_output_path}'")
    s3_client.upload_file(local_output_path, bucket, key_output_path)
    print(f"Successfully uploaded object '{local_output_path}' to S3 bucket '{bucket}' with key '{key_output_path}'.")
except botocore.exceptions.ClientError as e:
    print(f"Error uploading object '{local_output_path}' to S3 bucket '{bucket}': {str(e)}")
    exit()


# get presigned url to download an out put file and call webhook url
try:
    presignedurl = s3_client.generate_presigned_url('get_object',
                                                Params={'Bucket': bucket,
                                                        'Key': key_output_path},
                                                ExpiresIn=300)
except ClientError as e:
    print(f"Error generating presigend url to get object from S3 bucket '{bucket}' with key '{key_output_path}'. {e}")
    exit()

payload = {'presignedurl': presignedurl}
r = requests.get(webhook_url, params=payload)
print (r.status_code) 
