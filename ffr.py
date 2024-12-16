#!/usr/bin/env python
import sys,csv,os,time,subprocess,argparse
from operator import itemgetter
from subprocess import call
import shutil
import time
import datetime

filePath=None
wait=3


# -f ismv -movflags frag_keyframe

#listFile = '/usr/local/bin/.list.csv'
listFile = '/home/chime/.ffrlist'
log_file = '/home/chime/ffrlog.txt'
def log(input):
    with open(log_file, "a") as myfile:
        string = datetime.datetime.fromtimestamp(
            time.time()).strftime('%Y-%m-%d %H:%M:%S')
        string = string + ' - ' + str(input) + '\n'
        myfile.write(string)

def main_menu():
    log("starting")
    os.system('clear')
    print("number 1 re-cord existing stream")
    print("number 2 Listen to existing stream")
    print("number 3 Add new stream")
    print("number 4 Remove stream")
    print("number 5 Edit existing stream")
    print("number 6 Quit")
    choices=("1","2","3","4","5","6")
    choice_made = None
    while (choice_made == None):
        choice_made = menu_choice(choices)

    if (choice_made=="1"):
        choice = choose_stream()
        if (choice=="-1"):
            main_menu()
        else:
            #record_stream(choice[1], get_path(),choice[2])
            record_stream(choice[1],choice[2])

    elif (choice_made=="2"):
        choice = choose_stream()
        if (choice=="-1"):
            main_menu()
        else:
            play_stream(choice[1])
    elif (choice_made=="3"):
        add_stream()
    elif (choice_made=="4"):
        choice = choose_stream()
        if (choice=="-1"):
            main_menu()
        else:
            remove_stream(choice)
    elif (choice_made=="5"):
        choice = choose_stream()
        if (choice=="-1"):
            main_menu()
        else:
            edit_stream(choice)
    elif (choice_made=="6"):
        sys.exit(0)

def edit_stream(stream):
    os.system('clear')
    print("existing alias: " + stream[0])
    alias=input("Alias for new stream: ")
    print("existing URL: " + stream[1])
    url=input("URL for new stream: ")
    data=get_data()

    for sublist in data:
        if sublist[0] == stream[0] and sublist[1] != url:
            if len(alias) > 0:
                sublist[0] = alias
            if len(url) > 0:
                sublist[1] = youtube_dl_check(url)
                sublist[2] = get_stream_type(sublist[1])
            else:
                if len(sublist) > 2:
                    sublist[2] = get_stream_type(sublist[1])
                else:
                    sublist.append(get_stream_type(sublist[1]))

    with open(listFile, 'w') as out:
    # with open(listFile, 'wb+') as out:
        writer=csv.writer(out)
        writer.writerows(data)
    time.sleep(wait)
    main_menu()

def remove_stream(stream):
    data=get_data()
    # log(data)
    for sublist in data:
        if sublist[0] == stream[0]:
            data.remove(stream)

    with open(listFile, 'w') as out:
    # with open(listFile, 'wb+') as out:
        writer=csv.writer(out)
        writer.writerows(data)
    main_menu()

def choose_stream():
    os.system('clear')
    choices=list()
    stream_list=get_data()
    # log("***************************************************")
    # log("***************************************************")
    # log("***************************************************")
    # log("***************************************************")
    # log(stream_list)
    exit_entry_number=0
    # for each in stream_list:
    #     log(type(each))

    stream_list_cleaned =[]
    for stream in stream_list:
        if (len(stream)) == 3:
            stream_list_cleaned.append(stream)
    for i in range(len(stream_list_cleaned)):
        print("number {0} {1}".format(i+1, stream_list_cleaned[i][0]))
        # log(   "lenght: {0}".format(len(stream_list_cleaned[i]))  )
        # print("number {0} {1}".format(i ,type(stream_list_cleaned[i])))
        exit_entry_number=i+1
        choices.append(str(i+1))

    # for idx, val in enumerate(stream_list_cleaned):
    #     # log(idx)
    #     # log(val)
    #     print("number {0} {1}".format(idx+1 ,val[0]))
    #     exit_entry_number=idx+1
    #     choices.append(str(idx+1))
    choice_made=None
    choices.append(str(exit_entry_number+1))
    print("number {0} Back".format(exit_entry_number+1))
    while (choice_made==None):
        choice_made=menu_choice(choices)
    if (len(stream_list_cleaned) < int(choice_made)):
        return "-1"
    else :
        return stream_list_cleaned[int(choice_made)-1]

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

