import time
import datetime
import P
import threading
from threading import Thread
import keyboard

# cur = time.time()
# password = input('Nhap password: ')
# duration = int(time.time()) - int(cur)
# print(duration)



# print(str(dt.datetime.now().time())[:-10])
# print(time.ctime())



# timetables = P.readTimeTable('timetable.txt')

# def isAllow(timetables):
#     #Lay ra curTime = [hh:mm]
#     curTime = str(datetime.datetime.now().time())[:-10]

#     for index in range(len(timetables)):
#         if timetables[index].From < P.Time(curTime) and P.Time(curTime) < timetables[index].To:
#             return True, index
#     return False, -1

# isAllow, index = isAllow(timetables)
# if isAllow:
#     print('Children is using')
#     # timetables[index].To
# else: 
#     print('Not in time')

# str = '6:0'
# if len(str) != 5:
#     Find = str.find(':')
#     h = str[:Find]
#     m = str[(Find+1):]
#     while len(h) != 2:
#         h = '0' + h
#     while len(m) != 2:
#         m = '0' + m
# else:
#     h = str[:2]
#     m = str[3:]
# print(h)
# print(m)
def countdown(t):
    while t > 0:
        mins, secs = divmod(t, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        # print(timer, end="\r")
        time.sleep(1)
        t -= 1
        global stop_thread
        # if stop_thread:
        #     break


T = threading.Thread(target=countdown, args=(10,))
# T = threading.Thread(target=countdown, args=(waitTime.toSecond(),))
T.start()
f = open("./file/log.txt")
# while T.is_alive():
log = keyboard.record(until="esc")
    # print("is running")

print(log)
# f.write(log)
# f.close()
                    