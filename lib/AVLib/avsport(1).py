import numpy
import cv2
import socket
import time,sys
import pyaudio
import threading


def video_send():
    while(True):
        ret,vframe = cap.read()
        cv2.imshow('frame',vframe)
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 15]
        result, encimg = cv2.imencode('.jpg', vframe, encode_param)
        d = encimg.flatten ()
        s = d.tostring ()
        #print sys.getsizeof(s)
        sock.sendto ("V"+s,(UDP_IP, UDP_PORT))
        print 'vframe sent'
        if cv2.waitKey(1) & 0xFF == ord ('q'):
            AVend = True
            break
        
        i=1
        print ' trying to receive'
        for i in range(4) :
            try:
                avdata, addr = sock.recvfrom(20000)
                print 'received data :',i
            except:
                continue
            if avdata[0] == "V":
                vdata1 = avdata[1:]
                vframe1 = numpy.fromstring (vdata1,dtype=numpy.uint8)
                decimg1 = cv2.imdecode(vframe1, 1)
                cv2.imshow('frame2',decimg1)
                print 'decoded :',i
                i=i+1
            
        
            if avdata[0] == "A":
                    adata  = avdata[1:]
                    stream2.write(adata)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                AVend = True
                break
    #cap.release()
    return

def audio_send():    
    while True:
        #print("*recording")
        adata  = stream.read(CHUNK)
        sock.sendto ("A"+adata,(UDP_IP, UDP_PORT))
        print("audio sent")
        if AVend == True :
            return
    return

CHUNK = 512
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 20000
WIDTH = 2
pi = pyaudio.PyAudio()
stream2 = pi.open(format=pi.get_format_from_width(WIDTH),
                channels=CHANNELS,
                rate=RATE,
                output=True,
                frames_per_buffer=CHUNK)

p = pyaudio.PyAudio()
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)
#UDP_IP = "127.0.0.1"
UDP_IP = "192.168.1.106"
UDP_PORT = 5005
#UDP_PORT2 = 7001
#UDP_PORT =int(sys.argv[1])
#UDP_PORT2 = int(sys.argv[2])

cap = cv2.VideoCapture(0)
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.settimeout(.01)
sock.bind (('', UDP_PORT))
AVend = False        
try:
    threading.Thread(target = audio_send).start()
    threading.Thread(target = video_send).start()
    #threading.Thread(target = video_read).start()
except:
    print ("failed 1")

