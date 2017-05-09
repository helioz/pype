import socket
import numpy
import time
import cv2
import pyaudio
import threading

UDP_IP = "127.0.0.1"
UDP_PORT = 5005
#UDP_PORT2 = 7001
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
#sock2 = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
CHUNK = 512
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 20000
WIDTH = 2
p = pyaudio.PyAudio()
stream = p.open(format=p.get_format_from_width(WIDTH),
                channels=CHANNELS,
                rate=RATE,
                output=True,
                frames_per_buffer=CHUNK)
        
def video_read():
    sock.bind ((UDP_IP, UDP_PORT))
    while True:
        avdata, addr = sock.recvfrom(20000)
        if avdata[0] == "V":
            vdata = avdata[1:]
            vframe = numpy.fromstring (vdata,dtype=numpy.uint8)
            decimg = cv2.imdecode(vframe, 1)
            cv2.imshow('frame',decimg)
            if cv2.waitKey(1) & 0xFF == ord ('q'):
                break
        if avdata[0] == "A":
            adata  = avdata[1:]
            stream.write(adata)
            
#def audio_read():
       
        #while True:
            #adata,addr = sock.recvfrom(4096)
            #if adata[0] == "A":
                #adata  = adata[1:]
                #stream.write(adata)
        
#try:
    #threading.Thread(target = video_read).start()
    #threading.Thread(target = audio_read).start()
#except:
    #print ("failed 2")

#sock.close()
#sock2.close()
video_read()
