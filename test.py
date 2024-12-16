import sched
import time

def job():
    print("Hello, world!")

scheduler = sched.scheduler(time.time, time.sleep)

# Run job at 10:30 AM tomorrow
specific_time = time.mktime(time.strptime("2024-12-13 14:36", "%Y-%m-%d %H:%M")) 
scheduler.enterabs(specific_time, 1, job)

scheduler.run()