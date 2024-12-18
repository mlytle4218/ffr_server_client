import sched
import time
import datetime
import calendar

def job():
    print("Hello, world!")

# scheduler = sched.scheduler(time.time, time.sleep)

# # Run job at 10:30 AM tomorrow
# specific_time = time.mktime(time.strptime("2024-12-13 14:36", "%Y-%m-%d %H:%M")) 
# scheduler.enterabs(specific_time, 1, job)

# scheduler.run()

today = datetime.datetime.now()

# result = {}
print(today.month)
# print(today.day)
print(today.year)

print(calendar.monthrange(today.year, today.month)[1])

# result["month"] = input("Enter month (default: {}): ".format(today.month)) or today.month

# print(result["month"])


# datetime.datetime.strptime('Jun 1 2005  1:33PM', '%b %d %Y %I:%M%p')
# datetime.datetime.strptime('06-1-2024 1:56PM', '%m-%d-%Y %I:%M%p')

# # datetime in string format for may 25 1999
# input = '2021/05/25'
# format = '%Y/%m/%d'
 
# # convert from string format to datetime format
# datetime = datetime.datetime.strptime(input, format)
