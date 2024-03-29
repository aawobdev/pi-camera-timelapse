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
import os
import logging
import boto3
import glob
import json
import argparse

parser=argparse.ArgumentParser()
parser.add_argument('-length', '-l', action="store", dest="length", default=60, help='Length in seconds')
parser.add_argument('-interval', '-i', action="store", dest="interval", default=1, help='Interval in seconds')
parser.add_argument('-rotation', '-r', action="store", dest="rotation", default=0, help='Rotation 0, 90, 180, 270')
parser.add_argument('-output', '-o', action="store", dest="output", default="/home/pi/Camera", help='Output full path')
parser.add_argument('-night', '-n', action="store_true", dest="night", help='Night mode')
parser.add_argument('-day', '-d', action="store_false", dest="night", help='Day mode')

args = parser.parse_args()

logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)

__default_rotation__ = 0
__night_mode__ = bool(args.night)
__length__ = int(args.length)
__interval__ = int(args.interval)
__rotation__ = int(args.rotation)
__output__ = str(args.output)

__output_folder_name__= __output__ + '/output'

def clean_directory():
    os.system('rm -R -f '+__output_folder_name__)

def capture_images(length_in_seconds,interval_in_seconds, rotation, n_mode):
    count = length_in_seconds / interval_in_seconds
    logging.info('Taking {} shots...'.format(count))
    print(n_mode)
    with picamera.PiCamera() as camera:
        if(n_mode):
            print("Trying to set exposure to night")
            camera.exposure_mode = 'night'
            camera.iso = 800
        else:
            print("No night mode")
        camera.start_preview()
        print(camera.exposure_mode)
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
    if (__rotation__ != None):
        rotation = __rotation__
    else:
        rotation = __default_rotation__

    # Take pictures
    logging.info('Opening camera...')
    capture_images(__length__,__interval__, rotation,__night_mode__)
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
