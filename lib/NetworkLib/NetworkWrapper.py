##Wrapper class for Network operations.
##Manages all high level applications of the network, works based on classes and functions defined in the network_support library and p2p library

#Control strings
import p2p
import Resources._globals as G



class NetworkHandler:
    def __init__(self):
        self.peer_list = [] ##peer_list is a dictionary that contains net_addr and control flags of peers
        self.network = p2p.P2PNetwork()
        self.supportServer = p2p.SupportServer()

    def getFirstPeer(self):
        ##Returns the net_addr of first peer returned by support server
        f = 0
        t = 5
        while f == 0 and t > 0:
            self.supportServer.sendUDP(G.C_401)
            addr = self.supportServer.recieveUDP()
            if addr[:7] == G.C_102:
                self.supportServer.sendUDP(G.C_102)
                addr = addr[8:]
                
                peer = p2p.Peer(addr, 0)

                while i < 5:
                    if self.connect2peer(peer):
                        self.peer_list.append((peer, 0))
                        self.network.addNode(peer)
                        f = 1
                        break
                    i = i-1
            t = t - 1
        if f == 0:
            print "No peer found"
            return False
        else:
            return True
            
            
            
    def connect2peer(self, peer):
        ##Hole punches a connection to a peer, returns true or false
        f = 0
        t = 5
        self.supportServer.sendUDP(G.C_201)
        
        return

    def getPeerList(self, peer):
        ##Returns a peer_list from selected peer.
        peer.sendTextPacket(C_501)
        if peer.recieveTextPacket() == G.C_502:
            peer.sendTextPacket(G.C_102)
            peer_list = peer.recieveTextPacket()
            peer.sendTextPacket(G.C_102)
            return peer_list
        else:
            return False

    def getAddrBook(self, peer):
        ##Returns AddrBook of selected peer
        return
    def pushAddrBook(self):
        ##Broadcasts updates to AddrBook
        return
    def callPeer(self,net_addr):
        ##Used to call a peer.
        return
    def sendAV(self, AV_encode_string):
        ##Called by AV Handler to send AV
        return
    
    
