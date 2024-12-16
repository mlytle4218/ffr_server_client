
import socket
import ffr_config
import json
import time
import m3u8
import requests
from multiprocessing import Process, Value
import uuid
import recording
import logging
import sched
import datetime

def start_recording(url, file_details, start_time=None, end_time=None):
    try:
        id = uuid.uuid4()
        a=Value('b',True)
        file_handle = open(file_details, 'wb')
        if url.endswith(".m3u") or url.endswith(".m3u8"):
            p = Process(target=record_stream_data, args=(url,file_handle,a,))
        else:
            p = Process(
                target=concatenate_m3u8_segments, 
                args=(url,file_handle,a,)
                )
        p.start()
        rec = recording.Recording(
                id,
                process=p,
                file_handler=file_handle, 
                flag=a, 
                file_details=file_details,
                start_time=time.time())
        recordings.append(rec)
    except Exception:
        logging.exception("start_recording Error")
        return -1

# def start_recording_other(url, file_details):
#     try:

#         id = uuid.uuid4()
#         a=Value('b',True)
#         file_handle = open(file_details, 'wb')
#         p = Process(target=record_stream_data, args=(url,file_handle,a,))
#         p.start()
#         rec = recording.Recording(
#                 id,
#                 process=p,
#                 file_handler=file_handle, 
#                 flag=a, 
#                 file_details=file_details,
#                 start_time=time.time())
#         recordings.append(rec)
#         return id
#     except Exception:
#         logging.exception("start_recording_other Error")
#         return -1

def record_stream_data(url,fhandler, a):
    try:
        chunk_size = 1024

        with requests.Session() as session:
            response = session.get(url, stream=True)
            for chunk in response.iter_content(chunk_size=chunk_size):
                if a.value:
                    if chunk:
                        fhandler.write(chunk)
                else:
                    break
    except Exception:
        logging.exception("record_stream_data")

# def start_recording_m3u8(url, file_details):
#     try:
#         id = uuid.uuid4
#         a=Value('b', True)
#         file_handle = open(file_details, 'wb')
#         p = Process(target=concatenate_m3u8_segments, args=(url,file_handle,a,))
#         p.start()
#         recordings.append(
#             recording.Recording(
#                 id,
#                 file_handler=file_handle, 
#                 flag=a, 
#                 file_details=file_details,
#                 start_time=time.time())
#             )
#         return id
#     except Exception:
#         return False

def concatenate_m3u8_segments(url, fhandler, a):
    try:
        stop_flag  = a.value
        path_parts = url.split('/')

        path_parts.pop()
        chunk_size = 1024
        segments_found = []
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
        logging.exception("concatenate_m3u8_segments")

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
        temp.append({"id":str(rec.id),"file_details":rec.file_details})
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
            logging.info(data.get("action"))

            if data.get('action') == "start_recording":
                url = data.get("url")
                file_details = data.get("file_details")
                logging.info("starting recording for {}".format(file_details.split('/')[-1]))

                rec_uuid = start_recording(url=url,file_details=file_details)
                r_data = json.dumps({"id":str(rec_uuid)})
                SOCK.sendto(r_data.encode(), addr)

            elif data.get('action') == 'stop_recording':
                stop_recording(data.get("id"))
            elif data.get('action') == 'get_recordings':
                SOCK.sendto(get_recordings().encode(), addr)
        except KeyboardInterrupt:
            logging.exception("control c")
            exit()


if __name__ == '__main__':
    SOCK = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    SOCK.bind((ffr_config.IP, ffr_config.PORT))

    scheduler = sched.scheduler(time.time, time.sleep)

    specific_time = time.mktime(time.strptime("2024-12-15 19:16:10", "%Y-%m-%d %H:%M:%S")) 
    specific_time2 = time.mktime(time.strptime("2024-12-15 19:16:15", "%Y-%m-%d %H:%M:%S")) 
    new_time = datetime.datetime(year=2024,month=12,day=13,hour=14,minute=34)
    scheduler.enterabs(specific_time, 1, print_something)
    scheduler.enterabs(specific_time2, 1, print_something)
    scheduler.run()

    print((specific_time))
    print((new_time))
    # print(time.strftime(new_time.timestamp(), "%Y-%m-%d %H:%M:%S"))


    # print((specific_time).strftime('%Y-%m-%d %H:%M:%S'))
    # print((new_time).strftime('%Y-%m-%d %H:%M:%S'))

    # get_date()

    recordings = []
    logging.basicConfig(
        filename=ffr_config.SERVER_LOG_LOC,
        encoding="utf-8",
        filemode="a",
        format="{asctime} - {levelname} - {message}",
        style="{",
        datefmt="%Y-%m-%d %H:%M",
        level=logging.DEBUG
    )
    logging.info("starting server")
    main()