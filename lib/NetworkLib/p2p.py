##Peer2peer library for establishing peer connection and send and recieve data
import Resources._globals as GLOBALS

class Peer:
    def __init__(self, net_addr, sym_key):
        self.session_endpoints = net_addr
        ## net_addr contains session endpoints and any other details to establish connection
        self.tcpStream = 0 #Stream object
        self.symKey = sym_key 

    def sendUDP(self, data_bStream):
        ## Function to send UDP packet to peer
        return

    def recieveUDP(self):
        ## Function to recieve UDP packets
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

    def pushBroadcast(self, data_bStream, ctrlString):
        for p in self.nodeList:
            p.createTCPStream()
            p.sendTCP(ctrlString)
            p.sendTCP(data_bStream)
            p.destroyTCP()

class SupportServer:
    def __init__(self, ):
        self.ip_addr = GLOBALS.IPADDR_support_server
        self.port_holePunch = GLOBALS.PORT_Node
        self.port_getPeer = GLOBALS.PORT_support_server_get_peer

    def sendUDP(self, packet):
        ##Send UDP packet to server
        return
    def recieveUDP(self, packet):
        ##Recieve UDP packet from server
        return
    
    
        
        
        
