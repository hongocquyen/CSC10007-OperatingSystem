import os 
import time
import datetime
import P
import threading
from threading import Thread
import keyboard
from pynput.keyboard import Listener

def getPassword(filename):
    with open(filename) as f:
        datalist = f.readlines()

    return datalist[0][:-1], datalist[1]

def getCurTime():
    return str(datetime.datetime.now().time())[:-10]

def keyLog(key):
    key = str(key)
    if key == "Key.esc":
        raise SystemExit(0)
    
    with open("./file/log.txt", "a") as logfile:
        logfile.write(str(P.Time(getCurTime())) + ": " + key + "\n")
    
    print(key)

def countdown(t):
    flagEnter = True
    while t > 0:
        # mins, secs = divmod(t, 60)
        # timer = '{:02d}:{:02d}'.format(mins, secs)
        # print("\n",timer, end="\r")
        time.sleep(1)
        t -= 1
        global stop_thread
        if stop_thread:
            flagEnter = False
            break

    if flagEnter:
        keyboard.press_and_release("enter")

def countdownKeyLog(t):
    while t > 0:
        # mins, secs = divmod(t, 60)
        # timer = '{:02d}:{:02d}'.format(mins, secs)
        # print("\n",timer, end="\r")
        time.sleep(1)
        t -= 1
        if t == 60: 
            print("One minute to shutdown")
        # global stop_thread
        # if stop_thread:
        #     break

    keyboard.press_and_release("esc")

def isAllow(timetables):
    #Lay ra curTime = [hh:mm]
    curTime = getCurTime()

    allow = False
    shutdownTime = None
    nextavailableTime = None
    for index in range(len(timetables)):
        # Kiem tra neu curTime nam trong khoang [From:To]
        if timetables[index].From < P.Time(curTime) and P.Time(curTime) < timetables[index].To:
            allow = True
            shutdownTime = timetables[index].To
            #Neu la khoang thoi gian cuoi cung trong ngay thi lay thoi gian bieu lai tu dau
            if index == len(timetables)-1:
                nextavailableTime = timetables[0].From
            #Neu khong phai khoang thoi gian cuoi cung thi lay thoi gian tiep theo
            else:
                nextavailableTime = timetables[index+1].From

    if allow == False:
        nextavailableTime = curTime
        #Kiem tra thoi gian duoc su dung may gan nhat trong timetables
        for time in timetables: 
            if P.Time(nextavailableTime) < time.From:
                nextavailableTime = time.From
        if P.Time(nextavailableTime) == P.Time(curTime):
            nextavailableTime = timetables[0].From
    return allow,shutdownTime,nextavailableTime
    
def main():
    #Lay password tu file password
    parentPassword, childPassword = getPassword('./file/pw.txt')

    # print("Parent: ",parentPassword)
    # print("Child: ",childPassword)


    timetables = P.readTimeTable("./file/timetable.txt")
    wrongCount = 0
    global stop_thread
    stop_thread = False
    allow = False
    while True:
        password = input('Enter password: ') #C0

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

                T = threading.Thread(target=countdownKeyLog, args=(10,))
                # T = threading.Thread(target=countdown, args=(waitTime.toSecond(),))
                T.start()

                
                with Listener(on_press=keyLog) as keylogger:
                    keylogger.join()

                
                flagShutdown = True
                print("Time out")
            #C2.1.1
            elif allow == False:
                print("NOT ALLOW")
                print("Next available time: ", nextavailableTime)

                T = threading.Thread(target=countdown, args=(5,))
                T.start()
                # continue
                while T.is_alive():
                    pw = ""
                    pw = input("Enter password: ")

                    if pw == parentPassword:
                        # wrongCount = 0
                        print('Parent is using')
                        flagShutdown = False
                        #global stop_thread
                        stop_thread = True  # Kill thread
                        # 60p
                        # time.sleep(3600)
                        time.sleep(5)
                        print('Time out')
                        break
                    elif pw == "":
                        flagShutdown = True
                    elif pw != parentPassword:
                        continue
            #shutdown
            if flagShutdown:
                # print("Time out, shutting down!!!")
                break
        else:
            wrongCount +=1 
            print('Wrong password')
            if wrongCount >= 3:
                #delay 10'
                print("Try again in 10 minutes")
                # time.sleep(600)

                #shutdown
                # break
        flagShutdown = False
        password = None
    #Do Shutdown
    print('Shutdown')
    # os.system("shutdown -s -t 1")

if __name__ == "__main__":
    main()


    
