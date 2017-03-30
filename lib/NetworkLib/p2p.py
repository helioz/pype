##Peer2peer library for establishing peer connection and send and recieve data


class Peer:
    def __init__(self, net_addr):
        self.session_endpoints = net_addr
        ## net_addr contains session endpoints and any other details to establish connection
        self.tcpStream = 0 #Stream object

    def sendUDP(self, data_bStream):
        ## Function to send UDP packet to peer

    def recieveUDP(self):
        ## Function to recieve UDP packets
        return data_bStream

    def createTCPStream(self):
        ##Creates a TCP Stream to self node

    def sendTCP(self, data_bStream):
        ##Sends data_bStream to node via tcpStream
    def recieveTCP(self):
        ##Recieves TCP packets from tcpStream
        return data_bStream
    def destroyTCP(self):
        ##Closes TCP stream
    
    
class p2p:
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
        
        
