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
        self.callEnd = False
        

        
        

        
    def video(self):
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            cap.open()

        p = pyaudio.PyAudio()
        stream = p.open(format=p.get_format_from_width(self.WIDTH),
                       channels=self.CHANNELS,
                       rate=self.RATE,
                       output=True,
                       frames_per_buffer=self.CHUNK)

        while not self.callEnd:
            ret, vframe = cap.read()
            if not ret:
                continue
            
            cv2.imshow('Self',vframe)
            encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 15]
            result, encimg = cv2.imencode('.jpg', vframe, encode_param)

            d = encimg.flatten ()
            s = d.tostring ()
            

            self.peer.sendMediaPacket("V"+s)

            for i in range(4) :
                try:
                    avdata = self.peer.recieveMediaPacket()
                except:
                    continue
                
                if avdata == None:
                    continue
            
                if avdata[0] == "V":
                    vdata1 = avdata[1:]
                    vframe1 = numpy.fromstring (vdata1,dtype=numpy.uint8)
                    decimg1 = cv2.imdecode(vframe1, 1)
                    cv2.imshow('Other',decimg1)
                    #print 'decoded :',i
                    
            
        
                elif avdata[0] == "A":
                    adata  = avdata[1:]
                    stream.write(adata)

                elif avdata[0] == 'E':
                    self.callEnd = True

            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.peer.sendMediaPacket("E")
                time.sleep(1)
                self.peer.sendMediaPacket("E")
                self.peer.sendMediaPacket("E")
                self.peer.sendMediaPacket("E")
                self.callEnd = True
                break
        
        cap.release()
        cv2.destroyAllWindows()
        return

    def audio_send(self):
        s = pyaudio.PyAudio()
        stream = s.open(format=self.AUDIO_FORMAT,
                channels=self.CHANNELS,
                rate=self.RATE,
                input=True,
                frames_per_buffer=self.CHUNK)
        print "audio_send: Recording audio"
        while not self.callEnd:
            adata  = stream.read(self.CHUNK)            
            self.peer.sendMediaPacket("A"+adata)
        return



    def callAV(self):
        self.callEnd = False
        try:
            videoThread = threading.Thread(target = self.video)
            audioSendThread = threading.Thread(target = self.audio_send)
            
            videoThread.start()
            audioSendThread.start()
            
        except:
            print ("AVHandler.callAV() failed")
        videoThread.join()
        print "End call"

        
    def rejectAV(self):
        for i in range(G.noOfIterations):
            time.sleep(0.5)
            self.peer.sendMediaPacket("E")
        return

