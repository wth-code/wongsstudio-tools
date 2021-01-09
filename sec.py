import time

last_time = "30"
wait_time = 300

while True:
    t = time.localtime()
    current_time = time.strftime("%S", t)
    if current_time == last_time:
        last_time = str(int(current_time)+wait_time)
        do()