import subprocess
import sys
from moviepy.editor import *


def ffmpeg_command(video, audio, output):
    audioclip = AudioFileClip(audio)
    videoclip = VideoFileClip(video)
    vclip2 = videoclip.set_audio(audioclip)
    vclip2.write_videofile(output, verbose=0)
    # command = ['ffmpeg', '-loglevel', 'warning', '-i', video, '-i',
    #            audio,
    #            output]
    # subprocess.run(command)


class StdoutInterceptor:
    def __init__(self, original_stdout):
        self.original_stdout = original_stdout

    def write(self, text):
        # pass
        if "moviepy" not in text and "Moviepy" not in text and "\n" not in text:
            self.original_stdout.write(text.strip())


if __name__ == '__main__':
    video = 'C:\\Users\\14485\\Downloads\\video.m4s'
    audio = 'C:\\Users\\14485\\Downloads\\audio.m4s'
    output = 'C:\\Users\\14485\\Downloads\\output.mp4'
    original_stdout = sys.stdout
    sys.stdout = StdoutInterceptor(sys.stdout)
    ffmpeg_command(video, audio, output)
    sys.stdout = original_stdout
