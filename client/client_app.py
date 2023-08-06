import boto3
import botocore
import configparser
import json
import requests
import shutil
from fastapi import FastAPI

app = FastAPI()

config = configparser.ConfigParser()
config.read('config.ini')


@app.get("/")
def root():
    return {"welcome.": "client app"}


@app.get("/upload")
def upload_video(video_name: str):
    lambda_client = boto3.client("lambda")

    webhook_url = config.get('URL', 'WEBHOOK_URL')
    payload = {"video_id": video_name, "webhook_url": webhook_url}
    apigateway_url = config.get('URL', 'APIGATEWAY_URL')

    response = requests.get(apigateway_url, params=payload)
    print(response)

    content = json.loads(response.text)
    print(content["url"])
    url_s3presignedurl = content["url"]["url"]
    fields = content["url"]["fields"]

    local_video_path = video_name
    input_videos = {"file": open(local_video_path, "rb")}
    r = requests.post(url_s3presignedurl, data=fields, files=input_videos)

    print(r.status_code)
    print(r.text)


@app.get("/postprocessing")
def post_processing(presignedurl: str):
    if not presignedurl:
        print("presigned url is empty")
        return
    print(f"Recieved presigned url {presignedurl}")
    response = requests.get(presignedurl)
    if response.status_code == 200:
        with open(config.get('FILES', 'OUTPUT_VIDEO_FILE'), "wb") as f:
            f.write(response.content) 