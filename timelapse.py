#!/usr/bin/env python3

# [START includes]
from subprocess import check_output
from re import findall
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from video_stitcher import stitch_video
from timestamper import write_timestamps
import argparse
from datetime import datetime
import time
import picamera
import sys
import os
import logging
import boto3
import glob
import json

logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)

__output_folder_name__= sys.argv[3] + '/output'

__default_rotation__ = 0

def clean_directory():
    os.system('rm -R -f '+__output_folder_name__)

def capture_images(length_in_seconds,interval_in_seconds, rotation):
    count = length_in_seconds / interval_in_seconds
    logging.info('Taking {} shots...'.format(count))
    with picamera.PiCamera() as camera:
        camera.start_preview()
        camera.rotation = rotation
        time.sleep(2)
        for filename in camera.capture_continuous(__output_folder_name__+'/img{counter:06d}.jpg'):
            time.sleep(interval_in_seconds) # wait <interval_in_seconds> seconds
            count -= 1
            if count <= 0:
                break

def upload_to_s3(video_folder):

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

    for file in list(glob.glob(video_folder + '/*.mp4')):
        file_ob = open(file,'r')
        file_name=os.path.basename(file_ob.name)
        file_ob.close()
        data = open(file,'rb')
        s3.Bucket(bucket_name).put_object(Key=file_name, Body=data)
# [START]
def main():
    # Start with cleanup
    start_time = time.time()
    if not os.path.exists(__output_folder_name__):
        os.makedirs(__output_folder_name__)
    logging.info('Running clean script...')

    # Check for rotation
    if len(sys.argv) == 5:
        rotation = int(sys.argv[4])
    else:
        rotation = __default_rotation__

    # Take pictures
    logging.info('Opening camera...')
    capture_images(int(sys.argv[1]),int(sys.argv[2]), rotation)
    logging.info('Writing timestamps...')

    # Write timestamps to images
    write_timestamps(72,32,__output_folder_name__)
    logging.info('Captured images {} seconds to run'.format(str(time.time() - start_time)))

    # Create video
    logging.info('Making video...')
    timestamp = str(datetime.now().strftime('%Y-%m-%d_%H%M%S'))
    stitch_video('timelapse_'+timestamp+'.mp4','warning',__output_folder_name__,'video','img%06d-resized.jpg')
    logging.info('Done!')
    logging.info('Creating video {} seconds to run'.format(str(time.time() - start_time)))
    upload_to_s3(__output_folder_name__ + '/video')
    clean_directory()


if __name__ == '__main__':
    main()
