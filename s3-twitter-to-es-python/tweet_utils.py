#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on Oct 20, 2015

@author: mentzera

modifications for Social Media Macroscope
07/12/2017	JMT	remove call to Sentiments function
07/12/2017	JMT	add additional fields
07/12/2017	JMT	remove sentiments from tweet_mapping
07/15/2017  JMT	fixed typo statuses not statses
07/17/2017	JMT	Fixed assignment of user_mentions
'''
import re
from textblob import TextBlob

class Sentiments:
    POSITIVE = 'Positive'
    NEGATIVE = 'Negative'
    NEUTRAL = 'Neutral'
    CONFUSED = 'Confused'
    
id_field = 'id_str'
emoticons = {Sentiments.POSITIVE:'😀|😁|😂|😃|😄|😅|😆|😇|😈|😉|😊|😋|😌|😍|😎|😏|😗|😘|😙|😚|😛|😜|😝|😸|😹|😺|😻|😼|😽',
             Sentiments.NEGATIVE : '😒|😓|😔|😖|😞|😟|😠|😡|😢|😣|😤|😥|😦|😧|😨|😩|😪|😫|😬|😭|😾|😿|😰|😱|🙀',
             Sentiments.NEUTRAL : '😐|😑|😳|😮|😯|😶|😴|😵|😲',
             Sentiments.CONFUSED: '😕'
             }

tweet_mapping = {'properties': 
                    {'timestamp_ms': {
                                  'type': 'date'
                                  },
                     'text': {
                                  'type': 'string'
                              },
                     'coordinates': {
                          'properties': {
                             'coordinates': {
                                'type': 'geo_point'
                             },
                             'type': {
                                'type': 'string',
                                'index' : 'not_analyzed'
                            }
                          }
                     },
                     'user': {
                          'properties': {
                             'id': {
                                'type': 'long'
                             },
                             'name': {
                                'type': 'string'
                            }
                          }
                     }
                    }
                 }

def _sentiment_analysis(tweet):
    tweet['emoticons'] = []
    tweet['sentiments'] = []
    _sentiment_analysis_by_emoticons(tweet)
    if len(tweet['sentiments']) == 0:
        _sentiment_analysis_by_text(tweet)


def _sentiment_analysis_by_emoticons(tweet):
    for sentiment, emoticons_icons in emoticons.iteritems():
        matched_emoticons = re.findall(emoticons_icons, tweet['text'].encode('utf-8'))
        if len(matched_emoticons) > 0:
            tweet['emoticons'].extend(matched_emoticons)
            tweet['sentiments'].append(sentiment)
    
    if Sentiments.POSITIVE in tweet['sentiments'] and Sentiments.NEGATIVE in tweet['sentiments']:
        tweet['sentiments'] = Sentiments.CONFUSED
    elif Sentiments.POSITIVE in tweet['sentiments']:
        tweet['sentiments'] = Sentiments.POSITIVE
    elif Sentiments.NEGATIVE in tweet['sentiments']:
        tweet['sentiments'] = Sentiments.NEGATIVE

def _sentiment_analysis_by_text(tweet):
    blob = TextBlob(tweet['text'].decode('ascii', errors="replace"))
    sentiment_polarity = blob.sentiment.polarity
    if sentiment_polarity < 0:
        sentiment = Sentiments.NEGATIVE
    elif sentiment_polarity <= 0.2:
                sentiment = Sentiments.NEUTRAL
    else:
        sentiment = Sentiments.POSITIVE
    tweet['sentiments'] = sentiment
    
def get_tweet(doc):
    tweet = {}
    tweet[id_field] = doc[id_field]
    tweet['hashtags'] = map(lambda x: x['text'],doc['entities']['hashtags'])
    tweet['coordinates'] = doc['coordinates']
    tweet['timestamp_ms'] = doc['timestamp_ms'] 
    tweet['text'] = doc['text']
    tweet['user'] = {'id': doc['user']['id'], 'name': doc['user']['name']}
    tweet['mentions'] = re.findall(r'@\w*', doc['text'])
    # *--------------- additional fields added ----------------* #
    tweet['id'] = doc['id']
    tweet['source'] = doc['source']
    tweet['truncated'] = doc['truncated']
    tweet['id_str'] = doc['id_str']
    tweet['created_at'] = doc['created_at']
    tweet['retweet_count'] = doc['retweet_count']
    tweet['in_reply_to_user_id_str'] = doc['in_reply_to_user_id_str']
    tweet['in_reply_to_status_id_str'] = doc['in_reply_to_status_id_str']
    tweet['in_reply_to_screen_name'] = doc['in_reply_to_screen_name']
    tweet['is_quote_status'] = doc['is_quote_status']
    tweet['favorite_count'] = doc['favorite_count']
    tweet['favorited'] = doc['favorited']
    tweet['retweeted'] = doc['retweeted']
    if ('possibly_sensitive' in doc): tweet['possibly_sensitive'] = doc['possibly_sensitive']
    tweet['filter_level'] = doc['filter_level']
    tweet['lang'] = doc['lang']
    # *--------------- additional fields added to tweet user  --* #
    tweet['user']['id_str'] = doc['user']['id_str']
    tweet['user']['screen_name'] = doc['user']['screen_name']
    tweet['user']['description'] = doc['user']['description']
    tweet['user']['protected'] = doc['user']['protected']
    tweet['user']['verified'] = doc['user']['verified']
    tweet['user']['created_at'] = doc['user']['created_at']
    tweet['user']['profile_image_url'] = doc['user']['profile_image_url']
    tweet['user']['url'] = doc['user']['url']
    tweet['user']['location'] = doc['user']['location']
    tweet['user']['followers_count'] = doc['user']['followers_count']
    tweet['user']['friends_count'] = doc['user']['friends_count']
    tweet['user']['listed_count'] = doc['user']['listed_count']
    tweet['user']['favourites_count'] = doc['user']['favourites_count']
    tweet['user']['statuses_count'] = doc['user']['statuses_count']
    tweet['user']['time_zone'] = doc['user']['time_zone']
    tweet['user']['geo_enabled'] = doc['user']['geo_enabled']
    tweet['user']['lang'] = doc['user']['lang']
    tweet['user']['contributors_enabled'] = doc['user']['contributors_enabled']
    tweet['user']['is_translator'] = doc['user']['is_translator']
    tweet['user']['profile_image_url'] = doc['user']['profile_image_url']
    if ('profile_banner_url' in doc['user']): tweet['user']['profile_banner_url'] = doc['user']['profile_banner_url']
    tweet['user']['following'] = doc['user']['following']
    tweet['user']['follow_request_sent'] = doc['user']['follow_request_sent']
    tweet['user']['notifications'] = doc['user']['notifications']
    # *--------------- additional fields added to tweet place  --* #
    tweet['place'] = doc['place']
    #tweet['place']['id'] = doc['place']['id']
    #tweet['place']['url'] = doc['place']['url']
    #tweet['place']['place_type'] = doc['place']['place_type']
    #tweet['place']['name'] = doc['place']['name']
    #tweet['place']['full_name'] = doc['place']['full_name']
    #tweet['place']['country_code'] = doc['place']['country_code']
    #tweet['place']['country'] = doc['place']['country']
    # *--------- for bounding_box and attributes in place we capture the entire hierarchy in one test  --* #
    #tweet['place']['bounding_box'] = doc['place']['bounding_box']
    #tweet['place']['attributes'] = doc['place']['attributes']
    # *-------------- additional entities fields --* #
    tweet['urls'] = map(lambda x: x['url'],doc['entities']['urls'])
    
    # tweet['user_mentions'] = doc['entities']['user_mentions']
    # Note originally created user_mentions as an array of values but Kinbana issued
    # a warning message indicating "Objects in arrays are not well supported"
    # Also, I was not able to search on them either.  To solve this problem we will
    # create 4 tweet['user_mentions'] lists id, id_str, name and screen_name
    tweet['user_mentions'] = {}
    tweet['user_mentions'] ['id'] = map(lambda x: x['id'],doc['entities']['user_mentions'])
    tweet['user_mentions'] ['id_str'] = map(lambda x: x['id_str'],doc['entities']['user_mentions'])
    tweet['user_mentions'] ['name'] = map(lambda x: x['name'],doc['entities']['user_mentions'])
    tweet['user_mentions'] ['screen_name'] = map(lambda x: x['screen_name'],doc['entities']['user_mentions'])

    # _sentiment_analysis(tweet) # commented out call to sentiments
    return tweet