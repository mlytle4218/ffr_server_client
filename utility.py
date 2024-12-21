import csv
import ffr_config
from client_logger import logger
import subprocess
import tabCompleter
import readline

class StreamData():
    """
    General object to represent the data used to represent the information 
    needed for recording.
    """
    def __init__(self, description, url, extension):
        """_summary_

        Args:
            description (str): the alias for the stream
            url (str): the URL from which to record
            extension (str): the extension determined from probing the URL
        """
        self.description = description
        self.url = url
        self.extension = extension

def get_list_data():
    """
    Opens the csv list of saved streams information and returns as a sorted
    list.

    Returns:
        list: list of objects representing the alias, URL, and extension type
        of a stream
    """
    try:
        with open(ffr_config.LINK_LIST, 'rt') as csvfile:
            return sorted(list(csv.reader(csvfile)))
    except Exception:
        logger.exception("utility:get_list_data")
        return None
    
def youtube_dl_check(stream):
    """
    Utility which uses youtube-dl to clean up the URL if the original URL is a 
    proxy for another URL. If youtube-dl returns an error, then it checks that
    it is a meu or m3u8 file. 

    Args:
        stream (str): The actual URL of the stream

    Returns:
        str: recordable URL
    """
    youtube_dl_cmd = ['youtube-dl','-g',stream]
    p = subprocess.Popen(youtube_dl_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output,err = p.communicate()
    print("checking with youtube-dl")
    logger.info("youtube-dl response - {}".format(output))
    if b"ERROR" in output:
        print("giving up on youtube-dl approach")
    else:
        print("not giving up")
        for line in output.splitlines():
            if b"m3u" in line:
                stream = line
    # print(stream)
    return stream

def get_stream_type(stream):
    """
    Utility that uses ffprobe to get information about the media type associated
    with a stream URL

    Args:
        stream (str): the recordable URL

    Returns:
        str: The extension associated with the media type detected by ffprobe.
    """
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
    """
    Appends an instance of stream information to the saved file.

    Args:
        stream_data (list): a list containing the alias, URL, and extension of 
        the new stream
    """
    with open(ffr_config.LINK_LIST, 'a') as f:
        writer = csv.writer(f)
        writer.writerow(stream_data)

def override_list(list_data):
    """
    Utility to completely override the data in the saved stream file - this is 
    used when a choice is removed. Easier to over write everything.

    Args:
        list_data (list of lists): a list of lists each containing the alias, 
        URL, and extension of a stream
    """
    with open(ffr_config.LINK_LIST, 'w') as f:
        writer = csv.writer(f)
        writer.writerows(list_data)

def load_saved_stream_data():
    """_summary_

    Returns:
        _type_: _description_
    """
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

def get_file_path(extenstion):
    t = tabCompleter.tabCompleter()
    readline.set_completer_delims('\t')
    readline.parse_and_bind("tab: complete")
    readline.set_completer(t.pathCompleter)
    path = input("Enter file path: ")
    return path + "." + extenstion


