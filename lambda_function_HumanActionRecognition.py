import os
import boto3
import botocore
from action_recognition import action_recognition

def lambda_handler(event, context):
    bucket = event["Records"][0]["s3"]["bucket"]["name"]
    key = event["Records"][0]["s3"]["object"]["key"]
    

    key_input_path = os.path.split(key)[0]
    video_name = os.path.split(key)[1]

    # download a video file from S3
    local_dir = "tmp/"
    # local_dir = "/tmp/"
    local_input_path = local_dir + video_name
    s3_client = boto3.client('s3')
    try:
        s3_client.download_file(bucket, key, local_input_path)
        print(f"Successfully downloaded object '{key}' from S3 bucket '{bucket}' to '{local_input_path}'.")
        object = s3_client.head_object(Bucket=bucket, Key=key)
        webhoook_url = ...
    except botocore.exceptions.ClientError as e:
        print(f"Error downloading object '{key}' from S3 bucket '{bucket}': {str(e)}")
        return
    except s3_client.exceptions.LimitExceedException as e:
        print("API call limit exceeded")
        return

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
        return
    except s3_client.exceptions.LimitExceedException as e:
        print("API call limit exceeded")
        return

    # call webhook url
    # r = requests.get(webhoook_url)

    # print(r.status_code)
    # print(r.text)

def main():
    bucket = "human-action-recognition-bucket"
    key = "inputs/raj-bb.mp4"
    event = {"Records": [{"s3": {"bucket": {"name": bucket}, "object": {"key": key}}}]}
    lambda_handler(event, None)

if __name__ == '__main__':
    main()