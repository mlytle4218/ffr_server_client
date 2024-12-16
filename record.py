import m3u8

url ="http://hatsubservices.ottc.pro/GNRVUQPGFJ/N77HKXQEQE/9334"
url = "https://cbcradiolive.akamaized.net/hls/live/2041036-b/ES_R1ETR/adaptive_192/chunklist_ao.m3u8"
# url = "https://cbcradiolive.akamaized.net/hls/live/2041036-b/ES_R1ETR/adaptive_192/7tkpsjgt/00000045/media_85974.aac"
# url = "https://stream.live.vc.bbcmedia.co.uk/bbc_world_service"

import time
import requests


print("Recording video...")
filename = time.strftime("/home/marc/ffr/test-trt.mp4")
# # filename = time.strftime("/home/chime/scripts/" + "%Y%m%d%H%M%S",time.localtime())+".mp4"
file_handle = open(filename, 'wb')
chunk_size = 1024

# with requests.Session() as session:
#     response = session.get(url, stream=True)
#     for chunk in response.iter_content(chunk_size=chunk_size):
#         if chunk:
#             file_handle.write(chunk)

#     file_handle.close()



# res = requests.get(url)
# print(res.text)


# playlist = m3u8.load(url)
# # print(playlist.dumps())

# # if you want to write a file from its content

# playlist.dump(url)

playlist = m3u8.load(url)  # this could also be an absolute filename

path_parts = url.split('/')

path_parts.pop()

segments_found = []


# for seg in playlist.segments:
#     print((seg.uri))
#     segment_filename = seg.uri.split('/').pop()
#     print(segment_filename)
#     print((seg.duration))
#     pp = path_parts.copy()
#     pp.append(seg.uri)
#     new_path = '/'.join(pp)
#     print(new_path)
#     data = requests.get(new_path)
#     for chunk in data.iter_content(chunk_size=chunk_size):
#         file_handle.write(chunk)
#     print(type(data))
#     print()

if ".m3u" in url:
    print("m3u8")


for i in range(10):
    playlist = m3u8.load(url)
    print(len(playlist.segments))
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
            segment_filename = seg.uri.split('/').pop()
        #     print(segment_filename)
        #     print((seg.duration))
            pp = path_parts.copy()
            pp.append(seg.uri)
            new_path = '/'.join(pp)
        #     print(new_path)
            data = requests.get(new_path)
            for chunk in data.iter_content(chunk_size=chunk_size):
                file_handle.write(chunk)


    time.sleep(2)

print(segments_found)



file_handle.close()

# print(playlist.segments)
# print(playlist.target_duration)