import numpy
import cv2
import socket
import time,sys
import pyaudio
import threading

def video_send():
    while(True):
        ret, vframe = cap.read()
        cv2.imshow('frame',vframe)
        time.sleep(0.04)
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 15]
        result, encimg = cv2.imencode('.jpg', vframe, encode_param)
        #decimg = cv2.imdecode(encimg, 1)
        #cv2.imshow('frame',decimg)
        d = encimg.flatten ()
        s = d.tostring ()
        #print sys.getsizeof(s)
        sock.sendto ("V"+s,(UDP_IP, UDP_PORT))
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    return

def audio_send():
    
    while True:
        print("*recording")
        adata  = stream.read(CHUNK)
        sock.sendto ("A"+adata,(UDP_IP, UDP_PORT))
        print("*done recording")
        #stream.stop_stream()
        #stream.close()
        #p.terminate()
        #s.close()
    return

CHUNK = 512
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 20000

p = pyaudio.PyAudio()
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)
UDP_IP = "127.0.0.1"
#UDP_IP = "192.168.1.105"
UDP_PORT = 5005
#UDP_PORT2 = 7001
#UDP_PORT =int(sys.argv[1])
#UDP_PORT2 = int(sys.argv[2])
cap = cv2.VideoCapture(0)
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
#sock2 = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
#sock.bind (('', UDP_PORT))
        
try:
    threading.Thread(target = video_send).start()
    threading.Thread(target = audio_send).start()
except:
    print ("failed 1")

#video_send()
