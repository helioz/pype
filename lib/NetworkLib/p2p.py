##Peer2peer library for establishing peer connection and send and recieve data
import Resources._globals as G
import socket
import sys
import time
import lib.NetworkLib.network_support as netAlgo

getaddrm = 'getaddr'
getpeerm = 'getpeer'
initm = 'init'
pollm = 'poll'
getconm = 'getcon'
endm = 'end'

separator = '_'

class Peer:
    def __init__(self, net_addr):

        self.net_addr = net_addr
        self.isPunched = False

        
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.settimeout(G.punchTimeout)
	for p in range(G.nOfIteration):
            try:
	        self.s.bind(('',G.PORT_local))
                break
            except:
                print "Peer init: Failed to bind port, retrying"
        try:
	    self.s.connect(netAlgo.stringToTuple(self.net_addr))
        except:
            print "Peer init: Bad address for peer."
            

        
    def __str__(self):
        return "Peer : "+self.net_addr
    
    def __repr__(self):
        return "Peer : "+self.net_addr


    
    def makeConnection(self):
        
        for i in range(G.nOfIteration) :

            if self.sendTextPacket('punch'):

                self.s.settimeout(G.punchTimeout)

                try :
		    data = self.s.recv(G.packet_maxsize)                    
	        except :
                    time.sleep(1)
		    continue

	        if data == 'punch' :
		    self.sendTextPacket('punched')
		    self.isPunched = True
		    return True

                if data == 'punched' :
		    self.isPunched = True
		    return True

	return False
    

    def sendMediaPacket(self, data_bStream):
        try:
	    self.s.send(data_bStream)
            return True
        except:
            return False



    def recieveMediaPacket(self):
        self.s.settimeout(G.mediaTimeOut)
        try:
	    data_bStream = self.s.recv(G.mediaPacket_maxsize)
            return data_bStream
        except:
            return None




    def sendTextPacket(self, data_bStream):
        try:
	    self.s.send(data_bStream)
            return True
	except:
            return False

        
    def recieveTextPacket(self, timeout = G.punchTimeout):
        self.s.settimeout(timeout)
	try:
	    data_bStream = self.s.recv(G.packet_maxsize)
	    if data_bStream != 'punched' and data_bStream != 'punch' and data_bStream != None :
		return data_bStream
            
	    elif data_bStream == 'punch' :
		self.send('punched')
		return self.recieveTextPacket()
	    else :
		return self.recieveTextPacket()
	except:
            #print "receiveTextPacket failed"
	    return None
                  



class SupportServer:
    def __init__(self):
        self.ip_addr = G.IPADDR_support_server
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.settimeout(G.punchTimeout)
        for p in range(G.nOfIteration):
            try:
	        self.s.bind(('',G.PORT_local))
                break
            except:
                print "supportServer: Error binding, retrying..."
        print G.name+" "+G.version_no+" running on port :",G.PORT_local
        self.s.connect((self.ip_addr, G.PORT_support_server))


        

    def getAddress(self):  #Returns net_addr of self
        while True:
            self.sendTextPacket(getaddrm)
            addr = self.recieveTextPacket()
            if addr != None:
                return addr


            
    def getFirstPeer(self):
        self.sendTextPacket(getpeerm)
        addr = self.recieveTextPacket()
        if addr != None:
            return addr
        else:
            return endm
            

        
        
    def getcon(self, net_addr):
        msg = getconm + separator + net_addr
        self.sendTextPacket(msg)
        print "getcon: sent ", net_addr
        try:
            msg = self.recieveTextPacket(G.packet_maxsize)
        except:
            pass


        
    def poll(self):
        self.sendTextPacket(pollm)
        try:
            msg = self.receiveTextPacket(G.packet_maxsize)
        except:
            return None
        if msg == endm:
            return None
        duties = msg.split(separator)
 
        if duties[-1] == endm:
            del duties[-1]
        return duties




    
    def sendTextPacket(self, packet):
        try:
	    self.s.send(packet)
            return True
	except:
	    return False

    def recieveTextPacket(self):
        try:
	     packet = self.s.recv(G.packet_maxsize)
	     return packet
	except socket.error:
            return None


    
    
        
        
        
