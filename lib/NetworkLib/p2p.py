##Peer2peer library for establishing peer connection and send and recieve data
import Resources._globals as GLOBALS
import socket

class Peer:
    def __init__(self, net_addr, sym_key):
        self.session_endpoints = net_addr
        ## net_addr contains session endpoints and any other details to establish connection
        self.tcpStream = 0 #Stream object
        self.symKey = sym_key

    def makeConnection(self):
        ##Hole punches a connection to peer and returns true
        return

    def sendMediaPacket(self, data_bStream):
        ## Function to send UDP packet to peer
        return

    def recieveMediaPacket(self):
        ## Function to recieve UDP packets
        return data_bStream

    def sendTextPacket(self, data_bStream):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(data_bStream, self.net_addr)
        return
    
    def recieveTextPacket(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(("",GLOBALS.PORT_Node))
        data_bStream, addr = sock.recvfrom(GLOBALS.PORT_Node)
                  
        return data_bStream
    
    def createTCPStream(self):
        ##Creates a TCP Stream to self node
        return
    def sendTCP(self, data_bStream):
        ##Sends data_bStream to node via tcpStream
        return
    def recieveTCP(self):
        ##Recieves TCP packets from tcpStream
        return data_bStream
    def destroyTCP(self):
        ##Closes TCP stream
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
        self.ip_addr = GLOBALS.IPADDR_support_server
        #self.port_holePunch = GLOBALS.PORT_Node
        #self.port_getPeer = GLOBALS.PORT_support_server_get_peer

    def sendUDP(self, packet):
        ##Send UDP packet to server
        return
    def recieveUDP(self):
        return packet
        ##Recieve UDP packet from server
        return
    
    
        
        
        
