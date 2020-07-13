# pi-camera-timelapse

Heavily inspired by:
* Armin Hinterwirth (https://github.com/amphioxus) - https://www.amphioxus.org/content/timelapse-time-stamp-overlay

[![PiCam Timelapse](https://i9.ytimg.com/vi/auIuiP3BAKg/mq3.jpg?sqp=CID0sPgF&rs=AOn4CLDYb8buEuuwAdGCJPEfYO4Z-TcCuQ)](https://youtu.be/auIuiP3BAKg)

## Some helpful Python scripts for achieving a timelapse with your Rapsberry Pi Camera

```timelapse.py``` is the main script

### Dependencies on 
* ```video_stitcher.py``` 
* ```timestamper.py```
### Python lib dependencies are:
* ffmpeg (usually comes with Pi OS)
* Pillow (aka PIL, also should ship with Pi)
### Font dependencies
* /usr/share/fonts/truetype/freefont/FreeMono.ttf

## Steps
* Initial Images will be outputted to ```imgXXXXXX.jpg``` inside the ```output``` folder
* Next, timestamps are drawn onto the images, they're stored as ```imgXXXXXX-resized.jpg```
* Finally the ```imgXXXXXX-resized.jpg``` images are stitched into a video inside ```output/video``` folder as ```timelapse_YYYY-MM-DD_HHmmSS.mp4```
* Modify ```main()``` inside ```timelapse.py``` to use what you need

## Usage examples
```
python3 timelapse.py [length in seconds] [interval in seconds] [directory to output]
```

### Example 1) Run for 1 hour with 1 minute intervals, output to /home/pi/Camera
```
python3 timelapse.py 3600 60 /home/pi/Camera
```

### Example 2) Run for 8 hours with 1 hour intervals, output to /home/pi/Camera
```
python3 timelapse.py 28800 3600 /home/pi/Camera
```

### Example 3) Run for 1 minute with 1 second intervals, output to /home/pi/Camera
```
python3 timelapse.py 60 1 /home/pi/Camera
```

## Run in background

### Example 4) Will do the following:
* Run as cronjob for 1 minute with 1 second intervals
* Output images and video to /home/pi/Camera
* Run at 4AM every morning
* Output the Logs to a file inside my Camera folder

#### Open cron config
```
crontab -e
```
#### Add line to the end of the file
```
0 4 * * * python3 /home/pi/Camera/timelapse.py 60 1 /home/pi/Camera >> /home/pi/Camera/output.log 2>$
```
#### CTRL+X and 'y' to confirm saved changes

## Some helpful links
* https://crontab.guru/
* https://www.raspberrypi.org/documentation/usage/camera/raspicam/
* https://projects.raspberrypi.org/en/projects/getting-started-with-picamera
* https://picamera.readthedocs.io/en/release-1.10/api_camera.html
