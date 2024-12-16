import asyncio
import time
import m3u8
import requests








async def background_task(url,fhandler):
    path_parts = url.split('/')

    path_parts.pop()
    chunk_size = 1024
    segments_found = []
    while True:
        print("Running in the background...")
        await asyncio.sleep(0.5)
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
                    fhandler.write(chunk)

async def main():
    url = "https://cbcradiolive.akamaized.net/hls/live/2041036-b/ES_R1ETR/adaptive_192/chunklist_ao.m3u8"

    print("Recording video...")
    filename = time.strftime("/home/marc/ffr/test-trt.mp4")
    file_handle = open(filename, 'wb')
    
    #playlist = m3u8.load(url)  # this could also be an absolute filename


    task = asyncio.create_task(background_task(url=url,fhandler=file_handle))

    # Continue running until told to stop
    # while True:
    #     user_input = input("Enter 'stop' to exit: ")
    #     if user_input.lower() == "stop":
    #         break
    #     await asyncio.sleep(0.1)  # Allow other tasks to run
    #time.sleep(10)
    await asyncio.sleep(10)

    # Cancel the background task
    task.cancel()

    try:
        await task
    except asyncio.CancelledError:
        print("Background task cancelled.")
        file_handle.close()

if __name__ == "__main__":
    asyncio.run(main())