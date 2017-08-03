'''
Created on Oct 8, 2015

@author: mentzera

Modifications
08/01/2017 JMT added code to set default encoding to UTF8
'''

import json
import boto3
import twitter_to_es

# the next 3 lines change default encoding to UTF-8
import sys
reload(sys)
sys.setdefaultencoding('UTF8')


s3 = boto3.client('s3')

def lambda_handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))

    # Get the object from the event and show its content type
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    # Getting s3 object
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
              
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e
    
    # Parse s3 object content (JSON)
    try:
        s3_file_content = response['Body'].read()
        #clean trailing comma
        if s3_file_content.endswith(',\n'):
            s3_file_content = s3_file_content[:-2]
        tweets_str = '['+s3_file_content+']'
        tweets = json.loads(tweets_str)
   
    except Exception as e:
        print(e)
        print('Error loading json from object {} in bucket {}'.format(key, bucket))
        raise e
    
    # Load data into ES
    try:
        twitter_to_es.load(tweets)

    except Exception as e:
        print(e)
        print('Error loading data into ElasticSearch')
        raise e    
