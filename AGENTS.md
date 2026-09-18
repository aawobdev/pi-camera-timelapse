# AGENTS.md

## Purpose

Small Python scripts for capturing a timelapse with a Raspberry Pi camera: take photos at an interval,
overlay a timestamp on each, stitch them into an MP4 with ffmpeg, and upload the video to S3.
Inspired by Armin Hinterwirth's timestamp-overlay timelapse (see `README.md`).

## Structure

- `timelapse.py` - main script (argparse CLI, picamera capture, then timestamps, stitch, S3 upload, cleanup)
- `timestamper.py` - draws date/time from EXIF onto each image (`write_timestamps`), writes `imgXXXXXX-resized.jpg`
- `video_stitcher.py` - shells out to `ffmpeg` to build the video (`stitch_video`)
- `upload.py` - standalone S3 upload of a single file (`python3 upload.py <file>`)
- `requirements.txt` - pinned Python dependencies (Dependabot bumps these)

## Running

Runs on a Raspberry Pi (needs `picamera`, Pillow, `ffmpeg`, and the DejaVu font at
`/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf`). `timelapse.py` flags: `-l/-length` seconds,
`-i/-interval` seconds, `-r/-rotation` (0/90/180/270), `-o/-output` directory (default `/home/pi/Camera`),
`-n/-night` or `-d/-day`:

```
python3 timelapse.py -l 3600 -i 60 -o /home/pi/Camera
```

`README.md` documents a positional-argument form (`python3 timelapse.py 3600 60 /home/pi/Camera`) and a cron
example; `timelapse.py` itself parses the flag form, so the README's usage examples may be out of date.
No tests or CI are present in the repo.

## Conventions and cautions

- Output goes under `<output>/output`; final videos land in `<output>/output/video/timelapse_YYYY-MM-DD_HHmmSS.mp4`, and the working directory is deleted after upload.
- S3 credentials are read from a local `crds.json` (gitignored) and the bucket name is hard-coded in `timelapse.py` and `upload.py`. Never commit `crds.json` or print its contents.
- Scripts are plain modules with no packaging; `timelapse.py` imports `video_stitcher` and `timestamper` from the same directory.
