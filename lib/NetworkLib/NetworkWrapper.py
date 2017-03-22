##Wrapper class for Network operations.

class NetworkHandler:
    def __init__(self):
        self.peer_list = [] ##peer_list is a dictionary that contains net_addr and control flags of peers
        

    def getFirstPeer(self):
        ##Returns the net_addr of first peer returned by support server

    def connect2peer(self, net_addr):
        ##Hole punches a connection to a peer, returns true or false


    def getPeerList(self, net_addr):
        ##Returns a peer_list from selected peer.
        

    def getAddrBook(self, net_addr):
        ##Returns AddrBook of selected peer

    def pushAddrBook(self):
        ##Broadcasts updates to AddrBook
        
    def callPeer(self,net_addr):
        ##Used to call a peer.

    def sendAV(self, AV_encode_string):
        ##Called by AV Handler to send AV
    
    
