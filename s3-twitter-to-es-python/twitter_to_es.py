'''
Created on Oct 8, 2015

@author: mentzera

08/01/2017	JMT	added create_awsauth functions and modifiedy es object creatation to use http authorization.
'''
from elasticsearch import Elasticsearch, RequestsHttpConnection
from elasticsearch.helpers import bulk
import config
from elasticsearch.exceptions import ElasticsearchException
from tweet_utils import get_tweet, id_field, tweet_mapping
from requests_aws4auth import AWS4Auth
import os

index_name = 'twitter'
doc_type = 'tweet'
mapping = {doc_type: tweet_mapping
           }
bulk_chunk_size = config.es_bulk_chunk_size


def create_index(es,index_name,mapping):
    print('creating index {}...'.format(index_name))
    es.indices.create(index_name, body = {'mappings': mapping})

def create_awsauth():
    AWS_ACCESS_KEY_ES = os.environ["AWS_ACCESS_KEY_ES"]
    AWS_SECRET_KEY_ES = os.environ["AWS_SECRET_KEY_ES"]
    AWS_REGION_ES =     os.environ["AWS_REGION_ES"]
    return AWS4Auth(AWS_ACCESS_KEY_ES, AWS_SECRET_KEY_ES, AWS_REGION_ES, 'es')


def load(tweets):    
    # es = Elasticsearch(host = config.es_host, port = config.es_port)
    awsauth=create_awsauth()
    es = Elasticsearch(hosts=[{'host': config.es_host, 'port': config.es_port}],http_auth=awsauth,use_ssl=True,verify_certs=True,connection_class=RequestsHttpConnection)

    if es.indices.exists(index_name):
        print ('index {} already exists'.format(index_name))
        try:
            es.indices.put_mapping(doc_type, tweet_mapping, index_name)
        except ElasticsearchException as e:
            print('error putting mapping:\n'+str(e))
            print('deleting index {}...'.format(index_name))
            es.indices.delete(index_name)
            create_index(es, index_name, mapping)
    else:
        print('index {} does not exist'.format(index_name))
        create_index(es, index_name, mapping)
    
    counter = 0
    bulk_data = []
    list_size = len(tweets)
    for doc in tweets:
        tweet = get_tweet(doc)
        bulk_doc = {
            "_index": index_name,
            "_type": doc_type,
            "_id": tweet[id_field],
            "_source": tweet
            }
        bulk_data.append(bulk_doc)
        counter+=1
        
        if counter % bulk_chunk_size == 0 or counter == list_size:
            print "ElasticSearch bulk index (index: {INDEX}, type: {TYPE})...".format(INDEX=index_name, TYPE=doc_type)
            success, _ = bulk(es, bulk_data)
            print 'ElasticSearch indexed %d documents' % success
            bulk_data = []
  
