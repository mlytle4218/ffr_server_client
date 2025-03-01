import time



class Recording():
    def __init__(self, id, process, file_details, file_handler, flag, start_time, end_time=None):
        self.id = id
        self.process = process 
        self.file_details = file_details
        self.file_handler = file_handler
        self.flag = flag
        self.start_time = start_time,
        self.end_time = end_time

    def __str__(self):
        print((self.id))
        print((self.process))
        print((self.file_details))
        print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(self.start_time)))

    def get_start_time(self):
        return self.start_time[0]