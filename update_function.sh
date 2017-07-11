#!/bin/bash

# NOTE: as of 7/7/2016 this script has never been run, but could be used to upload
# a new version of the python code for the lambda function send-twitter-stream-to-es
# Also NOTE: I have used aws cli to update other lambda function, but I HAVE NOT used the PUT command below (which is commented out)

# PUT /2015-03-31/functions/arn:aws:lambda:us-west-2:083781070261:function:send-twitter-stream-to-es/code HTTP/1.1
# Content-type: application/json
# 
# {
#    "DryRun": TRUE,
#    "Publish": FALSE,
# #   "S3Bucket": "string",
# #   "S3Key": "string",
# #   "S3ObjectVersion": "string",
#    "ZipFile": my-s3-twitter-to-es-python.zip
# }


aws lambda update-function-code --function-name send-twitter-stream-to-es --zip-file fileb://my-s3-twitter-to-es-python.zip