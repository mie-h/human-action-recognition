"""
This file is not deployed to ECS. Use this if you want to make highly available ECS service.
Currently, ECS task is triggered and initialized for each S3 Put Object.
"""
import os
import boto3
import botocore
from action_recognition import action_recognition

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
"""
curl -X POST --url 'http://127.0.0.1:8000/predict' -d '{"bucket":"human-action-recognition-bucket", "key":"inputs/raj-bb.mp4"}' -H "Content-Type: application/json"
curl -X POST --url 'http://0.0.0.0:80/predict' -d '{"bucket":"human-action-recognition-bucket", "key":"inputs/raj-bb.mp4"}' -H "Content-Type: application/json"
"""
class Input(BaseModel):
    bucket: str
    key: str

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.post("/predict")
def predict_human_action(data: Input):
    data_dict = data.dict()
    bucket = data_dict['bucket']
    key = data_dict['key']

    key_input_path = os.path.split(key)[0]
    video_name = os.path.split(key)[1]

    local_dir = "./"
    local_input_path = local_dir + video_name
    s3_client = boto3.client('s3')
    try:
        s3_client.download_file(bucket, key, local_input_path)
        print(f"Successfully downloaded object '{key}' from S3 bucket '{bucket}' to '{local_input_path}'.")
        # TODO: webhook is not implemented. Learn more about how to implement on main.py file.
        webhoook_url = ...
    except botocore.exceptions.ClientError as e:
        print(f"Error downloading object '{key}' from S3 bucket '{bucket}': {str(e)}")
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
