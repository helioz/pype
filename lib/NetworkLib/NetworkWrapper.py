##Wrapper class for Network operations.
##Manages all high level applications of the network, works based on classes and functions defined in the network_support library and p2p library

import p2p
import Resources._globals as G
import pickle
import time



class NetworkHandler:
    def __init__(self, crypto):
        self.peer_list = [] ##peer_list is a list that contains net_addr and control flags of peers
        self.network = p2p.P2PNetwork()
        self.supportServer = p2p.SupportServer()
        self.peerListenerThreads = []
        self.AddrBook = [("hash_address","encrypted_signature")]
        self.crypto = crypto
        self.AddrDeltaDict = ["hash"]
        G.NET_ADDR_self = self.supportServer.getAddress()
        print "pype running at IP: ",G.NET_ADDR_self
        self.numPeers = 0


        
    def getFirstPeer(self):
        ##Returns the net_addr of first peer returned by support server
        # f = 0
        # t = G.nOfIteration
        # while f == 0 and t > 0:
        #     self.supportServer.sendTextPacket(G.C_401)
        #     addr = self.supportServer.recieveTextPacket()
        #     if addr == None:
        #         t = t - 1
        #         continue
        #     elif addr[:7] == G.C_102:
        #         self.supportServer.sendTextPacket(G.C_102)
        #         addr = addr[8:]
        #while True:
        addr = self.supportServer.getFirstPeer()
        if addr == 'end':
            time.sleep(G.waiting_time)
            return False
        if addr == G.NET_ADDR_self:
            time.sleep(G.waiting_time)
            return False
            
        peer = p2p.Peer(addr, self.supportServer)
        #print "First peer object made"
        #self.supportServer.getcon(peer.net_addr)
        if self.connect2peer(peer):
            #print "Connected to peer"
            return True

            
            
            
    def connect2peer(self, peer):
        t = G.nOfIteration
        f = 0
        if (peer, 0) in self.peer_list:
            return True
        #while (not f) and t>0:
            #self.supportServer.getcon(peer.net_addr)
            # if peer.makeConnection():
        #         f = 1
        #         break
        #     t = t - 1
        # if f == 1:
        self.peer_list.append((peer, 0))
        self.network.addNode(peer)
        return True
        # else:
        #     print "Failed to connect to node"
        #     return False
        ##Hole punches a connection to a peer, returns true or false

        
    def getPeerList(self, peer):
        ##Returns a peer_list from selected peer.
        peer.sendTextPacket(G.C_501)
        print "getPeerList: Sent 501"
        f = 0
        t = G.nOfIteration
        while f == 0 and t > 0:
            #time.slpee(0.2)
            if peer.recieveTextPacket() == G.C_502:
                print "getPeerList: Recieved 502"
                #peer.sendTextPacket(G.C_102)
                #print "sent 102"
                pickledPeerList = peer.recieveTextPacket()
                if pickledPeerList != None:
                    peer_list = pickle.loads(pickledPeerList)
                    print "getPeerList: Peer list obtained"
                    peer.sendTextPacket(G.C_102)
                    print "getPeerList: sent 102"
                    f = 1
                    print "getPeerList : peer list ", peer_list
                    return peer_list
            t = t -1 
        return None

    def getAddrBook(self, peer):
        ##Adds AddrBook of selected peer as current AddrBook
        peer.sendTextPacket(G.C_601)
        f = 0
        t = 5
        while f == 0 and t > 0:
            if peer.recieveTextPacket() == G.C_602:
                peer.sendTextPacket(G.C_102)
                pickledAddrBook = peer.recieveTextPacket()
                if pickledAddrBook == None:
                    continue
                addr_book = pickle.loads(pickledAddrBook)
                peer.sendTextPacket(G.C_102)
                f = 1
                self.AddrBook = addr_book
                return None
            t = t -1 
        return

    def pushAddrBookDelta(self, AddrBookDelta):
        ##Broadcasts updates to AddrBook
        self.network.pushBroadcast(pickle.dumps(AddrBookDelta), G.C_701, G.C_702)
        return
    
    def callPeer(self, contact):
        ##Used to call a peer.
        ##Obtain peer address
        pub_key_hash_other = crypto.pubKeyHash(contact.keyN, contact.keyE)
        for ad in self.AddrBook:
            if ad[0] == pub_key_hash_other:
                sign = crypto.decryptSignature(ad[1],toPubKey(contact.keyE, contact.keyN)) # sign is decrypted signature
        p = self.network.getPeerByAddr(sign.net_addr)
        if p != None:
            p.sendTextPacket(G.C_801)
            if p.recieveTextPacket() == G.C_802:
                p.sendTextPacket(G.C_803+"-"+pub_key_hash_self)
                if p.recieveTextPacket() == G.C_803+"-"+pub_key_hash_other:
                    p.sendTextPacket(G.C_102)
                    while p.recieveTextPacket() != G.C_805:
                        pass
                    return peer
                else:
                    print "callPeer: Reciever unidentified"
            else:
                print "callPeer: Call rejected"
                    
        print "callPeer: Address not a peer. Trying to establish connection"
        peer = p2p.Peer(net_addr,0)
        
        if self.connect2peer(peer):
            return self.callPeer(net_addr, pub_key_hash_self,pub_key_hash_other)
        else:
            print "Peer does not exist"
            return None

    def addToAddrBook(self, AddrBookDelta):
        f = 0
        h = self.crypto.sha256(pickle.dumps(AddrBookDelta))
        for t in self.AddrDeltaDict:
            if t[0] == h:
                f = 1
        if f == 0:
            self.AddrBook = self.AddrBook+AddrBookDelta
            self.AddrDeltaDict.append(h)
            self.pushAddrBookDelta(AddrBookDelta)


            
    def PeerListenerThread(self, peer, callInterrupt):
        if not peer.makeConnection():
            return
        try:
            while True:
                #peer.makeConnection()
                packet = peer.recieveTextPacket()
                #print "Recieved",packet
                if packet == G.C_501:
                    print "PeerListener: Recieved 501"
                    peer.sendTextPacket(G.C_502)
                    print self.peer_list
                    peer.sendTextPacket(pickle.dumps(self.peer_list))
                    while peer.recieveTextPacket() != G.C_102:
                        peer.sendTextPacket(pickle.dumps(self.peer_list))
                elif packet == G.C_701:
                    peer.sendTextPacket(G.C_702)
                    AddrBookDelta = pickle.loads(peer.recieveTextPacket())
                    addToAddrBook(AddrBookDelta)
                    print "PeerListener: Address Book delta updated"
                    
                elif packet == G.C_601:
                    peer.sendTextPacket(G.C_602)
                    if peer.recieveTextPacket() == G.C_102:
                        peer.sendTextPacket(pickle.dumps(self.addr_book))
                    if peer.recieveTextPacket() != G.C_102:
                        peer.sendTextPacket(pickle.dumps(self.addr_book))

                elif packet == G.C_801:
                    #Incoming call
                    f = 0
                    print "PeerListener: Incoming call, recieved 801"
                    peer.sendTextPacket(G.C_802)
                    print "PeerListener: sent 802"
                    addr = peer.recieveTextPacket()
                    ad1, pub_key_hash_other = addr.split("-")
                    if ad1 == G.C_803:
                        print "PeerListener: Recieved 803"
                        for contact in contacts:
                            if contact.h == pub_key_hash_other:
                                print "PeerListener: Caller identified"
                                peer.sendTextPacket(G.C_803+"-"+crypto.pubKeyHashSelf())
                                print "PeerListener: Address verification sent 803"
                                peer.recieveTextPacket()
                                print "PeerListener: Recieved 102"
                                peer.sendTextPacket(G.C_805)
                                print "PeerListener: sent 805"
                                callInterrupt(1,peer)
                                #Call incoming call interrupt with contact, and peer
                                f = 1
                        if f == 0:
                            print "PeerListener: Caller not identified"

            
                            
        except KeyboardInterrupt:
            print "Keyboard interrupted"
            return



    
    
