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
        

        
        

        
    def video_send(self):
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            cap.open()
        while not self.callEnd:
            ret, vframe = cap.read()
            if not ret:
                continue
            cv2.imshow('Self',vframe)
            time.sleep(G.frame_rate)
            encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 15]
            result, encimg = cv2.imencode('.jpg', vframe, encode_param)
            #decimg = cv2.imdecode(encimg, 1)
            #cv2.imshow('frame',decimg)
            d = encimg.flatten ()
            s = d.tostring ()
            #print sys.getsizeof(s)
            #self.peer.sendMediaPacket("V"+s)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.peer.sendMediaPacket("E")
                break
        
        cap.release()
        cv2.destroyAllWindows()
        return

    def audio_send(self):
        s = pyaudio.PyAudio()
        stream = s.open(format=s.get_format_from_width(self.WIDTH),
                channels=self.CHANNELS,
                rate=self.RATE,
                output=True,
                frames_per_buffer=self.CHUNK)

        while not self.callEnd:
            print("*recording")
            adata  = stream.read(self.CHUNK)
            self.peer.sendMediaPacket("A"+adata)
            print("*done recording")
            #stream.stop_stream()
            #stream.close()
            #p.terminate()
            #s.close()
        return

    def video_read(self):
        #p = pyaudio.PyAudio()
        #stream = p.open(format=p.get_format_from_width(self.WIDTH),
        #                channels=self.CHANNELS,
        #                rate=self.RATE,
        #                output=True,
        #                frames_per_buffer=self.CHUNK)
        
        while True:
            try:
                avdata = self.peer.recieveMediaPacket()
            except:
                continue
            if avdata[0] == "V":
                vdata1 = avdata[1:]
                vframe1 = numpy.fromstring (vdata1,dtype=numpy.uint8)
                decimg1 = cv2.imdecode(vframe1, 1)
                cv2.imshow('External',decimg1)
                if cv2.waitKey(1) & 0xFF == ord ('q'):
                    break
            if avdata[0] == "A":
                adata  = avdata[1:]
                stream.write(adata)
            if avdata[0] == "E":
                self.callEnd = True
                break


    def callAV(self):
        self.callEnd = False
        try:
            threading.Thread(target = self.video_send).start()
            
            #threading.Thread(target = self.audio_send).start()
            threading.Thread(target = self.video_read).start()
        except:
            print ("AVHandler.callAV() failed")
        time.sleep(1)
        #threading.Thread(target = self.video_send).join()
        #threading.Thread(target = self.audio_send).join()
        #threading.Thread(target = self.video_read).join()




