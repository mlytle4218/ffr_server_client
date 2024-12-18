import socket
import ffr_config
import json
import csv
from base_logger import logger
import os
import tabCompleter
import readline
from date import Date
from subprocess import call
import utility
import menus

class StreamData():
    def __init__(self, description, url, extension):
        self.description = description
        self.url = url
        self.extension = extension
    def __str__(self):
        return self.description


SOCK = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def choose_stream():    
    while True:
        os.system('clear')
        for i,each in enumerate(streams):
            print("number {} {}".format(i+1, each.description))
        print("Letter q Quit")
        choice_made=input("Choice: ")
        
        try:
            int(choice_made)
            if int(choice_made) > 0:
                return streams[int(choice_made)-1]
            else:
                input("invalid choice - Enter to continue")
        except ValueError as e:
            if choice_made == "q":
                return None
            input("invalid choice - Enter to continue")
        except IndexError as e:
            input("invalid choice - Enter to continue")
    
def start_recording(file_details,url,start_time=None,end_time=None):
    if start_time and end_time:
        data = json.dumps(
                {
                    "action":"start_recording",
                    "file_details": file_details, 
                    "url": url,
                    "start_time":start_time,
                    "end_time": end_time
                }
            )
    elif start_time:
        data = json.dumps(
                {
                    "action":"start_recording",
                    "file_details": file_details, 
                    "url": url,
                    "start_time":start_time
                }
            )

    else:
        data = json.dumps(
                {
                    "action":"start_recording",
                    "file_details": file_details, 
                    "url": url,
                }
            )
    SOCK.sendto(
        data.encode(),
        (ffr_config.IP, ffr_config.PORT)
        )
    data, _ = SOCK.recvfrom(1024)
    return data

def stop_recording(id):
    data = json.dumps({"action":"stop_recording","id": id})
    SOCK.sendto(
        data.encode(),
        (ffr_config.IP, ffr_config.PORT)
        )
    # data, _ = SOCK.recvfrom(1024)
    return data

def get_recordings():
    data = json.dumps({"action":"get_recordings"})
    SOCK.sendto(
        data.encode(),
        (ffr_config.IP, ffr_config.PORT)
        )
    data, _ = SOCK.recvfrom(1024)
    return json.loads(data)

def get_file_path(extenstion):
    t = tabCompleter.tabCompleter()
    readline.set_completer_delims('\t')
    readline.parse_and_bind("tab: complete")
    readline.set_completer(t.pathCompleter)
    path = input("Enter file path: ")
    return path + "." + extenstion

def load_saved_stream_data():
    streams = []
    with open(ffr_config.LINK_LIST, 'rt') as stream_list:
        stream_data = sorted(list(csv.reader(stream_list)))
        for stream in stream_data:
            streams.append(
                StreamData(
                    description=stream[0],
                    url=stream[1],
                    extension=stream[2]
                    )
                )
    return streams

def stream_record_start():
    record_menu_options = [
        {"text":"re-cord now","func":stream_record_start_now},
        {"text":"re-cord later","func":stream_record_start_later}
    ]
    menu_choice(record_menu_options)

def stream_record_start_now():
    stm = choose_stream()
    file_path = get_file_path(stm.extension)
    start_recording(file_path, stm.url)
    input("recoding started - Enter to continue")

def stream_record_start_later():
    s_time = Date().enter_datetime("start")
    e_time = Date().enter_datetime("end")
    stm = choose_stream()
    file_path = get_file_path(stm.extension)
    start_recording(file_path, stm.url,start_time=s_time,end_time=e_time)
    input("recoding started - Enter to continue")

