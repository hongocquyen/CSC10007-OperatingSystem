import os
import time
import datetime
import P
import threading
from threading import Thread


def getPassword(filename):
    with open(filename) as f:
        datalist = f.readlines()

    return datalist[0][:-1], datalist[1]


def getCurTime():
    return str(datetime.datetime.now().time())[:-10]


def isAllow(timetables):
    # Lay ra curTime = [hh:mm]
    curTime = getCurTime()
    for index in range(len(timetables)):
        if timetables[index].From < P.Time(curTime) and P.Time(curTime) < timetables[index].To:
            return True, index
    return False, -1


parentPassword, childPassword = getPassword('./file/pw.txt')


timetables = P.readTimeTable("./file/timetable.txt")
# print(timetables[0].From)
countWrong = 0


def countdown(t):
    while t:
        mins, secs = divmod(t, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        print(timer, end="\r")
        time.sleep(1)
        t -= 1
        global stop_thread
        if stop_thread:
            break


stop_thread = False

def check(thread1, thread2):


def main():
    wrongCount = 0
    while True:
        cur = time.time()
        password = input('Nhap mat khau: ')
        done = time.time()
        # if done - cur > 5:
        #     break
        if password == parentPassword:
            wrongCount = 0
            print('Parent is using')
            # 60p

            # global stop_thread
            # stop_thread = True  # Kill thread

            time.sleep(5)
            print('Time out')
        elif password == childPassword:
            wrongCount = 0

            #C2.1.2
            # isAllow, index = isAllow(timetables)
            # if isAllow:
            #     print('Children is using')

            #     waitTime = timetables[index].To - P.Time(getCurTime)
            #     print("Time left until shutdown: ", waitTime)
            #     # time.sleep(waitTime.toSecond())
            #     print("Next available time: ", nextTime)
            #     print("Time out")
            
            print("Notice")
            T1 = threading.Thread(target=countdown, args=(15,))
            T1.start()
            # continue
            while T1.is_alive():
                p2 = ""
                p2 = input("Nhap lai mat khau: ")
                if p2 == parentPassword:
                    # wrongCount = 0
                    print('Parent is using')
                    

                    global stop_thread
                    stop_thread = True  # Kill thread
                    # 60p
                    time.sleep(5)
                    # print('Time out')
                    break
                elif p2 == "" or p2 != parentPassword:
                    continue
            print("time out, shutting down!!!")

        else:
            wrongCount += 1
            print('Wrong password')
            if wrongCount >= 3:
                break

        password = None


main()
print('Shutdown')


########