##Peer2peer library for establishing peer connection and send and recieve data
import Resources._globals as G
import socket
import sys
import time
import lib.NetworkLib.network_support as netAlgo

initm = 'init'
pollm = 'poll'
getconm = 'getcon'
endm = 'e'

separator = '_'

class Peer:
    def __init__(self, net_addr, supportServer):
        self.net_addr = net_addr
        ## net_addr contains session endpoints and any other details to establish connection
        #self.tcpStream = 0 #Stream object
        #self.symKey = sym_key
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

	for p in range(G.nOfIteration):
            try:
	        self.s.bind(('',G.PORT_local))
                break
            except:
                print "Failed to bind port, retrying"

	self.s.connect(netAlgo.stringToTuple(self.net_addr))
	self.isPunched = False
	self.s.settimeout(None)
        self.supportServer = supportServer

    def makeConnection(self):
        ##Hole punches a connection to peer and returns true
        for i in range(G.nOfIteration) :
	    if self.sendTextPacket('punch'):
	        self.s.settimeout(G.punchTimeout)
	        #data = ''
	        try :
		    data = self.s.recv(G.packet_maxsize)                    
	        except :
                    time.sleep(3)
		    continue
	        if data == 'punch' :
		    print 'received punch\n'
		    self.sendTextPacket('punched')
		    self.isPunched = True
		    #self.s.settimeout(None)
		    return True
	        if data == 'punched' :
		    print 'received punched\n'
		    self.isPunched = True
		    #self.s.settimeout(None)		
		    return True
	    #self.s.settimeout(None)
	return False

    def sendMediaPacket(self, data_bStream):
        ## Function to send UDP packet to peer
        return

    def recieveMediaPacket(self):
        ## Function to recieve UDP packets
        return data_bStream

    def sendTextPacket(self, data_bStream):
        self.s.settimeout(None)
        try:
	    self.s.send(data_bStream)
            return True
	except socket.error, msg:
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
	    print 'Error: No packet recieved from peer'
	    return
                  
    
class P2PNetwork:
    def __init__(self):
        self.nodeList = []

    def addNode(self, peer):
        self.nodeList.append(peer)
        
    def getPeerByAddr(self, net_addr):
        for p in self.nodeList:
            if p.net_addr == net_addr:
                return peer
        print "No peer with corresponding address"
        return None

    def pushBroadcast(self, data_bStream, ctrlString1, ctrlString2):
        for p in self.nodeList:
            p.createTCPStream()
            p.sendTCP(ctrlString1)
            if p.recieveTCP() == ctrlString2:
                p.sendTCP(data_bStream)
                print "Successfully sent to ", p.session_endpoints
            p.destroyTCP()



class SupportServer:
    def __init__(self, ):
        self.ip_addr = G.IPADDR_support_server
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        for p in range(G.nOfIteration):
            try:
	        self.s.bind(('',G.PORT_local))
                break
            except:
                print "Error binding, retrying..."
                #G.PORT_local = G.PORT_local + 10
        print G.name+" "+G.version_no+" running on port :",G.PORT_local
        self.s.connect((self.ip_addr, G.PORT_support_server))


    def sendTextPacket(self, packet):
        ##Send UDP packet to server
        try:
	    self.s.send(packet)
            return True
	except socket.error, msg:
	    print 'Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
	    return False

    def recieveTextPacket(self):
        ##Recieve UDP packet from server
        try:
	     packet = self.s.recv(G.packet_maxsize)
	     return packet
	except socket.error, msg:
	    print 'Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
            return None


    
    
        
        
        
