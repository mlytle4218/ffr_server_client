
import socket
import ffr_config
import json
import time
import m3u8
import requests
from multiprocessing import Process, Value
import uuid
import recording
import datetime
from server_logger import logger

def start_recording(url, file_details, start_time=None, end_time=None):
    try:
        s_time = start_time if start_time else time.time()
        logger.info("tttuuuppplllleeee")
        logger.info(s_time)
        logger.info(type(s_time))

        id = uuid.uuid4()
        a=Value('b',True)
        file_handle = open(file_details, 'wb')

        if url.endswith(".m3u") or url.endswith(".m3u8"):
            p = Process(
                target=concatenate_m3u8_segments,
                args=(url,file_handle,a,start_time, end_time)
                )
        else:
            p = Process(
                target=record_stream_data, 
                args=(url,file_handle,a,start_time, end_time)
                )
        p.start()
        rec = recording.Recording(
                id,
                process=p,
                file_handler=file_handle, 
                flag=a, 
                file_details=file_details,
                start_time=s_time,
                end_time=end_time
                )

        recordings.append(rec)
    except Exception:
        logger.exception("start_recording Error")
        return -1

def record_stream_data(url,fhandler, a, start_time, end_time):
    if end_time != None and time.time() > end_time:
        return None
    if start_time != None and end_time != None:
        while True:
            if start_time < time.time() < end_time:
                break 
    try:
        chunk_size = 1024

        with requests.Session() as session:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
            }
            response = session.get(url, headers=headers, stream=True)
            logger.info(response)
            for chunk in response.iter_content(chunk_size=chunk_size):
                if end_time:
                    if a.value and time.time() < end_time:
                        if chunk:
                            fhandler.write(chunk)
                    else:
                        break
                else:
                    if a.value:
                        if chunk:
                            fhandler.write(chunk)
                    else:
                        break
    except Exception:
        logger.exception("record_stream_data")

def concatenate_m3u8_segments(url, fhandler, a, start_time, end_time):
    if time.time() > end_time:
        return None
    while True:
        if start_time < time.time() < end_time:
            break 
    try:
        stop_flag  = a.value
        path_parts = url.split('/')

        path_parts.pop()
        chunk_size = 1024
        segments_found = []
        if end_time:
            while stop_flag and time.time() < end_time:
                # print("Running in the background...{}".format(a.value))
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
            else:
                while stop_flag:
                    # print("Running in the background...{}".format(a.value))
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

    except Exception:
        logger.exception("concatenate_m3u8_segments")

def stop_recording(id):
    rec = list(filter(lambda recording: str(recording.id) == id, recordings))[0]
    get_rid_of = -1
    for i,recording in enumerate(recordings):
        if recording == rec:
            get_rid_of = i
    
    if get_rid_of >= 0:
        recordings.pop(get_rid_of)

    rec.flag.acquire()
    rec.flag.value = False
    rec.flag.release()
    RUNTIME = 1
    rec.process.join(RUNTIME)
    rec.file_handler.close()

def get_recordings():
    temp = []
    for rec in recordings:
        temp.append({
            "id":str(rec.id),
            "file_details":rec.file_details,
            "start_time": rec.get_start_time(),
            "end_time": rec.end_time
            })
    return json.dumps(temp)

def print_something(bob="default"):
    print("something:{}".format(bob))

def get_date(desc):
    n = datetime.datetime.now()

    print(n.year)

def main():
    while True:
        try:
            data, addr = SOCK.recvfrom(1024)
            data = json.loads(data.decode())
            logger.info(data.get("action"))

            if data.get('action') == "start_recording":
                logger.info(data)
                url = data.get("url")
                file_details = data.get("file_details")

                s_time = data.get("start_time")
                if not data.get("start_time"):
                    s_time = time.time()

                e_time = data.get("end_time")
                if not data.get("end_time"):
                    e_time = None
                
                logger.info("starting recording for {}".format(
                    file_details.split('/')[-1])
                    )

                rec_uuid = start_recording(
                    url=url,
                    file_details=file_details,
                    start_time=s_time,
                    end_time=e_time
                    )
                r_data = json.dumps({"id":str(rec_uuid)})
                SOCK.sendto(r_data.encode(), addr)

            elif data.get('action') == 'stop_recording':
                stop_recording(data.get("id"))
            elif data.get('action') == 'get_recordings':
                SOCK.sendto(get_recordings().encode(), addr)
        except KeyboardInterrupt:
            logger.exception("control c")
            exit()
        except Exception as e:
            logger.exception(e)
            exit()


if __name__ == '__main__':
    SOCK = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    SOCK.bind((ffr_config.IP, ffr_config.PORT))

    recordings = []

    logger.info("starting server")
    main()