'''
Created on Oct 8, 2015

@author: mentzera
'''

import json
import boto3
import config
import twitter_to_es
from elasticsearch import Elasticsearch

def create_index(es,index_name,mapping):
    print('creating index {}...'.format(index_name))
    mapping_dict = {'mapping': mapping}
    mapping_str = str(mapping_dict)
    print json.dumps(mapping_dict)
    mapping_dict = "{\"mappings\":{\"logs_june\":{\"_timestamp\": {\"enabled\": \"true\"},\"properties\":{\"logdate\":{\"type\":\"date\",\"format\":\"dd/MM/yyy HH:mm:ss\"}}}}}"
#     es.indices.create(index_name, body = json.dumps(mapping_dict))
    es.indices.create(index_name, body = {'mappings': mapping})
    print {'mapping': mapping}
    
bucket = 'mentzera'
key = 'twitter/2015/10/16/14/twitter-stream-1-2015-10-16-14-21-36-7e019a27-7b3d-47d5-8805-344832c67be4'
key = 'twitter/2015/10/20/20/twitter-stream-1-2015-10-20-20-23-33-8f39af04-ee9f-45d6-a2da-06dc068f0c15'
s3 = boto3.client('s3')
response = s3.get_object(Bucket=bucket, Key=key)
s3_file_content = response['Body'].read()
#clean trailing comma
if s3_file_content.endswith(',\n'):
    s3_file_content = s3_file_content[:-2]
tweets_str = '['+s3_file_content+']'
# tweets_str = '['+response['Body'].read().replace('}{','},\n{')+']'
# with open("/tmp/1.txt", "w") as text_file:
#     text_file.write(tweets_str)

tweets = json.loads(tweets_str)
print len(tweets)

twitter_to_es.load(tweets)
