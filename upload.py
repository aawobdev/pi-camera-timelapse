import json
import boto3
import sys
import os

def upload_to_s3(file):

    with open("crds.json") as f:
        setup = json.load(f)
        f.close()
        AWS_ACCESS_KEY_ID = setup["AWS_ACCESS_KEY_ID"]
        AWS_SECRET_ACCESS_KEY = setup["AWS_SECRET_ACCESS_KEY"]

    session = boto3.Session(
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )

    # Let's use Amazon S3
    s3 = session.resource('s3')
    bucket_name='pi-camera-images'
    data = open(file,'rb')
    s3.Bucket(bucket_name).put_object(Key=os.path.basename(file), Body=data)


# [START]
def main():
    upload_to_s3(sys.argv[1])

if __name__ == '__main__':
    main()
