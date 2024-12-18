import csv
import ffr_config
from base_logger import logger
import subprocess

def get_list_data():
    try:
        with open(ffr_config.LINK_LIST, 'rt') as csvfile:
            return sorted(list(csv.reader(csvfile)))
    except Exception:
        logger.exception("utility:get_list_data")
        return None
    
def youtube_dl_check(stream):
    youtube_dl_cmd = ['youtube-dl','-g',stream]
    p = subprocess.Popen(youtube_dl_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output,err = p.communicate()
    print("checking with youtube-dl")
    print(output)
    if b"ERROR" in output:
        print("giving up on youtube-dl approach")
    else:
        print("not giving up")
        for line in output.splitlines():
            if b"m3u" in line:
                stream = line
    print(stream)
    return stream

def get_stream_type(stream):
    print("Checking URL")
    command = ['ffprobe', '-show_format', '-pretty', '-loglevel', 'quiet', '-protocol_whitelist', 'file,http,https,tcp,tls', stream]
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err =  p.communicate()
    for line in out.splitlines():
        if b"mp3" in line:
            return "mp3"
        elif b"hls" in line:
            return "mp4"
        elif b"aac"  in line:
            return "mp4"
        elif b"mpegts" in line:
            return "mp4"
        else:
            logger.info(line)

def add_data(stream_data):
    with open(ffr_config.LINK_LIST, 'a') as f:
        writer = csv.writer(f)
        writer.writerow(stream_data)