def add_stream():
    alias=input("Alias for new stream: ")
    if (not check_alias(alias)):
        stream=input("URL for stream: ")
        stream=youtube_dl_check(stream)
        extension=get_stream_type(stream)
        if extension==None:
            print("Problem with that url")
            time.sleep(wait)
            #log(stream)
            #log(extension)
        else:
            new_fields=[alias,stream,extension]
            add_data(new_fields)
            print("New stream added")
        time.sleep(wait)
    else:
        print("This alias already taken")
        time.sleep(wait)
    main_menu()

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

def play_stream(stream):
    #print "number 1 On Board"
    #print "number 2 Ensoniq"
    #print "number 3 DGX"
    #print "number 4 Audigy"
    #card=raw_input("Which sound card. Default is On Board: ")
    #if (card=="" or card=="1"):
    #     call(["mpv","--really-quiet","--no-video","--audio-device=alsa/plughw:CARD=Intel,DEV=0",str(stream)])
    #elif (card=="2"):
    #     call(["mpv","--really-quiet","--no-video","--audio-device=alsa/plughw:CARD=AudioPCI,DEV=0",str(stream)])
    #elif (card=="4"):
    #     call(["mpv","--really-quiet","--no-video","--audio-device=alsa/plughw:CARD=Audigy2,DEV=0",str(stream)])
    #elif (card=="3"):
    #     call(["mpv","--really-quiet","--no-video","--audio-device=alsa/plughw:CARD=DGX,DEV=0", str(stream)])
    #print "Playing {}".format(str(stream))
    #call(["sudo","mpv","--really-quiet","--no-video",str(stream)])
    call(["mpv","--really-quiet","--no-video",str(stream)])
    main_menu()

def get_path():
    print("Input path and filename")
    return input("Path:")

# ffmpeg -i 'concat:/home/chime/test.aac|test-temp.aac' -c copy output.aac
# ffmpeg -i 'concat:/home/chime/test.aac|/home/chime/test-temp.acc' -c copy /home/chime/test-temp-temp.acc

