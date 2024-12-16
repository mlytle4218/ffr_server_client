import socket
import ffr_config
import json
import time
import csv
import utility
from base_logger import logger
import os
import sys
import tabCompleter
import readline

class StreamData():
    def __init__(self, description, url, extension):
        self.description = description
        self.url = url
        self.extension = extension
    def __str__(self):
        return self.description


SOCK = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
def start_recording(file_details,url):
    data = json.dumps(
        {"action":"start_recording","file_details": file_details, "url": url}
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
    while True:
        os.system('clear')
        for i,each in enumerate(streams):
            print("number {} {}".format(i+1, each.description))
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

    # print(streams[int(choice_made)-1])
    # input("Enter to continue")
    stm = streams[int(choice_made)-1]
    file_path = get_file_path(stm.extension)
    start_recording(file_path, stm.url)
    input("recoding started - Enter to continue")

def stream_record_start_later():
    os.system('clear')
    print("record_start_later")
    input("Enter to continue")
    pass

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
    os.system('clear')
    print("play")
    input("Enter to continue")
    pass
def stream_add():
    os.system('clear')
    print("add")
    input("Enter to continue")
    pass
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





    main_menu_options = [
        {"text":"re-cord existing stream","func":stream_record_start},
        {"text":"stop re-cording existing stream","func":stream_record_stop},
        {"text":"Listen to existing stream","func":stream_play},
        {"text":"Add new stream","func":stream_add},
        {"text":"Remove stream","func":stream_remove},
        {"text":"Edit existing stream","func":stream_edit}
    ]
    menu_choice(main_menu_options)


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
