import json
import boto3
import botocore


def lambda_handler(event, context):
    # Create an S3 client
    s3 = boto3.client("s3")
    api_gateway_request = False

    input_dir = "inputs/"
    params = event.get("queryStringParameters")
    if not params:
        video_id = event.get("video_id")
        webhook_url = event.get("webhook_url")

    else:
        video_id = params.get("video_id")
        webhook_url = params.get("webhook_url")
        api_gateway_request = True
    if not video_id:
        print("video id is empty")
        return
    if not webhook_url:
        print("webhook_url is empty")
        return
    # Specify the S3 bucket and object key
    bucket_name = "human-action-recognition-bucket"
    object_key = input_dir + video_id
    fields = {
        "x-amz-meta-webhook_url": webhook_url,
    }
    conditions = [{"x-amz-meta-webhook_url": webhook_url}]

    # Generate a pre-signed URL for uploading the object
    try:
        payload = s3.generate_presigned_post(
            Bucket=bucket_name,
            Key=object_key,
            Fields=fields,
            Conditions=conditions,
            ExpiresIn=1000,  # Expiration time in seconds
        )
        print("Pre-signed URL generated successfully:")
        print(payload)
    except botocore.exceptions.ClientError as e:
        print("Error generating pre-signed URL:", str(e))

    if api_gateway_request:
        http_response = {}
        http_response["statusCode"] = 200
        http_response["headers"] = {}
        http_response["headers"]["Content-Type"] = "application/json"
        http_response["body"] = json.dumps({"payload": payload})
        return http_response
    else:
        return payload
