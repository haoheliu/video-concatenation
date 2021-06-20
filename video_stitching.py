"""

Concatenate videos

Things to keep in mind:
1. This tool only support .avi format, other format can use ffmpeg to convert to .avi
2. The *.avi files in argument --input_videos_path will be sorted by name, which determines the order.
3. The width of output (argument --width) is an integer, while argument --height is a list, corresponding to the heigth of each row
4. You can determine the number of video in each row by setting argument --number_for_each_row
5. To control the black ragions (margins), you can adjust arguments: --margin and --padding
6. The duration of output file is determined by the shortest duration of files in --input_videos_path

"""


from progressbar import *
import cv2
from os import listdir, path, mkdir
import numpy as np
from argparse import ArgumentParser
from math import ceil

def second_arg(*args):
    return args[0][1]

def pad_row_frames(row_frames, height, width):
    # return row_frames
    h, w = row_frames.shape[0],row_frames.shape[1]
    if(w == width and h == height): return row_frames
    else:
        # print(row_frames.shape,(0,height-h), (0,width-w), (0,0))
        row_frames = np.pad(row_frames,(
            (int(height-h) // 2, int(height-h)-int(height-h) // 2),
            (int(width-w)//2, int(width-w)-int(width-w)//2),
            (0,0)))
    return row_frames

if __name__ == "__main__":
    parser = ArgumentParser()

    parser.add_argument("-i", "--input_videos_path", default="./data/videos", help="The direction containing all avi files")
    parser.add_argument("-o", "--output_video_path", default="merge.avi", help="output file path")
    parser.add_argument("-w", "--width", default=1024, help="output width")
    parser.add_argument("--height", nargs="+", default=[400,300,300], help="heigth for each row")
    parser.add_argument("--number_for_each_row", nargs="+", default=[1,2,2], help="how many video in each row")
    parser.add_argument("--padding", nargs="+", default=[100,10,10], help="left and right padding for each row")
    parser.add_argument("--margin", default=25, help="margin between each frames (in a row)")
    parser.add_argument("--fps", default=30, help="frame per second")

    args = parser.parse_args()

    row_number = len(args.height)
    input_videos_path, output_video_path = args.input_videos_path, args.output_video_path
    width, height, margin, padding = args.width, args.height, args.margin, args.padding
    number_for_each_row = args.number_for_each_row
    fps = args.fps

    file = sorted([path.join(input_videos_path,x) for x in listdir(input_videos_path)])

    assert len(number_for_each_row)==len(height)==len(padding), "These three variable should have the same length, which is row number"
    assert sum(number_for_each_row) == len(file), "The total number of files should be consistant with argument number_for_each_row"

    readers = []
    for f in file:
        if(path.basename(f).split(".")[-1] != "avi"): raise ValueError("Error: Only avi file is supported")
        readers.append(cv2.VideoCapture(f))
        if (not readers[-1].isOpened()): raise ValueError("Error: Fail to open video file", f)
    total_frames = min(reader.get(cv2.CAP_PROP_FRAME_COUNT) for reader in readers)
    print("duration:", total_frames // fps)
    writer = cv2.VideoWriter(output_video_path, cv2.VideoWriter_fourcc('I', '4', '2', '0'), fps,(width, sum(height)))

    have_more_frame = True
    c = 0
    pbar = ProgressBar().start()
    while have_more_frame:
        try:
            frames = [second_arg(reader.read()) for reader in readers]
            row,start = [],0
            for r in range(row_number):
                row_frames = []
                for i, frame in enumerate(frames[start:start+number_for_each_row[r]]):
                    fr = cv2.resize(frame, ((width-padding[r]*2) // number_for_each_row[r] - margin*2, height[r] - margin * 2))
                    fr = np.pad(fr,((margin,margin),(margin,margin),(0,0)))
                    row_frames.append(fr)
                row.append(pad_row_frames(np.concatenate((row_frames),axis=1), height=height[r], width=width))
                start = start+number_for_each_row[r]

            img = np.concatenate(row,axis=0)
            cv2.waitKey(1)
            writer.write(img)
            c += 1
            pbar.update(int((c / (total_frames - 1)) * 100))
        except Exception as e:
            break
    pbar.finish()

    writer.release()
    for reader in readers: reader.release()
    cv2.destroyAllWindows()