# video-concatenation

Make several video into one video, display at the same time. 

## Usage
- Use default parameters: 

```shell
python3 video_stitching.py
```

- More customizations: 

```shell
python3 video_stitching.py \ 
-i data/videos \
-o merged.avi 
-w 1024 \
--height 400 300 300 \
--number_for_each_row 1 2 2 \
--padding 100 10 10 \
--margin 25 \
--fps 30
```

## Things to keep in mind

1. This tool only support .avi format, other format can use ffmpeg to convert to .avi.

2. The *.avi files in argument --input_videos_path will be sorted by name, which determines the order later used in concatenation.

3. The width of output (argument --width) is an integer, while argument --height is a list, corresponding to the height of each row.

4. You can determine the number of video in each row by setting argument --number_for_each_row.

5. To control the black region (margins), you can adjust arguments: --margin and --padding.

6. The duration of output file is determined by the shortest duration of files in --input_videos_path.
