
import time
def w():
    x=0
    list=[]
    a = time.time()
    while x<20000:
        x += 1
        b=time.time()
        y=b-a
        list.append(y)
        print(y)
    print(list)

def write():
    f = open("testje.txt","w")
    f.write(str(list))
    f.close()
    
w()
write()


