import os

timetables = []

class Time:
    def __init__(self,str):
        if len(str) != 5:
            Find = str.find(':')
            h = str[:Find]
            m = str[(Find+1):]
            while len(h) != 2:
                h = '0' + h
            while len(m) != 2:
                m = '0' + m
        else:
            h = str[:2]
            m = str[3:]

        self.hour = int(h)
        self.minute = int(m)

    def __eq__(self, other):
        if self.hour == other.hour and self.minute == other.minute:
            return True
        return False

    def __lt__(self,other):
        if self.hour < other.hour: return True
        elif self.hour == other.hour:
            if self.minute < other.minute: return True
        else :
            return False

    def __repr__(self)->str:
        strHour = str(self.hour)
        while len(strHour) <=1:
            strHour = '0' + strHour
        strMinute = str(self.minute)
        while len(strMinute) <=1:
            strMinute = '0' + strMinute
        return strHour + ":" + strMinute
    def toSecond(self):
        return self.hour*3600 + self.minute*60
    
    def __add__(self, other):
        res = Time("00:00")
        res.minute = self.minute + other.minute
        if res.minute >= 60:
            res.minute -= 60
            res.hour = self.hour + other.hour + 1

        else:
            res.hour = self.hour + other.hour
        return res   

    def __sub__(self, other):
        res = Time("00:00")
        res.minute = self.minute - other.minute
        if res.minute <= 0:
            res.minute += 60
            res.hour = self.hour - other.hour - 1

        else:
            res.hour = self.hour - other.hour
        return res      

class TimeTable:
    def __init__(self,F = '00:00',T = '00:00',D = 0,I = 0,S = 0):
        self.From = Time(F)
        self.To = Time(T)
        self.Duration = D
        self.Interrupt = I
        self.Sum = S

    def __str__(self)->str:
        return str(self.Duration)

    def editFrom(self,F):
        self.From = Time(F)
    def editTo(self,T):
        self.To = Time(T)
    def editDuration(self, D):
        self.Duration = D
    def editInterrupt(self, I):
        self.Interrupt = I
    def editSum(self, S):
        self.Sum = S
        
    def Show (self):
        print ("From: ", self.From)
        print ("To: ", self.To)
        print ("Duration: ", self.Duration)
        print ("Interrupt: ", self.Interrupt)
        print ("Sum: ", self.Sum)    

# Tim khung thoi gian -> Dieu chinh
def findTimeTable(timetables, From, To):
    for i in range(len(timetables)):
        if timetables[i].From == From and timetables[i].To == To:
            return i
    return None

def readTimeTable(filename):
    # timetables = []

    #Doc file timetable luu vao datalist
    with open(filename) as f:
        datalist = f.readlines()

    #Xu ly chuoi voi moi line trong datalist, luu vao timetables
    for line in datalist:
        attributes = line.split(' ')
        attributes[-1] = attributes[-1].replace('\n','')

        timetable = TimeTable()
        
        for a in attributes:
            if a[0] == 'F':
                timetable.From = Time(a.replace('F',''))
            elif a[0] == 'T':
                timetable.To = Time(a.replace('T',''))
            elif a[0] == 'D':
                timetable.Duration = a.replace('D','')
            elif a[0] == 'I':
                timetable.Interrupt = a.replace('I','')
            elif a[0] == 'S':
                timetable.Sum = a.replace('S','')
        timetables.append(timetable)
    return timetables

# Dieu chinh thoi gian
def Adjust (index):
    while(True):
        os.system("cls")
        print("0. Thoat")
        print("1. Dieu chinh From")
        print("2. Dieu chinh To")
        print("3. Dieu chinh Duration")
        print("4. Dieu chinh Interrupt")
        print("5. Dieu chinh Sum")

        choice = input("Nhap lua chon: ")
        if choice == '0':
            break
        elif choice == '1':
            print("Nhap -From- moi theo cu phap: [hh:mm]")
            F = input("New From: ")
            timetables[index].editFrom(F)
        elif choice == '2':
            print("Nhap -To- moi theo cu phap: [hh:mm]")
            T = input("New To: ")
            timetables[index].editTo(T)
        elif choice == '3':
            D = input("Nhap -Duration- moi: ")
            timetables[index].editDuration(D)
        elif choice == '4':
            I = input("Nhap -Interrupt- moi: ")
            timetables[index].editInterrupt(I)
        elif choice == '5':
            S = input("Nhap -Sum- moi: ")
            timetables[index].editSum(S)
        else:
            print("Nhap lai lua chon!!")
    return "Cap nhat thanh cong"

def Menu (timetables):

    while(True):
        os.system('cls')
        print("MENU")
        print("0. Thoat")
        print("1. Xem Cac Khung gio")
        print("2. Dieu chinh khung gio")
        
        choice = input("Nhap lua chon: ")
        if choice == '1':
            i = 1
            for t in timetables:
                print("Khung gio thu", i)
                t.Show()
                i += 1
            os.system("pause")
        elif choice == '2':
            #Kiem tra active
            fin = open("./file/flagActive.txt","r")
            data = fin.read()
            if data == "True":
                print("Chuc nang dang duoc su dung o mot thiet bi khac")
                fin.close()
                break
            elif data == "False":
                #Dat lai trang thai: isActive = True
                fout = open("./file/flagActive.txt","w")
                fout.write("True")
                fout.close()

                print("Nhap khung gio: ")
                F = input("From: ")
                T = input("To: ")
                index = findTimeTable(timetables, Time(F), Time(T))
                if index == None:
                    print("Khong tim thay timetable phu hop")
                else:
                    res = Adjust(index)
                    print(res)
                os.system("pause")
                
                #Dat lai trang thai: isActive = False
                fout = open("./file/flagActive.txt","w")
                fout.write("False")
                fout.close()
            
        elif choice == '0':
            break
        else:
            print("Nhap lai lua chon!!")
            os.system("pause")

def writeTimeTable(timetables, filename):
    if len(timetables) == 0: 
        return None
    lines = []
    for t in timetables:
        line = ''
        line += 'F' + str(t.From) + ' ' + 'T' + str(t.To) + ' '
        if t.Duration != 0:
            line += 'D' + t.Duration + ' '
        if t.Interrupt != 0:
            line += 'I' + t.Interrupt + ' '
        if t.Sum != 0:
            line += 'S' + t.Sum + ' '
        line = line[:-1] + '\n'
        lines.append(line)
    
    lines[len(lines)-1] = lines[len(lines)-1][:-1]
    f = open(filename,'w')
    for line in lines:
        f.write(line)

def main():

    timetables = readTimeTable('./file/timetable.txt')

    Menu(timetables)

    writeTimeTable(timetables,'./file/timetable.txt')

if __name__ == '__main__':
    main()


