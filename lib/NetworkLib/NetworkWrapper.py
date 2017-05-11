##Wrapper class for Network operations.
##Manages all high level applications of the network, works based on classes and functions defined in the network_support library and p2p library

import p2p
import Resources._globals as G
import pickle
import time
from lib.AVLib.AVWrapper import AVHandler



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
        #self.numPeers = 0


        
    # def getFirstPeer(self):
    #     ##Returns the net_addr of first peer returned by support server
    #     # f = 0
    #     # t = G.nOfIteration
    #     # while f == 0 and t > 0:
    #     #     self.supportServer.sendTextPacket(G.C_401)
    #     #     addr = self.supportServer.recieveTextPacket()
    #     #     if addr == None:
    #     #         t = t - 1
    #     #         continue
    #     #     elif addr[:7] == G.C_102:
    #     #         self.supportServer.sendTextPacket(G.C_102)
    #     #         addr = addr[8:]
    #     #while True:
    #     addr = self.supportServer.getFirstPeer()
    #     if addr == 'end':
    #         time.sleep(G.waiting_time)
    #         return False
    #     if addr == G.NET_ADDR_self:
    #         time.sleep(G.waiting_time)
    #         return False
            
    #     peer = p2p.Peer(addr, self.supportServer)
    #     #print "First peer object made"
    #     #self.supportServer.getcon(peer.net_addr)
    #     if self.connect2peer(peer):
    #         #print "Connected to peer"
    #         return True

            
            
            
    def connect2peer(self, peer_addr):
        for p in self.peer_list:
            if p[0].net_addr == peer_addr:
                print "connect2peer: peer exists"
                return False  ##If changed to True, fix peerListener and peer connecter threads
        self.supportServer.getcon(peer_addr)
        peer = p2p.Peer(peer_addr, self.supportServer)
        if peer.makeConnection():
            self.peer_list.append((peer, 0))
            self.network.addNode(peer)
            print "connect2peer: Connected to", peer
            return True, peer
        return False

        
    def getPeerList(self, peer):
        ##Returns a peer_list from selected peer.
        t = G.nOfIteration
        while t > 0:
            peer.sendTextPacket(G.C_501)
            print "getPeerList: Sent 501"
            #time.slpee(0.2)
            if peer.recieveTextPacket() == G.C_502:
                print "getPeerList: Recieved 502"
                pickledPeerList = peer.recieveTextPacket()
                if pickledPeerList == None:
                    continue
                if pickledPeerList[0] == 'P':
                    pickledPeerList = pickledPeerList[1:]
                    #print pickledPeerList
                    peer_list_u = pickle.loads(pickledPeerList)
                    #peerList = []
                    #for peerAddr in peer_list_u:
                    #    peerList.append( ( p2p.Peer(peerAddr, self.supportServer), 0 ) )
                    #print "getPeerList: Obtained peer_list :", peerList
                    #peer_list = []
                    #for adr in peer_list_u:
                    #    newPeer = (p2p.Peer(adr,self.supportServer), 0)
                    #    if newPeer not in peer_list:
                    #        peer_list.append( newPeer )
                    #print "getPeerList: Peer list obtained"
                    #peer.sendTextPacket(G.C_102)
                    #print "getPeerList: sent 102"
                    #f = 1
                    #print "getPeerList : peer list ", peer_list
                    return peer_list_u
            t = t -1 
        return None

    def getAddrBook(self, peer):
        ##Adds AddrBook of selected peer as current AddrBook
        
        #f = 0
        t = 5
        while  t > 0:
            peer.sendTextPacket(G.C_601)
            if peer.recieveTextPacket() == G.C_602:
                #peer.sendTextPacket(G.C_102)
                print "getAddrBook : Recieved 602"
                pickledAddrBook = peer.recieveTextPacket()
                if pickledAddrBook == None:
                    continue
                if pickledAddrBook[0] == 'A':
                    pickledAddrBook = pickledAddrBook[1:]
                    if pickledAddrBook == None:
                        continue
                    peer.sendTextPacket(G.C_102)
                    #addr_book 
                    #f = 1
                    self.AddrBook = pickle.loads(pickledAddrBook)
                    return True
            time.sleep(2)
        return False

    def pushAddrBookDelta(self, AddrBookDelta):
        ##Broadcasts updates to AddrBook
        self.network.pushBroadcast('D'+pickle.dumps(AddrBookDelta), G.C_701, G.C_702)
        return
    
    def callPeer(self, contact):
        #Used to call a peer.
        #Obtain peer address
        pub_key_hash_other = self.crypto.pubKeyHash(contact.keyN, contact.keyE)
        pub_key_hash_self = self.crypto.pubKeyHashSelf()
        print "Callee address ", pub_key_hash_other
        p = None
        sign = None
        for ad in self.AddrBook:
            if ad[0] == pub_key_hash_other:
                print "callPeer: Address found in AddrBook"
                sign = self.crypto.decryptSignature(ad[1],self.crypto.toPubKey(contact.keyE, contact.keyN)) # sign is decrypted signature
                p = self.network.getPeerByAddr(sign.net_addr)
        if p != None:
            print p
            p.sendTextPacket(G.C_801)
            #if p.recieveTextPacket() == G.C_802:
                #p.sendTextPacket('K'+pub_key_hash_self)
                #if p.recieveTextPacket() == G.C_803+"-"+pub_key_hash_other:
                #p.sendTextPacket(G.C_102)
                #p.recieveTextPacket()
            AVHandler(p).callAV()
            
        #     else:
        #         print "callPeer: Call rejected"
        elif sign != None:
            print "callPeer: Address not a peer. Trying to establish connection"
            #peer = p2p.Peer(sign.net_addr,0)
            self.supportServer.getcon(sign.net_addr)
            ret, peer = self.connect2peer(sign.net_addr)
            if ret:
            #if peer.makeConnection():
                return self.callPeer(contact)
        else:
            print "Peer does not exist"
            return None

    def addToAddrBook(self, AddrBookDelta):
        f = 0
        h = self.crypto.sha256(pickle.dumps(AddrBookDelta))
        print "addToAddrBook: hash", h
        for t in self.AddrDeltaDict:
            if t == h:
                print "addToAddrBook : hash exists"
                return True
            
        self.AddrDeltaDict.append(h)    
        self.AddrBook = self.AddrBook+AddrBookDelta
        self.pushAddrBookDelta(AddrBookDelta)
        print "addToAddrBook: updated AddrBook", self.AddrBook
        return True

            
    def PeerListenerThread(self, peer, callInterrupt):
        #if not peer.makeConnection():
        #    return
        try:
            while True:
                #peer.makeConnection()
                packet = peer.recieveTextPacket()
                #print "Recieved",packet
                if packet == G.C_501:
                    print "PeerListener: Recieved 501"
                    peer.sendTextPacket(G.C_502)
                    print "PeerListener: Peer list to send", self.peer_list
                    pl = []
                    for it in self.peer_list:
                       pl.append(it[0].net_addr)
                    print "PeerListener: Peer list to send", pl
                    peer.sendTextPacket('P'+pickle.dumps(pl))

                elif packet == G.C_701:
                    peer.sendTextPacket(G.C_702)
                    AddrBookDelta_u = peer.recieveTextPacket()
                    if AddrBookDelta_u == None:
                        continue
                    if AddrBookDelta_u[0] == 'D':
                        AddrBookDelta_u = AddrBookDelta_u[1:]
                        AddrBookDelta = pickle.loads(AddrBookDelta_u)
                        print "Peer listener: AddrBookDelta recieved:", AddrBookDelta
                        self.addToAddrBook(AddrBookDelta)
                        print "PeerListener: Address Book delta updated"
                    
                elif packet == G.C_601:
                    peer.sendTextPacket(G.C_602)
                    #if peer.recieveTextPacket() == G.C_102:
                    
                    peer.sendTextPacket('A'+pickle.dumps(self.AddrBook))
                    if peer.recieveTextPacket() != G.C_102:
                        peer.sendTextPacket('A'+pickle.dumps(self.AddrBook))
                        peer.recieveTextPacket()
                    print "peerListener: sent AddrBook"
                elif packet == G.C_801:
                    print "Got call"
                    #callInterrupt(1,0)
                    AVHandler(peer).callAV()
                    # #Incoming call
                    # f = 0
                    # print "PeerListener: Incoming call, recieved 801"
                    # peer.sendTextPacket(G.C_802)
                    # print "PeerListener: sent 802"
                    # addr = peer.recieveTextPacket()
                    # if addr == None:
                    #     addr = peer.recieveTextPacket()
                    #     if addr == None:
                    #         continue
                    # if addr[0] == 'K':
                    #     addr = addr[1:]
                    #     print "PeerListener: Recieved 803"
                    #     for contact in callInterrupt(2,0):
                    #         if contact.h == pub_key_hash_other:
                    #             print "PeerListener: Caller identified"
                                
                    #             #peer.sendTextPacket(G.C_803+"-"+crypto.pubKeyHashSelf())
                    #             #print "PeerListener: Address verification sent 803"
                    #             #peer.recieveTextPacket()
                    #             #print "PeerListener: Recieved 102"
                    #             #peer.sendTextPacket(G.C_805)
                    #             #print "PeerListener: sent 805"
                    #             callInterrupt(1,peer)
                    #             #Call incoming call interrupt with contact, and peer
                    #             f = 1
                    #     if f == 0:
                    #         print "PeerListener: Caller not identified"

            
                            
        except KeyboardInterrupt:
            print "Keyboard interrupted"
            return



    
    
