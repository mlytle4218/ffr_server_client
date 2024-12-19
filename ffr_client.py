import socket
import ffr_config
import json
from client_logger import logger
import os
from date import Date
from subprocess import call
import utility
import menus


def choose_stream():
    streams = utility.load_saved_stream_data() 
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
                input("1invalid choice - Enter to continue")
        except ValueError as e:
            if choice_made == "q":
                return None
            input("2invalid choice - Enter to continue")
        except IndexError as e:
            input("3invalid choice - Enter to continue")
    
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

def stream_record_start_now():
    stm = choose_stream()
    if stm:
        file_path = utility.get_file_path(stm.extension)
        start_recording(file_path, stm.url)
        input("recoding started - Enter to continue")

def stream_record_start_later():
    s_time = Date().enter_datetime("start")
    e_time = Date().enter_datetime("end")
    stm = choose_stream()
    if stm:
        file_path = utility.get_file_path(stm.extension)
        start_recording(file_path, stm.url,start_time=s_time,end_time=e_time)
        input("recoding started - Enter to continue")

def stream_record_start():
    menu_choice(menus.record_menu_options)

def stream_record_stop():
    recordings = get_recordings()
    # while True:
    #     os.system('clear')
    #     for i,each in enumerate(recordings):
    #         print("number {} {}".format(i+1, each["file_details"]))
    #     print("Letter q Quit")
    #     choice_made=input("Choice: ")
        
    #     try:
    #         int(choice_made)
    #         if int(choice_made) > 0:
    #             break
    #         else:
    #             input("invalid choice - Enter to continue")
    #     except ValueError as e:
    #         if choice_made == "q":
    #             break
    #         input("invalid choice - Enter to continue")
    #     except IndexError as e:
    #         input("invalid choice - Enter to continue")
    # os.system('clear')

    choice_made = menu_choice(recordings)
    print(recordings[int(choice_made)-1])
    stop_recording(recordings[int(choice_made)-1]["id"])
    input("recording stopped - Enter to continue")
    pass

def stream_play():
    stm = choose_stream()
    if stm:
        call(["mpv","--really-quiet","--no-video",str(stm.url)])
        input("Enter to continue")

def stream_add():
    os.system('clear')
    data = utility.get_list_data()
    alias=input("Alias for new stream: ")
    while len(list(filter(lambda als: als[0] == alias, data))) > 0:
        alias=input("Alias in use - alias for new stream: ")
    while True:
        stream = input("URL for stream: ")
        stream = utility.youtube_dl_check(stream=stream)
        extension = utility.get_stream_type(stream=stream)
        if extension==None:
            input("Problem with that url - Enter to continue")
        else:
            new_fields=[alias,stream,extension]
            utility.add_data(new_fields)
            input("New stream added - Enter to continue")
            break

    # input("Enter to continue")

def stream_remove():
    os.system('clear')
    stm = choose_stream()
    # print("remove")
    if stm:
        data = utility.get_list_data()
        result  = list(filter(lambda stream: stream[0] != stm.description, data))
        utility.override_list(result)
        input("Stream removed - Enter to continue")

def stream_edit():
    os.system('clear')
    stm = choose_stream()
    if stm:
        data = utility.get_list_data()
        for i in range(len(data)):
            if data[i][0] == stm.description:
                print("existing alias: " + data[i][0])
                alias=input("Alias for new stream: ") or  data[i][0]
                print("existing URL: " + data[i][1])
                stream = input("URL for stream: ") or data[i][1]
                stream = utility.youtube_dl_check(stream=stream)
                extension = utility.get_stream_type(stream=stream)
                if extension==None:
                    input("Problem with that url - Enter to continue")
                else:

                    data[i][0] = alias
                    data[i][1] = stream
                    data[i][2] = extension
                    utility.override_list(data)
                    input("Stream updated - Enter to continue")

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
    SOCK = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    logger.info("starting client")

    menu_choice(menus.main_menu_options)
