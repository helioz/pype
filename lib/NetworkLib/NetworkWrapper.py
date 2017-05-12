##Wrapper class for Network operations.
##Manages all high level applications of the network, works based on classes and functions defined in the network_support library and p2p library

import p2p
import Resources._globals as G
import pickle
import time
from lib.AVLib.AVWrapper import AVHandler
import multiprocessing


class NetworkHandler:
    def __init__(self, crypto):
        self.peer_list = [] ##peer_list is a list that contains net_addr and control flags of peers
        self.supportServer = p2p.SupportServer()

        self.AddrBook = [("hash_address","encrypted_signature")]
        self.crypto = crypto
        self.AddrDeltaDict = ["hash"]
        G.NET_ADDR_self = self.supportServer.getAddress()
        print "pype running at IP: ",G.NET_ADDR_self


        self.callFlag = False
        self.incomingCallInterrupt = (False, False, 0)
        self.killFlag = False

        
    def answerIncomingCall(self):
        if self.incomingCallInterrupt[0] == True:
            peer = self.incomingCallInterrupt[2]
            if self.incomingCallInterrupt[1] == False:
                peer.sendTextPacket(G.call_reject)
                self.incomingCallInterrupt(False, False, 0)
                return
            peer.sendTextPacket(G.call_ready)
            self.callFlag = True
            self.incomingCallInterrupt = (False, False, 0)
            #makeCallFunc
            self.callFlag = False

            
    def connect2peer(self, peer_addr):
        for p in self.peer_list:
            if p[0].net_addr == peer_addr:
                print "connect2peer: Peer connection exists"
                return False, p  
        self.supportServer.getcon(peer_addr)
        peer = p2p.Peer(peer_addr)
        if peer.makeConnection():
            self.peer_list.append(peer)
            print "connect2peer: Connected to", peer
            return True, peer
        return False, None

        
    def getPeerList(self, peer):
        for t in range(G.nOfIteration):
            peer.sendTextPacket(G.peer_list_req)
            pickledPeerList = peer.recieveTextPacket()
            if pickledPeerList == None:
                continue
            if pickledPeerList[0] == 'P':
                pickledPeerList = pickledPeerList[1:]
                peer_list_u = pickle.loads(pickledPeerList)
                print "peer_list obtained", peer_list_u
                return peer_list_u
        return None

    

    def getAddrBook(self, peer):
        for t in range(G.nOfIteration):
            peer.sendTextPacket(G.req_AddrBook)
            pickledAddrBook = peer.recieveTextPacket()
            if pickledAddrBook == None:
                time.sleep(2)
                continue
            if pickledAddrBook[0] == 'A':
                pickledAddrBook = pickledAddrBook[1:]
                if pickledAddrBook == None:
                    time.sleep(2)
                    continue
                    
                self.AddrBook = pickle.loads(pickledAddrBook)
                print "AddrBook obtained"
                return True
            
        return False

    
    def pushAddrBookDelta(self, AddrBookDelta):
        for peer in self.peer_list:
            peer.sendTextPacket(G.addr_book_delta)
            peer.sendTextPacket('D'+pickle.dumps(AddrBookDelta))
        return
    
    def getPeerByAddr(self, net_addr):
        for peer in self.peer_list:
            if peer.net_addr == net_addr:
                return peer
        return None

        
    def callPeer(self, contact):
        hash_addr_other = self.crypto.pubKeyHash(contact.keyN, contact.keyE)
        hash_addr_self = self.crypto.pubKeyHashSelf()
        print "Callee address ", pub_key_hash_other
        peer = None
        sign = None
        for ad in self.AddrBook:
            if ad[0] == pub_key_hash_other:
                print "callPeer: Address found in AddrBook"
                sign = self.crypto.decryptSignature(ad[1],self.crypto.toPubKey(contact.keyE, contact.keyN)) # sign is decrypted signature
                peer = self.getPeerByAddr(sign.net_addr)
        if peer != None:
            print peer
            peer.sendTextPacket(G.call_req )
            peer.recieveTextPacket()
            peer.sendTextPacket('Call'+hash_addr_self + G.separator + hash_addr_other)
            reply = peer.recieveTextPacket()
            if reply == G.call_reject:
                print "Peer rejected call"
                return "Peer rejected call"
            elif reply == G.call_ready:
                self.callFlag = True
                #makeCallFunc()
                self.callFlag = False
                
        elif sign != None:
            print "callPeer: Address not a peer. Trying to establish connection"
            self.supportServer.getcon(sign.net_addr)
            ret, peer = self.connect2peer(sign.net_addr)
            if ret:
                return self.callPeer(contact)
        else:
            print "Peer does not exist"
            return "Peer does not exist"

    def addToAddrBook(self, AddrBookDelta):
        h = self.crypto.simpleHash(pickle.dumps(AddrBookDelta))
        print "addToAddrBook: hash - ", h
        for t in self.AddrDeltaDict:
            if t == h:
                print "addToAddrBook : hash exists"
                return True
        self.AddrDeltaDict.append(h)    
        self.AddrBook = self.AddrBook+AddrBookDelta
        self.pushAddrBookDelta(AddrBookDelta)
        print "addToAddrBook: updated AddrBook", self.AddrBook
        return True

            
    def PeerListenerThread(self, peer):
        try:
            while True:
                if self.callFlag:
                    time.sleep(5)
                    continue
                if self.killFlag:
                    break
                #print "PeerListener : running"
                #peer.makeConnection()
                packet = peer.recieveTextPacket()
                #print "Recieved",packet
                if packet == G.peer_list_req:
                    pl = []
                    for it in self.peer_list:
                       pl.append(it[0].net_addr)
                    print "PeerListener: Peer list to send", pl
                    peer.sendTextPacket('P'+pickle.dumps(pl))

                elif packet == G.addr_book_delta:
                    AddrBookDelta_u = peer.recieveTextPacket()
                    if AddrBookDelta_u == None:
                        continue
                    if AddrBookDelta_u[0] == 'D':
                        AddrBookDelta_u = AddrBookDelta_u[1:]
                        AddrBookDelta = pickle.loads(AddrBookDelta_u)
                        print "Peer listener: AddrBookDelta recieved:", AddrBookDelta
                        self.addToAddrBook(AddrBookDelta)
                        print "PeerListener: Address Book delta updated"
                    
                elif packet == G.req_AddrBook:
                    peer.sendTextPacket('A'+pickle.dumps(self.AddrBook))
                    print "peerListener: sent AddrBook"

                elif packet == G.call_req:
                    print "Got call"
                    peer.sendTextPacket(G.ack)
                    packet = peer.recieveTextPacket()
                    if packet[:4] == 'Call':
                        packet = packet[4:]
                        hash_addr_other, k = packet.split(G.separator)
                        for contact in self.contacts:
                            if contact.h == hash_addr_other:
                                print "peer listener: got call"
                                self.incomingCallInterrupt = (True, contact, peer)
                                pass #Implement answer call mechanism
                        peer.sendTextPacket(G.call_reject)
                                        
        except KeyboardInterrupt:
            print "Keyboard interrupted"
            return



    
    
