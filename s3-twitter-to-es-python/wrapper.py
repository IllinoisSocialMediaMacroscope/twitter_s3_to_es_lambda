'''
Created on Oct 8, 2015

@author: mentzera

Modifications
07/31/2017 JMT	change default encoding to UTF-8
'''

import json
import boto3
import config
import twitter_to_es
from elasticsearch import Elasticsearch

# the next 3 lines change default encoding to UTF-8
import sys
reload(sys)
sys.setdefaultencoding('UTF8')

def create_index(es,index_name,mapping):
    print('creating index {}...'.format(index_name))
    mapping_dict = {'mapping': mapping}
    mapping_str = str(mapping_dict)
    print json.dumps(mapping_dict)
    mapping_dict = "{\"mappings\":{\"logs_june\":{\"_timestamp\": {\"enabled\": \"true\"},\"properties\":{\"logdate\":{\"type\":\"date\",\"format\":\"dd/MM/yyy HH:mm:ss\"}}}}}"
#     es.indices.create(index_name, body = json.dumps(mapping_dict))
    es.indices.create(index_name, body = {'mappings': mapping})
    print {'mapping': mapping}
    
bucket = 'store-twitter-stream'
# key = 'twitter/2015/10/16/14/twitter-stream-1-2015-10-16-14-21-36-7e019a27-7b3d-47d5-8805-344832c67be4'
# key = 'twitter/2015/10/20/20/twitter-stream-1-2015-10-20-20-23-33-8f39af04-ee9f-45d6-a2da-06dc068f0c15'
# key = 'twitter/raw-data/2017/07/28/15/twitter-delivery-stream-1-2017-07-28-15-46-45-c7deaace-4db4-4711-b07c-08bbbf3fe451'
# key = 'twitter/raw-data/2017/08/01/15/twitter-delivery-stream-1-2017-08-01-15-00-56-f458fe4e-c192-458b-a42f-1512f8a18b95'
# key = 'twitter/raw-data/2017/08/01/15/twitter-delivery-stream-1-2017-08-01-15-05-56-89a3c060-7119-4332-a034-5f1089a86335'
key = 'twitter/raw-data/2017/08/01/15/twitter-delivery-stream-1-2017-08-01-15-31-01-274bbadb-54c9-4f1d-b5aa-c0b7d675622e'
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
