import os 
import time
import datetime
import P


def getPassword(filename):
    with open(filename) as f:
        datalist = f.readlines()

    return datalist[0][:-1], datalist[1]

def getCurTime():
    return str(datetime.datetime.now().time())[:-10]

def isAllow(timetables):
    #Lay ra curTime = [hh:mm]
    curTime = getCurTime()
    for index in range(len(timetables)):
        if timetables[index].From < P.Time(curTime) and P.Time(curTime) < timetables[index].To:
            return True, index
    return False, -1
    
parentPassword, childPassword = getPassword('pw.txt')

print("Parent: ",parentPassword)
print("Child: ",childPassword)


timetables = P.readTimeTable("timetable.txt")
print(timetables[0].From)
countWrong = 0

while True:
    cur = time.time()
    password = input('Nhap mat khau: ')
    done = time.time()
    if done - cur > 5:
        break
    if password == parentPassword:
        wrongCount = 0
        print('Parent is using')
        #60p
        time.sleep(5)
        print('Time out')
    elif password == childPassword:
        wrongCount = 0

        isAllow, index = isAllow(timetables)
        if isAllow:
            print('Children is using')
            
            waitTime = timetables[index].To - P.Time(getCurTime) 
            print("Wait: ",waitTime)
            # time.sleep(waitTime.toSecond())
            print("Time out")

    else:
        countWrong +=1 
        print('Wrong password')
        if countWrong >= 3:
            break

    password = None
print('Shutdown')


    
