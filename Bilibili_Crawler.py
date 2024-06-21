import gzip
import json
import os
import re
import sys
import time
from urllib import request
import requests
from tqdm import tqdm
from m4s_2_mp4 import *


class Bilibili_Crawler:
    def __init__(self, url):
        self.headers = {
            'Cookie': 'i-wanna-go-back=-1; buvid4=61A838A4-763A-F8D3-1698-385310580BCE79863-023031719-EoBTQlFuJp9yv50TgeLTsw%3D%3D; CURRENT_BLACKGAP=0; buvid_fp_plain=undefined; hit-dyn-v2=1; hit-new-style-dyn=1; enable_web_push=DISABLE; DedeUserID=9207938; DedeUserID__ckMd5=20b6c2a2fc38fede; SESSDATA=ed6256b1%2C1724667032%2C7a63f%2A21CjCgWXxCxl4I2XbLVxi1XabkWcJnB_vwZJq30jHV5_WZpGme7UxntT0ZcvqUBipHorISVmU0dFFHdlZVSXVWOUNTUUJFRVhWXzZyaDN4Z01aX0tycEMwTUw4ZER4UWFjX1RnME1vbE9WbzlmYm5qc0toZHlrZ0NRc3pOQk12QVRJaDFtWUstLS1BIIEC; bili_jct=415b175bdf0421ab101a4cf4cb65e230; sid=4jxh0hgx; buvid3=75EB3200-5BDA-372D-77BB-93A22051246268101infoc; b_nut=1710676268; b_ut=5; _uuid=1E108B6CA-713C-6104E-7D13-F13101AAE974F68930infoc; header_theme_version=CLOSE; fingerprint=5a60693869462675f59d89a9fe5554e6; FEED_LIVE_VERSION=V_WATCHLATER_PIP_WINDOW3; CURRENT_FNVAL=4048; buvid_fp=aa7635d5345ba22eefdf02a90be4585d; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MTM4NTU4NzMsImlhdCI6MTcxMzU5NjYxMywicGx0IjotMX0.EK9O3mU57_0Vl24Nsg6F7XNjBOD_l2psDyApTxStJaw; bili_ticket_expires=1713855813; rpdid=|(J~kuRYu|Ym0J\'u~uJYYRJJ); bp_video_offset_9207938=923164655796355089; b_lsid=F4BB6910D_18F08822DB3; bmg_af_switch=1; bmg_src_def_domain=i1.hdslb.com; home_feed_column=5; browser_resolution=1872-958; CURRENT_QUALITY=80; PVID=1',
            'User-Agent':
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                'Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0'}
        self.url = url
        self.headers.update({'Referer': url})
        self.outdir = "./output/"

    def __call__(self, *args, **kwargs):
        req = request.Request(url=self.url, headers=self.headers)
        response = request.urlopen(req)
        context = response.read()
        txt = gzip.decompress(context).decode('utf8')

        match_video = re.search(r'"id":80,"baseUrl":"(.*?)"', txt)
        video_url = '{' + match_video.group(0) + '}'
        video_dic = json.loads(video_url)

        match_audio = re.search(r'"id":30280,"baseUrl":"(.*?)"', txt)
        audio_url = '{' + match_audio.group(0) + '}'
        audio_dic = json.loads(audio_url)
        video_download_path = self.download(video_dic)
        time.sleep(0.1)
        audio_download_path = self.download(audio_dic)

        original_stdout = sys.stdout
        print("\033[32m{txt}\033[0m".format(txt="开始合成MP4文件"))
        try:
            sys.stdout = StdoutInterceptor(sys.stdout)
            ffmpeg_command(video_download_path, audio_download_path, self.outdir + 'output.mp4')
        finally:
            sys.stdout = original_stdout
        print("\033[32m{txt}\033[0m".format(txt="合成MP4文件成功\n"))

    def download(self, dic):
        if dic['id'] in [80, 64, 32, 16]:
            download_type = '视频'
            download_path = './video/video.m4s'
        elif dic['id'] == 30280:
            download_type = '音频'
            download_path = './audio/audio.m4s'
        else:
            raise TypeError("Download Type Error. id should be [80, 64, 32, 16] or 30280")
        baseurl = dic['baseUrl']
        response = requests.get(baseurl, headers=self.headers, stream=True)

        if response.status_code == 200:
            print("\033[32m{txt}{type}\033[0m".format(txt="开始下载", type=download_type))
            time.sleep(0.1)
            total_size = int(response.headers.get('content-length', 0))
            with open(download_path, 'wb') as f:
                download_bar = tqdm(total=100)
                for chunk in response.iter_content(chunk_size=1024):
                    f.write(chunk)
                    download_size = os.path.getsize(download_path)
                    if download_size < total_size:
                        progress_percent = (download_size / total_size) * 100
                        download_bar.update(progress_percent - download_bar.n)
                download_bar.close()
            print("\n\033[32m{type}{txt}\033[0m".format(type=download_type, txt="下载成功"))
        else:
            print("\n\033[31m{type}{txt}{sc}\033[0m".format(type=download_type, txt="文件下载失败，状态码:",
                                                            sc=response.status_code))
        return download_path


if __name__ == '__main__':
    url = "https://www.bilibili.com/video/BV1EH4y1P7Kp/?spm_id_from=333.880.my_history.page.click&vd_source=422f25412dab6c8c12801cfc0eff4655"
    bc = Bilibili_Crawler(url)
    bc()
