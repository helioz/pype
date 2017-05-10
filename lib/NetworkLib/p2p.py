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
    def __init__(self, net_addr, supportServer):
        self.net_addr = net_addr
        ## net_addr contains session endpoints and any other details to establish connection
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
            
	self.isPunched = False
        self.supportServer = supportServer

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.net_addr == other.net_addr
        else:
            return False

    def __str__(self):
        return "Peer : "+self.net_addr
    
    def __repr__(self):
        return "Peer Obj: "+self.net_addr
        
    def makeConnection(self):
        ##Attempts to hole punch a connection to peer and returns true, assumes that getcon is called.
        #self.supportServer.getcon(self.net_addr)
        for i in range(G.nOfIteration) :
            #print "makeConn(): Running make connection on ", self.net_addr
	    if self.sendTextPacket('punch'):
                print "makeConn: sent punch", self.net_addr
	        self.s.settimeout(G.punchTimeout)
	        #data = ''
	        try :

		    data = self.s.recv(G.packet_maxsize)                    
	        except :
                    time.sleep(1)
		    continue
	        if data == 'punch' :
		    #print 'received punch\n'
		    self.sendTextPacket('punched')
		    self.isPunched = True
		    #self.s.settimeout(None)
		    return True
	        if data == 'punched' :
		    #print 'received punched\n'
		    self.isPunched = True
		    #self.s.settimeout(None)		
		    return True
	    #self.s.settimeout(None)
	return False
    

    def sendMediaPacket(self, data_bStream):
        try:
	    self.s.send(data_bStream)
        except:
            pass
            ## Function to send UDP packet to peer

    def recieveMediaPacket(self):
        self.s.settimeout(G.mediaTimeOut)
        try:
	    data_bStream = self.s.recv(G.mediaPacket_maxsize)
            return data_bStream
        except:
            pass

    def sendTextPacket(self, data_bStream):
        
        try:
	    self.s.send(data_bStream)
            #print "sendTexPack sent ", data_bStream, "to", self.net_addr
            return True
	except socket.error, msg:
            print "sendTextPacket failed at peer"
	    print 'Error Code : ' + str(msg[0]) + ' Message ' + msg[1]       
            return False
    
    def recieveTextPacket(self):
        self.s.settimeout(G.punchTimeout)
	try:
	    data_bStream = self.s.recv(G.packet_maxsize)
	    if data_bStream != 'punched' and data_bStream != 'punch' and data_bStream != None :
                #self.s.settimeout(None)
		return data_bStream
	    elif data_bStream == 'punch' :
		self.send('punched')
		return self.recieveTextPacket()
	    else :
		return self.recieveTextPacket()
	except:
	    #print 'recieveTextPacket No packet recieved from peer'
	    return
                  
    
class P2PNetwork:
    def __init__(self):
        self.nodeList = []

    def addNode(self, peer):
        self.nodeList.append(peer)
        
    def getPeerByAddr(self, net_addr):
        for p in self.nodeList:
            if p.net_addr == net_addr:
                return p
        print "getPeerByAddr: No peer with corresponding address"
        return None

    def pushBroadcast(self, data_bStream, ctrlString1, ctrlString2):
        for p in self.nodeList:
            p.sendTextPacket(ctrlString1)
            print "pushBroadcast sent ",ctrlString1
            if p.recieveTextPacket() == ctrlString2:
                print "pushBroadcast received ", ctrlString2
                p.sendTextPacket(data_bStream)
                print "pushBroadcast: Successfully sent to ", p.net_addr




class SupportServer:
    def __init__(self, ):
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
        #while True:
        self.sendTextPacket(getpeerm)
        addr = self.recieveTextPacket()
        if addr != None:
            return addr
        else:
            return endm
            
    
    def getcon(self, addr):
        msg = getconm + separator + addr
        self.s.send(msg)
        print "getcon(): sent ", msg
        try:
            msg = self.s.recv(G.packet_maxsize)
        except:
            pass
        #if msg != endm :
        #    self.getcon(addr)

    def poll(self):
        #print "Called poll"
        self.s.send(pollm)
        #print "poll sent", pollm
        msg = self.s.recv(G.packet_maxsize)
        #print msg
        if msg == endm:
            return None
        duties = msg.split(separator)
 
        if duties[-1] == endm:
            del duties[-1]
        #print duties
        return duties
        
    def sendTextPacket(self, packet):
        ##Send UDP packet to server
        try:
	    self.s.send(packet)
            return True
	except socket.error, msg:
	    print 'Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
            print "sendTextPacket : error at supportServer"
	    return False

    def recieveTextPacket(self):
        ##Recieve UDP packet from server
        try:
	     packet = self.s.recv(G.packet_maxsize)
	     return packet
	except socket.error:
	    #print 'recieveTextPacket: Packet recieve error at supportServer'
            return None


    
    
        
        
        
