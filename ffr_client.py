import socket
import ffr_config
import json
from client_logger import logger
import os
from date import Date
from subprocess import call
import utility
import menus
import datetime


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
    """
    Support function that is called when a user chooses to start a new 
    recording. 

    Args:
        file_details (str): the path to the file
        url (str): the URL to record
        start_time (Date, optional): when to start recording. Defaults to None.
        end_time (Date, optional): when to stop recording. Defaults to None.

    Returns:
        _type_: _description_
    """
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
    SOCK = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    SOCK.settimeout(ffr_config.TIMEOUT)
    SOCK.sendto(
        data.encode(),
        (ffr_config.IP, ffr_config.PORT)
        )
    data, _ = SOCK.recvfrom(1024)
    return data

def stop_recording(id):
    """
    Support function that is called when a user chooses to stop an existing 
    recording. It will pass the ID generated when the server recieved the 
    recording request, and tell the server to stop that recording.

    Args:
        id (str): UUID of the recording on the ffr server
    """
    data = json.dumps({"action":"stop_recording","id": id})
    SOCK = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    SOCK.settimeout(ffr_config.TIMEOUT)
    SOCK.sendto(
        data.encode(),
        (ffr_config.IP, ffr_config.PORT)
        )
    # data, _ = SOCK.recvfrom(1024)
    # return data

def get_recordings():
    """
    Allows a user to connect to the  ffr server and pull down information about
    recordings

    Returns:
        JSON: list of recordings reporting file path, start time, and scheuled
        end time if applicable.
    """
    try:
        SOCK = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        SOCK.settimeout(ffr_config.TIMEOUT)
        data = json.dumps({"action":"get_recordings"})
        SOCK.sendto(
            data.encode(),
            (ffr_config.IP, ffr_config.PORT)
            )
        data, _ = SOCK.recvfrom(1024)
        return json.loads(data)
    except TimeoutError:
        logger.exception("get recordings")
        input("could not connect to ffr server - Enter to continue")
    except Exception:
        logger.exception("get recordings ")

def stream_record_start_now():
    """
    Allows a user to choose a stream and start recording it.
    """
    stm = choose_stream()
    if stm:
        file_path = utility.get_file_path(stm.extension)
        start_recording(file_path, stm.url)
        input("recoding started - Enter to continue")

def stream_record_start_later():
    """
    Acts as an interactive menu for a user to record an stream at a later date.
    """
    s_time = Date().enter_datetime("start")
    e_time = Date().enter_datetime("end")
    stm = choose_stream()
    if stm:
        file_path = utility.get_file_path(stm.extension)
        start_recording(file_path, stm.url,start_time=s_time,end_time=e_time)
        input("recoding started - Enter to continue")

def stream_record_start():
    """
    Calls a submenu for recording.
    """
    menu_choice(menus.record_menu_options)

def stream_record_stop():
    """
    Lets a user communicate with the server and see recordings currently in 
    progress. The user can stop the recording by passing the id to the
    stop_recodring function or just quit the menu
    """
    recordings = get_recordings()
    if recordings:
        try:
            while True:
                os.system('clear')
                for i,each in enumerate(recordings):
                    e_time = each["end_time"] if each["end_time"] else None

                    print("number {} {} {} {}".format(
                            i+1, 
                            each["file_details"], 
                            datetime.datetime.fromtimestamp(
                                each["start_time"]
                                ).strftime("%Y-%m-%d %H:%M") , 
                            e_time
                            )
                        )
                print("Letter q Quit")
                rec_choice_made=input("Choice: ")
                
                try:
                    int(rec_choice_made)
                    if len(rec_choice_made)+1 > int(rec_choice_made) > 0:
                        stop_recording(recordings[int(rec_choice_made)-1]["id"])
                        break
                    else:
                        input("1invalid choice - Enter to continue")
                except ValueError as e:
                    if rec_choice_made == "q":
                        break
                    input("2invalid choice - Enter to continue")
                except IndexError as e:
                    input("3invalid choice - Enter to continue")
        except KeyboardInterrupt:
            logger.info("control c")
        except TypeError:
            logger.exception("menu_choice")
















        # print(recordings[int(choice_made)-1])
        # stop_recording(recordings[int(choice_made)-1]["id"])
        # input("recording stopped - Enter to continue")
    else:
        input("No recording currently in progress - Enter to continue")

def stream_play():
    """
    Lets a user choose and stream and attempt to listen to it via MPV.
    """
    stm = choose_stream()
    if stm:
        call(["mpv","--really-quiet","--no-video",str(stm.url)])
        input("Enter to continue")

def stream_add():
    """
    Acts as a interactive menu so a user can enter stream information. It will 
    check against known aliases and validity of the stream data.
    """
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
    """
    Lets a user pick a saved stream information and delete it from the list file.
    """
    os.system('clear')
    stm = choose_stream()
    if stm:
        data = utility.get_list_data()
        result  = list(filter(lambda stream: stream[0] != stm.description, data))
        utility.override_list(result)
        input("Stream removed - Enter to continue")

def stream_edit():
    """
    Acts as an interactive menu for a user to modify an existing stream 
    information.
    """
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
    """
    Displays nubmered menu of objects containing a description and function 
    name. The selection from the description calls the function. 

    Args:
        options (list): list of object that contain a text (description) and a 
        function name to be called after selection by number.

    Exceptions:
        KeyboardInterrupt: will exit function if ctrl-C used
        TypeError: will exit function if one of the functions returns an odd 
        choice.
    """
    try:
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
    except KeyboardInterrupt:
        logger.info("control c")
    except TypeError:
        logger.exception("menu_choice")

if __name__ == "__main__":
    logger.info("starting client")

    menu_choice(menus.main_menu_options)
