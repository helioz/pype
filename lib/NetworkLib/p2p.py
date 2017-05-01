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
	self.s.bind(('',G.PORT_local))
	
	self.s.connect(netAlgo.stringToTuple(self.net_addr))
	self.isPunched = False
	self.s.settimeout(None)
        self.supportServer = supportServer

    def makeConnection(self):
        ##Hole punches a connection to peer and returns true
        for i in range(G.nOfIteration) :
	    self.sendTextPacket('punch')
	    self.s.settimeout(G.punchTimeout)
	    data = ''
	    try :
		data = self.s.recieveTextPacket(G.packet_maxsize)
	    except :
                time.sleep(G.waiting_time)
		continue
	    if data == 'punch' :
		print 'received punch\n'
		self.sendTextPacket('punched')
		self.isPunched = True
		self.s.settimeout(None)
		return True
	    if data == 'punched' :
		print 'received punched\n'
		self.isPunched = True
		self.s.settimeout(None)		
		return True
	self.s.settimeout(None)
	return False

    def sendMediaPacket(self, data_bStream):
        ## Function to send UDP packet to peer
        return

    def recieveMediaPacket(self):
        ## Function to recieve UDP packets
        return data_bStream

    def sendTextPacket(self, data_bStream):
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
	    if data_bStream != 'punched' and msg != 'punch' and msg != None :
                self.s.settimeout(None)
		return data_bStream
	    elif msg == 'punch' :
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

    def pushBroadcast(self, data_bStream, ctrlString1, ctrlString2):
        for p in self.nodeList:
            p.createTCPStream()
            p.sendTCP(ctrlString)
            if p.recieveTCP() == ctrlString2:
                p.sendTCP(data_bStream)
                print "Successfully sent to ", p.session_endpoints
            p.destroyTCP()

class SupportServer:
    def __init__(self, ):
        self.ip_addr = G.IPADDR_support_server
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	self.s.bind(('',G.PORT_local))
	self.s.connect((self.ip_addr, G.PORT_support_server))


    def sendTextPacket(self, packet):
        ##Send UDP packet to server
        try:
	    self.s.send(packet)
	except socket.error, msg:
	    print 'Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
	    return None

    def recieveTextPacket(self):
        ##Recieve UDP packet from server
        try:
	     packet = self.s.recv(G.packet_maxsize)
	     return packet
	except socket.error, msg:
	    print 'Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
            return None


    
    
        
        
        
