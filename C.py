import os 
import time
import datetime
import P
import threading
from threading import Thread
import keyboard


def getPassword(filename):
    with open(filename) as f:
        datalist = f.readlines()

    return datalist[0][:-1], datalist[1]

def getCurTime():
    return str(datetime.datetime.now().time())[:-10]

def countdown(t):
    while t > 0:
        mins, secs = divmod(t, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        # print("\n",timer, end="\r")
        time.sleep(1)
        t -= 1
        global stop_thread
        if stop_thread:
            break

    keyboard.press_and_release("enter")

def isAllow(timetables):
    #Lay ra curTime = [hh:mm]
    curTime = getCurTime()

    allow = False
    shutdownTime = None
    nextavailableTime = None
    for index in range(len(timetables)):
        if timetables[index].From < P.Time(curTime) and P.Time(curTime) < timetables[index].To:
            allow = True
            shutdownTime = timetables[index].To
            if index == len(timetables)-1:
                nextavailableTime = timetables[0].From
            else:
                nextavailableTime = timetables[index+1].From

    if allow == False:
        nextavailableTime = curTime
        for time in timetables: 
            if P.Time(nextavailableTime) < time.From:
                nextavailableTime = time.From
        if P.Time(nextavailableTime) == P.Time(curTime):
            nextavailableTime = timetables[0].From
    return allow,shutdownTime,nextavailableTime
    
def main():
    parentPassword, childPassword = getPassword('./file/pw.txt')

    print("Parent: ",parentPassword)
    print("Child: ",childPassword)


    timetables = P.readTimeTable("./file/timetable.txt")
    wrongCount = 0
    global stop_thread
    stop_thread = False
    allow = False
    while True:
    # cur = time.time()
        password = input('Nhap mat khau: ') #C0
    # done = time.time()
    # if done - cur > 15:
    #     break


        #C1
        if password == parentPassword:
            wrongCount = 0
            print('Parent is using')
            #Wait 60p
            # time.sleep(3600)
            print('Time out')
        #C2
        elif password == childPassword:
            wrongCount = 0

            #C2.1
            allow, shutdownTime, nextavailableTime = isAllow(P.readTimeTable("./file/timetable.txt"))
            #C2.1.2
            if allow:
                print('Children is using')
            
                #C2.1.2.1
                waitTime = shutdownTime - P.Time(getCurTime()) 
                print("Time left: ",waitTime)
                print("Next available time: ", nextavailableTime)

                # T = threading.Thread(target=countdown, args=(10,))
                # # T = threading.Thread(target=countdown, args=(waitTime.toSecond(),))
                # T.start()
                # f = open("./file/log.txt")

                # while T.is_alive():
                #     log = keyboard.record()

                # time.sleep(waitTime.toSecond())
                print("Time out")
            #C2.1.1
            elif allow == False:
                print("NOT ALLOW")
                print("Next available time: ", nextavailableTime)

                T = threading.Thread(target=countdown, args=(15,))
                T.start()
                # continue
                while T.is_alive():
                    p2 = ""
                    p2 = input("Nhap lai mat khau: ")

                    if p2 == parentPassword:
                        # wrongCount = 0
                        print('Parent is using')

                        #global stop_thread
                        stop_thread = True  # Kill thread
                        # 60p
                        time.sleep(5)
                        # print('Time out')
                        break
                    elif p2 == "" or p2 != parentPassword:
                        flagShutdown = True
                        continue
            
            #shutdown
            if flagShutdown:
                # print("time out, shutting down!!!")
                break
        else:
            wrongCount +=1 
            print('Wrong password')
            if wrongCount >= 3:
                #delay 10'
                print("Thu lai sau 10 phut")
                # time.sleep(600)
                #shutdown
                break
        flagShutdown = False
        password = None
    #Do Shutdown
    print('Shutdown')

if __name__ == "__main__":
    main()


    
