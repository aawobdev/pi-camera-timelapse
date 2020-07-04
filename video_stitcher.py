#!/usr/bin/env python3

# [START includes]
import os

def stitch_video(filename, loglevel, input_folder,output_folder, image_name):
    if not os.path.exists(input_folder + '/' +output_folder):
        os.makedirs(input_folder + '/' +output_folder)
    os.system('ffmpeg -r 10 -i '+input_folder+'/'+image_name+' -r 10 -vcodec libx264 -vf scale=1280:720 '+input_folder + '/' +output_folder+'/'+filename + ' -loglevel '+loglevel)