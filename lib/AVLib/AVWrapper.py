##Wrapper class for AV operations

import numpy
import cv2
import socket
import time,sys
import pyaudio
import threading
import Resources._globals as G




class AVHandler:
    def __init__(self, peer):
        self.peer = peer
        self.CHUNK = 512
        self.AUDIO_FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 20000
        self.WIDTH = 2
        

        
        

        
    def video_send(self):
        self.cap = cv2.VideoCapture(0)
        while(True):
            ret, vframe = cap.read()
            cv2.imshow('frame',vframe)
            time.sleep(G.frame_rate)
            encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 15]
            result, encimg = cv2.imencode('.jpg', vframe, encode_param)
            #decimg = cv2.imdecode(encimg, 1)
            #cv2.imshow('frame',decimg)
            d = encimg.flatten ()
            s = d.tostring ()
            #print sys.getsizeof(s)
            self.peer.sendMediaPacket("V"+s)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            cap.release()
        return

    def audio_send(self):
        s = pyaudio.PyAudio()
        stream = s.open(format=p.get_format_from_width(self.WIDTH),
                channels=self.CHANNELS,
                rate=self.RATE,
                output=True,
                frames_per_buffer=self.CHUNK)

        while True:
            print("*recording")
            adata  = stream.read(CHUNK)
            self.peer.sendMediaPacket("A"+adata)
            print("*done recording")
            #stream.stop_stream()
            #stream.close()
            #p.terminate()
            #s.close()
        return

    def video_read():
        p = pyaudio.PyAudio()
        stream = p.open(format=p.get_format_from_width(self.WIDTH),
                        channels=self.CHANNELS,
                        rate=self.RATE,
                        output=True,
                        frames_per_buffer=self.CHUNK)
        
        while True:
            avdata = self.peer.recieveMediaPacket()
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


    def callAV(self):
        try:
            threading.Thread(target = video_send).start()
            threading.Thread(target = audio_send).start()
            threading.Thread(target = video_read).start()
        except:
            print ("AVHandler.callAV() failed")

