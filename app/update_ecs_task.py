"""
Overwrites target configuration of EventBridge.
By using put_target, you can configure InputTransformer which you cannot config on AWS Console.
"""
import boto3

config = configparser.ConfigParser()
config.read('config.ini')

REGION = config.get('AWS', 'REGION')

try:
    client = boto3.client("events")
    response = client.put_targets(
        Rule="human-action-recognition-event-rule",
        Targets=[
            {
                "Id": "1",
                "Arn": f"arn:aws:ecs:{REGION}:{}}:cluster/test-dev-cluster",
                "Arn": f"arn:aws:ecs:{REGION}:{}:cluster/test-dev-cluster",
                "RoleArn": "arn:aws:iam::963675165738:role/service-role/Amazon_EventBridge_Invoke_ECS_1604031748",
                "InputTransformer": {
                    "InputPathsMap": {
                        "keyname": "$.detail.requestParameters.key",
                        "eventname": "$.detail.eventName",
                    },
                    "InputTemplate": '{"containerOverrides": [{"name":"human-action-recognition-contianer","environment":[{"name":"EVENTNAME","value":<eventname>},{ "name":"S3_KEY","value":<keyname> }]}]}',
                },
                "EcsParameters": {
                    "TaskDefinitionArn": "arn:aws:ecs:us-west-1:963675165738:task-definition/human-action-recognition-task",
                    "TaskCount": 1,
                    "LaunchType": "FARGATE",
                    "NetworkConfiguration": {
                        "awsvpcConfiguration": {
                            "Subnets": ["suebnet-0b782f7d744a9f2c", "subnet-0e7a6e2063eb9c880"],
                            "SecurityGroups": ["sg-08c5c1ce710c75479"],
                            "AssignPublicIp": "ENABLED",
                        }
                    },
                },
            }
        ],
    )
except Exception as e:
    print(e)
