##Wrapper class for Network operations.
##Manages all high level applications of the network, works based on classes and functions defined in the network_support library and p2p library

import p2p
import Resources._globals as G
import pickle



class NetworkHandler:
    def __init__(self, crypto):
        self.peer_list = [] ##peer_list is a dictionary that contains net_addr and control flags of peers
        self.network = p2p.P2PNetwork()
        self.supportServer = p2p.SupportServer()
        self.AddrBook = [("hash_address","encrypted_signature")]
        self.crypto = crypto

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

                if self.connect2peer(peer):
                    f = 1
                    break
                    
            t = t - 1
        if f == 0:
            print "No peers found"
            return False
        else:
            return True
            
            
            
    def connect2peer(self, peer):
        t = 5
        f = 0
        while (not f) and t>0:
            if peer.makeConnection():
                f = 1
                break
            t = t - 1
        if f == 1:
            self.peer_list.append((peer, 0))
            self.network.addNode(peer)
            return True
        else:
            print "Failed to connec to node"
            return False
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
        ##Adds AddrBook of selected peer as current AddrBook
        peer.sendTextPacket(G.C_601)
        f = 0
        t = 5
        while f == 0 and t > 0:
            if peer.recieveTextPacket() == G.C_602:
                peer.sendTextPacket(G.C_102)
                addr_book = pickle.loads(peer.recieveTextPacket())
                peer.sendTextPacket(G.C_102)
                f = 1
                self.AddrBook = addr_book
                return
            t = t -1 
        return

    def pushAddrBookDelta(self, AddrBookDelta):
        ##Broadcasts updates to AddrBook
        self.network.pushBroadcast(pickle.dumps(AddrBookDelta), G.C_701, G.C_702)
        return
    
    def callPeer(self, contact):
        ##Used to call a peer.
        ##Obtain peer address
        pub_key_hash_other = crypto.sha256(str(contact.keyN) + str(contact.keyE))
        for ad in self.AddrBook:
            if ad[0] == pub_key_hash_other:
                sign = crypto.decryptSignature(ad[1],toPubKey(contact.keyE, contact.keyN)) # sign is decrypted signature 
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

        print "Address not a peer. Trying to establish connection"
        peer = p2p.Peer(net_addr,0)
        
        if self.connect2peer(peer):
            return self.callPeer(net_addr, pub_key_hash_self,pub_key_hash_other)
        else:
            print "Peer does not exist"
            return

    def ThreadListener(self, peer):
        while True:
            packet = peer.recieveTextPacket()
            if packet == G.C_501:
                peer.sendTextPacket(G.C_102)
                peer.sendTextPacket(pickle.dumps(self.peer_list))
                while peer.recieveTextPacket() != G.C_102:
                    peer.sendTextPacket(pickle.dumps(self.peer_list))
            elif packet == G.C_601:
                peer.sendTextPacket(G.C_602)
                
                
                    

    
    