def record_stream(stream, extension):
    filePath = ''
    if append_flag:
        filePath = os.path.splitext(args.append[0])[0]
        filePath += '-temp'
    else:
        filePath = get_path()
    print("number 1 record now")
    print("number 2 record later")
    print("number 3 quit")
    result=input("Choice: ")
    log("extension = {}".format(extension))
    if (result=="1"):
        try:
            if (extension =="mp4"):
                log("mp4")
                while True:
                    test_file = filePath + ".aac"
                    exists = os.path.isfile(test_file)
                    if exists:
                        what_to_do = input('This file exists. Do you want to overwrite or append?')
                        if what_to_do.lower() == 'o':
                            os.remove(filePath +".aac")
                            print("aac recording...")
                            call(["ffmpeg","-reconnect","1","-reconnect_streamed","1","-reconnect_delay_max","300","-re","-loglevel","error","-i",str(stream),"-vn","-c:a","copy",str(filePath+".aac")])
                            time.sleep(wait)
                            break
                        elif what_to_do.lower() == 'a':
                            print("aac recording...")
                            call(["ffmpeg","-reconnect","1","-reconnect_streamed","1","-reconnect_delay_max","300","-re","-loglevel","error","-i",str(stream),"-vn","-c:a","copy",str(filePath+"-temp.aac")])
                            print("appending files")
                            concat = "concat:{}|{}".format(filePath + ".aac", filePath + "-temp.aac")
                            command = ['ffmpeg', '-i',concat,'-c','copy', filePath+"-concat.aac"]
                            # print(command)
                            call(command)
                            shutil.move(filePath + "-concat.aac", filePath + ".aac")
                            os.remove(filePath + "-temp.aac")
                            break
                        else:
                            filePath = get_path()
                    else:
                        print('aac recording...')
                        log('aac recording...')
                        command = ["ffmpeg","-reconnect","1","-reconnect_streamed","1","-reconnect_delay_max","300","-re","-loglevel","error","-i",str(stream),"-vn","-c:a","copy",str(filePath+".aac")]
                        command = ["ffmpeg","-reconnect","1","-reconnect_streamed","1","-reconnect_delay_max","300","-re","-i",str(stream),"-vn","-c:a","copy",str(filePath+".aac")]
                        command = ["ffmpeg","-re","-i",str(stream),"-vn","-c:a","copy",str(filePath+".aac")]
                        p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                        out, err =  p.communicate()

                        log(err)
                        log(out)
                        break

                # print "aac recording..."
                # # call(["ffmpeg","-re","-loglevel","error","-i",str(stream),"-vn","-c:a","copy",str(filePath+"."+extension)])
                # call(["ffmpeg","-re","-loglevel","error","-i",str(stream),"-vn","-c:a","copy",str(filePath+".aac")])

                # if append_flag:
                #     concat = "concat:{}|{}".format(cwd+"/"+args.append[0], cwd+"/"+filePath + ".aac")
                #     print "appending files"
                #     command = ['ffmpeg', '-i',concat,'-c','copy', cwd + "/" + filePath+"-temp.aac"]
                #     call(command)
                #     shutil.move(cwd+'/'+filePath + "-temp.aac", cwd+'/'+args.append[0])
                #     os.remove(filePath + ".aac")


                # call(["mv",str(filePath+"."+extension),str(filePath+".aac")])
            elif (extension =="mp3"):
                while True:
                    test_file = filePath + ".mp3"
                    exists = os.path.isfile(test_file)
                    if exists:
                        what_to_do = input('This file exists. Do you want to overwrite or append?')
                        if what_to_do.lower() == 'o':
                            os.remove(filePath +".mp3")
                            print("mp3 recording...")
                            call(["ffmpeg","-reconnect","1","-reconnect_streamed","1","-reconnect_delay_max","300","-re","-loglevel","error","-i",str(stream),"-vn","-c:a","copy",str(filePath+".mp3")])
                            break
                        elif what_to_do.lower() == 'a':
                            print("mp3 recording...")
                            call(["ffmpeg","-reconnect","1","-reconnect_streamed","1","-reconnect_delay_max","300","-re","-loglevel","error","-i",str(stream),"-vn","-c:a","copy",str(filePath+"-temp.mp3")])
                            print("appending files")
                            concat = "concat:{}|{}".format(filePath + ".mp3", filePath + "-temp.mp3")
                            command = ['ffmpeg', '-i',concat,'-c','copy', filePath+"-concat.mp3"]
                            # print(command)
                            call(command)
                            shutil.move(filePath + "-concat.mp3", filePath + ".mp3")
                            os.remove(filePath + "-temp.mp3")
                            break
                        else:
                            filePath = get_path()
                    else:
                        print('mp3 recording...')
                        call(["ffmpeg","-reconnect","1","-reconnect_streamed","1","-reconnect_delay_max","300","-re","-loglevel","error","-i",str(stream),"-vn","-c:a","copy",str(filePath+".mp3")])
                        break
                # print "mp3 recording..."
                # call(["ffmpeg","-re","-loglevel","error","-i",str(stream),"-c","copy",str(filePath+"."+extension)])

                # if append_flag:
                #     concat = "concat:{}|{}".format(cwd+"/"+args.append[0], cwd+"/"+filePath + ".mp3")
                #     print "appending files"
                #     command = ['ffmpeg', '-i',concat,'-c','copy', cwd + "/" + filePath+"-temp.mp3"]
                #     call(command)
                #     shutil.move(cwd+'/'+filePath + "-temp.mp3", cwd+'/'+args.append[0])
                #     os.remove(filePath + ".mp3")

            elif (extension =="aac"):
                while True:
                    test_file = filePath + ".aac"
                    exists = os.path.isfile(test_file)
                    if exists:
                        what_to_do = input('This file exists. Do you want to overwrite or append?')
                        if what_to_do.lower() == 'o':
                            os.remove(filePath +".aac")
                            print("aac recording...")
                            call(["ffmpeg","-reconnect","1","-reconnect_streamed","1","-reconnect_delay_max","300","-re","-loglevel","error","-i",str(stream),"-vn","-c:a","copy",str(filePath+".aac")])
                            break
                        elif what_to_do.lower() == 'a':
                            print("aac recording...")
                            call(["ffmpeg","-reconnect","1","-reconnect_streamed","1","-reconnect_delay_max","300","-re","-loglevel","error","-i",str(stream),"-vn","-c:a","copy",str(filePath+"-temp.aac")])
                            print("appending files")
                            concat = "concat:{}|{}".format(filePath + ".aac", filePath + "-temp.aac")
                            command = ['ffmpeg', '-i',concat,'-c','copy', filePath+"-concat.aac"]
                            # print(command)
                            call(command)
                            shutil.move(filePath + "-concat.aac", filePath + ".aac")
                            os.remove(filePath + "-temp.aac")
                            break
                        else:
                            filePath = get_path()
                    else:
                        print('aac recording...')
                        #call(["ffmpeg","-reconnect","1","-reconnect_streamed","1","-reconnect_delay_max","300","-re","-loglevel","error","-i",str(stream),"-vn","-c:a","copy",str(filePath+".aac")])
                        command = ["ffmpeg","-reconnect","1","-reconnect_streamed","1","-reconnect_delay_max","300","-re","-loglevel","error","-i",str(stream),"-vn","-c:a","copy",str(filePath+".aac")]
                        p = subprocess.Popen(command, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
                        out, err = p.communicate()
                        log(out)
                        log(err)
                        break

        except Exception as e:
            log(e)
    elif (result=="2"):
        at_command=input("Enter A T command: ")
        hours=input("Enter hours to record: ")
        minutes=input("Enter minutes to record: ")

        sched_cmd = ['at', at_command]
        #sched_cmd = 'at ' + at_command
        command = ""
        p = subprocess.Popen(sched_cmd, stdin=subprocess.PIPE)
        if (extension=="mp4"):
            #print("mp4")
            #print("number {0:0>2}:{1:0>2}:00".format(hours,minutes))
            #print("ffmpeg -re -i "+str(stream)+" -t {0:0>2}:{1:0>2}:00".format(hours,minutes)+ " -vn -c:a copy "+str(filePath+".aac"))
            command = "ffmpeg -reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 300 -re -i "+str(stream)+" -t {0:0>2}:{1:0>2}:00".format(hours,minutes)+ " -vn -c:a copy "+str(filePath+".aac")
        elif (extension =="mp3"):
            #print("mp3")
            #print("number {0:0>2}:{1:0>2}:00".format(hours,minutes))
            #print("ffmpeg -re -i "+str(stream)+" -t {0:0>2}:{1:0>2}:00".format(hours,minutes)+ " -c copy "+str(filePath+"."+extension))
            command = "ffmpeg -reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 300 -loglevel error -i "+str(stream)+" -t {0:0>2}:{1:0>2}:00".format(hours,minutes)+ " -c copy "+str(filePath+"."+extension)
        p.communicate(bytes(command, 'utf-8'))
    else:
        main_menu()
    main_menu()




def menu_choice(choices):
    choice_made=input("Choice: ")
    if choice_made in choices:
        return choice_made
    else:
        print("Invalid choice. Please choose again")
        return None

def get_data():
    with open(listFile, 'rt') as csvfile:
        result = []
        data = list(csv.reader(csvfile))
        # log(data)
        data = sorted(data)
        for datum in data:
            #log(datum)
            if (len(datum) == 3) :
                result.append(datum)
    # data = sorted(data, key=itemgetter(0))
    # log(data)
       # log(result)
        return result
        # return data

def add_data(stream_data):
    with open(listFile, 'a') as f:
        writer = csv.writer(f)
        writer.writerow(stream_data)


def check_alias(alias):
    choice_made = False
    data = get_data()
    for lists in data:
        if(alias == lists[0]):
            choice_made = True
    return choice_made


append_flag = False

parser = argparse.ArgumentParser(description='Record some streams.')
group = parser.add_mutually_exclusive_group()
group.add_argument('-r','--record',nargs=1,help='record stream - must be followed by a known alias')
group.add_argument('-p','--play',nargs=1,help='play a stream  - must be followed by a known alias')
parser.add_argument('-o','--outfile',nargs=1,help='the name of the file about to be recorded')
args=parser.parse_args()


if args.record:
    print("record")
    data = get_data()
    for lst in data:
        if (args.record[0] == lst[0]):
            if args.outfile:
                record_stream(lst[1],args.outfile[0],lst[2])
            else:
                record_stream(lst[1],get_path(),lst[2])

elif args.play:
    print(args.play[0])
    data=get_data()
    if check_alias(args.play[0]):
        for lst in data:
            if (args.play[0] == lst[0]):
                play_stream(lst[1])
    else:
        print("Could not find that alias")


else: # not args.play or not args.record:
    main_menu()

#if len(sys.argv) == 1:
#    main_menu()
#elif len(sys.argv) == 2:
#    data = get_data()
#    if check_alias(sys.argv[1]):
#        for lst in data:
#            if (sys.argv[1] == lst[0]):
#                play_stream(lst[1])
#    else:
#        print "Could not find that alias"
#else:
#    data = get_data()
#    for lst in data:
#        if (sys.argv[1] == lst[0]):
#            record_stream(str(lst[1]),str(sys.argv[2]),lst[2])
            #call(["ffmpeg","-re","-i",str(lst[1]),"-c","copy","-bsf:a","aac_adtstoasc",str(sys.argv[2])])
            # print lst[0]
            # print lst[1]
            # print lst[2]
            # if (lst[1]=="-1"):
            #     # print "no flag"
            #     call(["sudo","youtube-dl", "-o",sys.argv[2],lst[2]])
            # else:
            #     call(["sudo","youtube-dl","-o",sys.argv[2],"-f",lst[1],lst[2]])
        # else:
            # print "Could not find that alias"
            # sys.exit(0)

#sudo ffmpeg -re -i <url> -c copy -bsf:a aac_adtstoasc recording.mp4


