"""
Overwrites target configuration of EventBridge.
By using put_target, you can configure InputTransformer which you cannot config on AWS Console.
"""
import boto3
import json
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

RULE_NAME = config.get('AWS', 'RULE_NAME')
REGION = config.get('AWS', 'REGION')
ACCOUNT_ID = config.get('AWS', 'ACCOUNT_ID')
CLUSTER_NAME = config.get('AWS', 'CLUSTER_NAME')
SERVICE_ROLE_NAME = config.get('AWS', 'SERVICE_ROLE_NAME')
CONTAINER_NAME = config.get('AWS', 'CONTAINER_NAME')
TASK_DEFINITION = config.get('AWS', 'TASK_DEFINITION')
SUBNETS = json.loads(config.get('AWS', 'SUBNETS'))
SECURITY_GROUPS = json.loads(config.get('AWS', 'SECURITY_GROUPS'))

try:
    client = boto3.client("events")
    response = client.put_targets(
        Rule=RULE_NAME,
        Targets=[
            {
                "Id": "1",
                "Arn": f"arn:aws:ecs:{REGION}:{ACCOUNT_ID}:cluster/{CLUSTER_NAME}",
                "RoleArn": f"arn:aws:iam::{ACCOUNT_ID}:role/service-role/{SERVICE_ROLE_NAME}",
                "InputTransformer": {
                    "InputPathsMap": {
                        "keyname": "$.detail.requestParameters.key",
                        "eventname": "$.detail.eventName",
                    },
                    "InputTemplate": '{"containerOverrides": [{"name":"' + CONTAINER_NAME + '","environment":[{"name":"EVENTNAME","value":<eventname>},{ "name":"S3_KEY","value":<keyname> }]}]}',
                },
                "EcsParameters": {
                    "TaskDefinitionArn": f"arn:aws:ecs:{REGION}:{ACCOUNT_ID}:task-definition/{TASK_DEFINITION}",
                    "TaskCount": 1,
                    "LaunchType": "FARGATE",
                    "NetworkConfiguration": {
                        "awsvpcConfiguration": {
                            "Subnets": SUBNETS,
                            "SecurityGroups": SECURITY_GROUPS,
                            "AssignPublicIp": "ENABLED",
                        }
                    },
                },
            }
        ],
    )
except Exception as e:
    print("ERROR")
    print(e)
