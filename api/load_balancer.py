import os
import boto3
import json
from decouple import config
import time
RESPONSE_QUEUE_NAME = 'responsequeue.fifo'
REQUEST_QUEUE_NAME = 'requestqueue.fifo'
INPUT_BUCKET = 'inputbucketskale9'

sqs = boto3.client('sqs', 
                    region_name='us-east-1', 
                    aws_access_key_id=config('ACCESS_ID'),
                    aws_secret_access_key= config('ACCESS_KEY'))

response = sqs.get_queue_url(QueueName=REQUEST_QUEUE_NAME)
queue_url = str(response['QueueUrl'])


while True:
    approximateNumberOfMessages = 0
    for i in range(3):
        response = sqs.get_queue_attributes(
            QueueUrl= queue_url,
            AttributeNames=[
                'ApproximateNumberOfMessages',
            ]
        )
        approximateNumberOfMessages += int(response['Attributes']['ApproximateNumberOfMessages'])
        time.sleep(0.1)
    approximateNumberOfMessages = int(approximateNumberOfMessages/3)
    print(approximateNumberOfMessages)