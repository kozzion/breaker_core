import os

from ffmpy import FFmpeg

import cv2
from PIL import Image
from subprocess import Popen, PIPE

class ToolsFfmpeg(object):


    @staticmethod
    def video_extract_frames_jpg(path_file_video:str, path_dir_frame:str):
        ff = FFmpeg(
            inputs={os.path.abspath(path_file_video): None},
            outputs={os.path.abspath(path_dir_frame) + os.sep + 'frame%08d.jpg': []})

        print(ff.cmd)
        ff.run()

    @staticmethod
    def video_merges_frames_jpg(path_file_video:str, path_dir_frame:str):
        ff = FFmpeg(
            inputs={os.path.abspath(path_dir_frame) + os.sep + 'frame%08d.jpg': []},
            outputs={os.path.abspath(path_file_video): None})

        print(ff.cmd)
        ff.run()

    @staticmethod
    def video_merges_frames_jpg2(path_file_video:str, path_dir_frame:str):
        p = Popen(['ffmpeg', '-y', '-f', 'image2pipe', '-vcodec', 'mjpeg', '-r', '24', '-i', '-', '-vcodec', 'h264', '-qscale', '5', '-r', '24', os.path.abspath(path_file_video)], stdin=PIPE)

        video = cv2.VideoCapture('videos.mp4')

        list_name_frame = sorted(os.listdir(path_dir_frame))
        for name_frame in list_name_frame:
            path_file_frame = os.path.join(path_dir_frame, name_frame)

            frame = cv2.cvtColor(cv2.imread(path_file_frame), cv2.COLOR_BGR2RGB)
            im = Image.fromarray(frame)
            im.save(p.stdin, 'JPEG')
   

        p.stdin.close()
        p.wait()
        video.release()
