import os
import boto3
from botocore.exceptions import ClientError
import datetime

NAMESPACE = "Codeforge-AI Metrics"
AWS_PROFILE = os.environ.get("CODEFORGEAI_AWS_PROFILE") or "default"


def getCloudwatchClient():
    session = boto3.Session(profile_name=AWS_PROFILE)
    return session.client('cloudwatch', region_name='us-west-2')


def put_metric(metric_name, dimensions, value, unit):
    client = getCloudwatchClient()
    try:
        client.put_metric_data(
            Namespace=NAMESPACE,
            MetricData=[
                {
                    'MetricName': metric_name,
                    'Dimensions': dimensions,
                    'Value': value,
                    'Unit': unit
                }
            ],
        )

    except ClientError as e:
        print("Error putting metric data:", e)
        raise e
