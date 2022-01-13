f = open("a.txt", "r")

read = f.read()
if read == 'True':
    print("Not DO STH")
    f.close()
elif read == "False":
    f1 = open("a.txt", "w")
    f1.write("True")
    f1.close()
    shin = input("Wait")
    print("STH")
    f1 = open("a.txt", "w")
    f1.write("False")
    f1.close()

