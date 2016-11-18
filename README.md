# S3-Restore
You will be able to restore file(s), directories or full bucket

$ ./s3_restore.py -h
usage: s3_restore.py [-h] -b BUCKETNAME [-v VERSION] [--getbucketinfo]

S3 Restore Script

optional arguments:
  -h, --help            show this help message and exit
  -b BUCKETNAME, --bucketname BUCKETNAME
                        Bucket Name ex. s3-io-test-2292
  -v VERSION, --version VERSION
                        Version ID
  --getbucketinfo       Get bucket info

Syntax:
./s3_restore.py -b bucket_name --getbucketinfo


