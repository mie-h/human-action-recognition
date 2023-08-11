"""
Main application file. This is the entry point of triggered and initialized ECS task.

To test locally, set a path to an input file to environmental variable S3_KEY and run main.py.
"""
import os
import sys
import requests
import boto3
import botocore
import configparser
from action_recognition import action_recognition


def download_input(s3_client, bucket, key, local_input_path):
    """Downloads an input video from S3 bucket and get webhook url from S3 metadata of the input video object.
    returns webhook url
    """
    try:
        s3_client.download_file(bucket, key, local_input_path)
        print(f"Successfully downloaded object '{key}' from S3 bucket '{bucket}' to '{local_input_path}'.")
        object = s3_client.head_object(Bucket=bucket, Key=key)
        webhook_url = object["ResponseMetadata"]["HTTPHeaders"]["x-amz-meta-webhook_url"]
        print(f"Recieved webhook url : {webhook_url}")
    except botocore.exceptions.ClientError as e:
        print(f"Error downloading object '{key}' from S3 bucket '{bucket}': {str(e)}")
        sys.exit(1)
        return
    return webhook_url


def upload_output(s3_client, local_input_path, video_name, bucket):
    """Save the output video to S3
    returns path to the output file in S3
    """
    local_output_path = os.path.splitext(local_input_path)[0] + "-output.mp4"
    key_output_path = "outputs/" + os.path.splitext(video_name)[0] + "-output.mp4"
    try:
        print(f"upload file '{local_output_path}' to bucket '{bucket}' and key '{key_output_path}'")
        s3_client.upload_file(local_output_path, bucket, key_output_path)
        print(f"Successfully uploaded object '{local_output_path}' to S3 bucket '{bucket}' with key '{key_output_path}'.")
    except botocore.exceptions.ClientError as e:
        print(f"Error uploading object '{local_output_path}' to S3 bucket '{bucket}': {str(e)}")
        sys.exit(1)
    return key_output_path


def get_presignedurl_download(s3_client, bucket, key_output_path):
    """Get presigned url to download an output file and call webhook url
    """
    try:
        presignedurl = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket,
                                                            'Key': key_output_path},
                                                    ExpiresIn=300)
    except ClientError as e:
        print(f"Error generating presigend url to get object from S3 bucket '{bucket}' with key '{key_output_path}'. {e}")
        sys.exit(1)
    return presignedurl


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('config.ini')

    bucket = config.get('AWS', 'BUCKET')
    key = os.getenv("S3_KEY")    # get key from ECS env. variable

    if not key:
        print("key is empty")
        sys.exit(1)

    key_input_path = os.path.split(key)[0]
    video_name = os.path.split(key)[1]

    local_dir = config.get('DIR', 'LOCAL_DIR')
    local_input_path = local_dir + video_name
    s3_client = boto3.client('s3')

    webhook_url = download_input(s3_client, bucket, key, local_input_path)

    # call action recognition function
    clip_len = 16
    action_recognition(local_input_path, local_dir, clip_len)

    key_output_path = upload_output(s3_client, local_input_path, video_name, bucket)

    presignedurl = get_presignedurl_download(s3_client, bucket, key_output_path)

    payload = {'presignedurl': presignedurl}
    r = requests.get(webhook_url, params=payload)
    print(r.status_code) 
