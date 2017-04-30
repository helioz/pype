##Wrapper class for Network operations.
##Manages all high level applications of the network, works based on classes and functions defined in the network_support library and p2p library

import p2p
import Resources._globals as G
import pickle



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
        if self.supportServer.holePunchPeer(peer):
             self.peer_list.append((peer, 0))
             self.network.addNode(peer)
        
        ##Hole punches a connection to a peer, returns true or false

        
    def getPeerList(self, peer):
        ##Returns a peer_list from selected peer.
        peer.sendTextPacket(G.C_501)
        f = 0
        t = 5
        while f == 0 and t > 0:
            if peer.recieveTextPacket() == G.C_502:
                peer.sendTextPacket(G.C_102)
                peer_list = pickle.loads(peer.recieveTextPacket())
                peer.sendTextPacket(G.C_102)
                f = 1
                return peer_list
            t = t -1 
        return False

    def getAddrBook(self, peer):
        ##Returns AddrBook of selected peer
        peer.sendTextPacket(G.C_601)
        f = 0
        t = 5
        while f == 0 and t > 0:
            if peer.recieveTextPacket() == G.C_602:
                peer.sendTextPacket(G.C_102)
                addr_book = pickle.loads(peer.recieveTextPacket())
                peer.sendTextPacket(G.C_102)
                f = 1
                return peer_list
            t = t -1 
        return

    def pushAddrBookDelta(self, AddrBookDelta):
        ##Broadcasts updates to AddrBook
        self.network.pushBroadcast(pickle.dumps(AddrBookDelta), G.C_701, G.C_702)
        return
    
    def callPeer(self, net_addr, pub_key_hash_self, pu_key_hash_other):
        ##Used to call a peer.
        for p in self.network.nodeList:
            if p.session_endpoints == net_addr:
                p.sendTextPacket(G.C_801)
                if p.recieveTextPacket() == G.C_802:
                    p.sendTextPacket(G.C_803+pub_key_hash_self)
                    if p.recieveTextPacket() == G.C_803+pub_key_hash_other:
                        p.sendTextPacket(G.C_102)
                        while p.recieveTextPacket() != G.C_805:
                            pass
                        return peer
                    else:
                        print "Reciever unidentified"
                else:
                    print "Call rejected"

        print "Address not a peer"
        self.
        return
    def sendAV(self, AV_encode_string, peer):
        ##Called by AV Handler to send AV
        return
    
    
