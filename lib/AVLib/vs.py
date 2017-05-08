import numpy as np
import cv2
import socket
import time,sys

UDP_IP = "192.168.1.103"
#UDP_IP = "192.168.1.106"
#UDP_PORT = 5005
#UDP_PORT2 = 7000
UDP_PORT =int(sys.argv[1])
UDP_PORT2 = int(sys.argv[2])
cap = cv2.VideoCapture(0)
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.bind (('', UDP_PORT))
while(True):
    ret, frame = cap.read()
    time.sleep(0.04)
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 15]
    result, encimg = cv2.imencode('.jpg', frame, encode_param)
    decimg = cv2.imdecode(encimg, 1)
    cv2.imshow('frame',decimg)


   

    d = encimg.flatten ()
    s = d.tostring ()

    print sys.getsizeof(s)


    #for i in xrange(1):
        
     #   sock.sendto (chr(i)+s[i*46070:(i+1)*46070],(UDP_IP, UDP_PORT))
        #time.sleep(0.04)
    sock.sendto (s,(UDP_IP, UDP_PORT2))
    data, addr = sock.recvfrom(15000)
    frame2 = np.fromstring (data,dtype=np.uint8)
    decimg2 = cv2.imdecode(frame2, 1)
    cv2.imshow('frame1',decimg2)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
