# import asyncio
import time
import m3u8
import requests
from multiprocessing import Process, Value




def concate_m3u8_segments(url, fhandler, a):
    stop_flag  = a.value
    path_parts = url.split('/')

    path_parts.pop()
    chunk_size = 1024
    segments_found = []
    while stop_flag:
        print("Running in the background...{}".format(a.value))
        time.sleep(1)
        playlist = m3u8.load(url)
        for seg in playlist.segments:
            flag = False

            for val in segments_found:
                if val == seg.uri:
                    flag = True
                    break

            if flag:
                pass
            else:
                segments_found.append(seg.uri)
                pp = path_parts.copy()
                pp.append(seg.uri)
                new_path = '/'.join(pp)
                data = requests.get(new_path)
                for chunk in data.iter_content(chunk_size=chunk_size):
                    fhandler.write(chunk)
        stop_flag = a.value


def record_stream_data(url,fhandler, a):
    chunk_size = 1024

    with requests.Session() as session:
        response = session.get(url, stream=True)
        for chunk in response.iter_content(chunk_size=chunk_size):
            if a.value:
                if chunk:
                    fhandler.write(chunk)
            else:
                break


def start_recording_other(url, file_details):
    a=Value('b',True)
    file_handle = open(file_details, 'wb')
    p = Process(target=record_stream_data, args=(url,file_handle,a,))
    p.start()
    return p,file_handle,a


def start_recording_m3u8(url, file_details):
    a=Value('b', True)
    file_handle = open(file_details, 'wb')
    p = Process(target=concate_m3u8_segments, args=(url,file_handle,a,))
    p.start()
    return p,file_handle,a

def stop_recording(p, fhandler, a):
    a.acquire()
    a.value = False
    a.release()
    RUNTIME = 1
    p.join(RUNTIME)
    fhandler.close()



def main():
    url = "https://cbcradiolive.akamaized.net/hls/live/2041036-b/ES_R1ETR/adaptive_192/chunklist_ao.m3u8"
    url = "http://www.godsdjsradio.com:8080/stream"
    # url = "https://live-hls-audio-web-aje.getaj.net/VOICE-AJE/01.m3u8"

    if url.endswith(".m3u") or url.endswith(".m3u8"):
        p,fhandler,a = start_recording_m3u8(url=url,file_details="/home/marc/ffr/test-trt.mp4")
        time.sleep(20)
        stop_recording(p, fhandler, a)
    else:
        p,fhandler,a = start_recording_other(url=url,file_details="/home/marc/ffr/test-trt.mp4")
        time.sleep(20)
        stop_recording(p, fhandler, a)

if __name__ == "__main__":
    main()