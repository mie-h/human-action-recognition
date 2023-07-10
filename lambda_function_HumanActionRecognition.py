def lambda_handler(event, context):
    bucket = event["Records"][0]["s3"]["bucket"]["name"]
    key = event["Records"][0]["s3"]["object"]["key"]
    webhoook_utl = ...

    # download a video file from S3

    # call action recognition function

    # save the output video to S3

    # call webhook url
