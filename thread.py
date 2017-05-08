import time
import threading

gbVar = 1

def threadFun(tid):
    global gbVar
    x = 0
    while gbVar:
        print "Thread ",tid, "says",x
        x = x+1
        if x == 12:
            gbVar = 0
        time.sleep(1)


class myThread(threading.Thread):
    def __init__(self, tid, name, counter, tfun):
        threading.Thread.__init__(self)
        self.threadID = tid
        self.name = name
        self.counter = counter
        self.tfun = tfun
    def run(self):
        print "Starting thread",self.threadID
        self.tfun(self.threadID)
        print "Exiting",self.name

t1 = myThread(1,"Td 1",1, threadFun)
t2 = myThread(2,"Td 2",2, threadFun)

t1.start()
t2.start()

# try:
#     while True:
#         pass
# except KeyboardInterrupt:
#     print "Fin"
