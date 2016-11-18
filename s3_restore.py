#!/usr/bin/python2.7
# Ali Ikram
import os, sys, argparse
from s3_functions import s3

parser = argparse.ArgumentParser(description='S3 Restore Script')
parser.add_argument('-b','--bucketname', help='Bucket Name ex. s3-io-test-2292',required=True)
parser.add_argument('-v','--version',help='Version ID', required=False)
parser.add_argument('--getbucketinfo',help='Get bucket info',  action='store_true', required=False)
args = parser.parse_args()

BUCKET_NAME = args.bucketname
VERSION_ID = args.version
GET_INFO = args.getbucketinfo

if args.getbucketinfo:
	data = s3(BUCKET_NAME)	
	data.get_bucket_list()
elif args.bucketname and args.version:
	data = s3(BUCKET_NAME)	
elif args.version and args.getbucketinfo:
	print('You cannot provide version ID with "--getbucketinfo" options')