def stream_record_stop():
    recordings = get_recordings()
    while True:
        os.system('clear')
        for i,each in enumerate(recordings):
            print("number {} {}".format(i+1, each["file_details"]))
        print("Letter q Quit")
        choice_made=input("Choice: ")
        
        try:
            int(choice_made)
            if int(choice_made) > 0:
                break
            else:
                input("invalid choice - Enter to continue")
        except ValueError as e:
            if choice_made == "q":
                break
            input("invalid choice - Enter to continue")
        except IndexError as e:
            input("invalid choice - Enter to continue")
    # os.system('clear')
    print(recordings[int(choice_made)-1])
    stop_recording(recordings[int(choice_made)-1]["id"])
    input("recording stopped - Enter to continue")
    pass

def stream_play():
    stm = choose_stream()
    # print(stm.url)
    call(["mpv","--really-quiet","--no-video",str(stm.url)])
    input("Enter to continue")

def stream_add():
    os.system('clear')
    data = utility.get_list_data()
    alias=input("Alias for new stream: ")
    while len(list(filter(lambda als: als[0] == alias, data))) > 0:
        alias=input("Alias in use - alias for new stream: ")
    stream = input("URL for stream: ")
    stream = utility.youtube_dl_check(stream=stream)
    extension = utility.get_stream_type(stream=stream)
    if extension==None:
        input("Problem with that url - Enter to continue")
    else:
        new_fields=[alias,stream,extension]
        utility.add_data(new_fields)
        input("New stream added - Enter to continue")

    input("Enter to continue")

def stream_remove():
    os.system('clear')
    print("remove")
    input("Enter to continue")
    pass

def stream_edit():
    os.system('clear')
    print("edit")
    input("Enter to continue")
    pass

def menu_choice(options):
    while True:
        os.system('clear')
        for i,each in enumerate(options):
            print("number {} {}".format(i+1, each["text"]))
        print("Letter q Quit")
        choice_made=input("Choice: ")
        
        try:
            int(choice_made)
            if int(choice_made) > 0:
                options[int(choice_made)-1]["func"]()
            else:
                input("invalid choice - Enter to continue")
        except ValueError as e:
            if choice_made == "q":
                break
            input("invalid choice - Enter to continue")
        except IndexError as e:
            input("invalid choice - Enter to continue")

if __name__ == "__main__":
    logger.info("starting client")

    streams = load_saved_stream_data()





    # main_menu_options = [
    #     {"text":"re-cord existing stream","func":stream_record_start},
    #     {"text":"stop re-cording existing stream","func":stream_record_stop},
    #     {"text":"Listen to existing stream","func":stream_play},
    #     {"text":"Add new stream","func":stream_add},
    #     {"text":"Remove stream","func":stream_remove},
    #     {"text":"Edit existing stream","func":stream_edit}
    # ]
    menu_choice(menus.main_menu_options)



    # specific_time = time.mktime(time.strptime("2024-12-15 21:16:00", "%Y-%m-%d %H:%M:%S")) 
    # specific_time2 = time.mktime(time.strptime("2024-12-15 21:16:55", "%Y-%m-%d %H:%M:%S")) 
    # t = timings.Timings(start_time=specific_time, end_time=specific_time2)

    # start_recording(
    #     "/home/marc/ffr/test1.mp3", 
    #     "http://www.godsdjsradio.com:8080/stream",
    #     specific_time,
    #     specific_time2
    #     )











    # temp = start_recording("/home/marc/ffr/test1.mp3", "http://www.godsdjsradio.com:8080/stream")
    # res = json.loads(temp)
    # time.sleep(10)
    # temp = start_recording("/home/marc/ffr/test2.mp3", "http://www.godsdjsradio.com:8080/stream")
    # time.sleep(10)
    # temp = start_recording("/home/marc/ffr/test3.mp3", "http://www.godsdjsradio.com:8080/stream")


    # print(get_recordings())


    # stop_recording(res["id"])


    # with open(ffr_config.LINK_LIST, 'rt') as csvfile:
    #     result = []
    #     data = sorted(list(csv.reader(csvfile)))
    #     for datum in data:
    #         print("{}:{}".format(len(datum), datum))
