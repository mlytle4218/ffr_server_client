import time



class Recording():
    def __init__(self, id, process, file_details, file_handler, flag, start_time):
        self.id = id
        self.process = process 
        self.file_details = file_details
        self.file_handler = file_handler
        self.flag = flag
        self.start_time = start_time

    def __str__(self):
        print(type(self.id))
        print(type(self.process))
        print(type(self.file_details))
        print(type(self.file_handler))
        print(type(self.flag))
        
        print((self.id))
        print((self.process))
        print((self.file_details))
        print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(self.start_time)))
        # print((self.file_handler))
        # print((self.flag))