##All data structures to hold information is defined here

import Resources._globals as GLOBALS
from lib.CryptoLib.CryptoWrapper import CryptoHandler
from lib.NetworkLib.NetworkWrapper import NetworkHandler
from lib.AVLib.AVWrapper import AVHandler
import lib.NetworkLib.p2p as p2p

import pickle
import threading
import random
import time


class PeerListener(threading.Thread):
    def __init__(self, threadID, peer, listenerFunc, interruptFunc):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.peer = peer
        self.listenerFunc = listenerFunc
        self.interruptFunc = interruptFunc
    def run(self):
        print "Listener running for peer :",self.peer.net_addr
        self.listenerFunc(self.peer, self.interruptFunc)
        print "Closing connection to peer :",self.peer.net_addr
        
## struct net_addr (ip_addr, port)

class ServerPollThread(threading.Thread):
    def __init__(self, listenerFunc):
        threading.Thread.__init__(self)
        self.listenerFunc = listenerFunc
    def run(self):
        print "Running server poll thread"
        self.listenerFunc()




class Signature:
    def __init__(self, net_addr, hash_addr, meta_data):
        self.net_addr = net_addr
        #self.hash_addr = hash_addr
        #self.meta_data = meta_data


#AddrBook = [("hash_address","encrypted_signature")]
#AddrDeltaDict = ["hash"]
#peer_list = [(Peer, control_flags), (Peer, control_flags)]


class Contact:
    def __init__(self, name, keyE, keyN):
        self.name = name
        self.keyN = keyN
        self.keyE = keyE
        self.h = CryptoHandler().pubKeyHash(keyN, keyE)
        

class Pype:
    def __init__(self):
        self.thread_count = 0

        self.newPeerInterrupt = False
        self.newCallInterrupt = False
        self.notKillAll = True
        self.calleePeer = 0
        self.peerThreads = []

        #Initialising bottom layers
        self.crypto = CryptoHandler()
        ##Loads keyring from file
        ##Sets current key to 0
        self.network = NetworkHandler(self.crypto)
        ##Finds current net address
        self.runPype()
        
    def runPype(self):
        #First peer connection
        self.connectToFirstPeer()


        #Server listener thread
        self.serverPollThread = ServerPollThread(self.serverPollThreadFunc)
        self.serverPollThread.start()
        
        # while True:
        #     self.network.getFirstPeer()
        #     time.sleep(5)
        #     if self.network.numPeers > 0:
        #         break
        #     print "runPype: Failed to get first peer. Retrying...."
            
        #Get first peer from server

        #Get address book

        #Update address book with self address

        #Populate peer_list
        print "runPype: list population"
        for p in self.network.peer_list:
            peer_list = self.network.getPeerList(p[0])
            if peer_list == None:
                continue
            for peer in peer_list:
                #if random.choice([1,2,3]) == 3:
                if peer[0].net_addr != GLOBALS.NET_ADDR_self and peer not in self.network.peer_list:
                    self.network.supportServer.getcon(peer[0].net_addr)
                    if self.network.connect2peer(peer[0]):
                        self.peerThreads.append(PeerListener(self.thread_count, self.network.peer_list[self.thread_count][0], self.network.PeerListenerThread, self.callInterrupt))
                        self.peerThreads[self.thread_count].start()                    
                        self.thread_count = self.thread_count + 1                    

        print "runPype : peer list populated and threads running"
        
        #Launching peer threads
        # while self.thread_count < len(self.network.peer_list):
        #     if peer[0].net_addr != GLOBALS.NET_ADDR_self:
                



        
        print "runPype: getAddrBook"
        self.network.getAddrBook(self.network.peer_list[0][0])
        AddrBookDelta = [(self.crypto.pubKeyHashSelf(), self.crypto.generateSignature(Signature(GLOBALS.NET_ADDR_self, self.crypto.pubKeyHashSelf(), 0)))]
        time.sleep(random.choice(range(5)))
        self.network.addToAddrBook(AddrBookDelta)
        print "runPype: AddrBookDelta published"


        print "pypeRun: Initialisation Complete, starting UI"
        #Listening to all peers as threads
        
        #threading.Thread(target = self.makeCall).start()

        
            

    def callInterrupt(self, control, arg):
        if control == 2:
            return loadContacts()
        if control == 1:
            self.newCallInterrupt = True
            #self.calleePeer = arg

    def makeCall(self):
        while True:
            if self.newCallInterrupt:
                AVHandler(self.calleePeer).callAV()
            time.sleep(5)

    def connectToFirstPeer(self):
        print "connectToFirstPeer: Attempting connection to first peer"
        while True and self.notKillAll:
            firstPeerAddr = self.network.supportServer.getFirstPeer()
            
            if firstPeerAddr == 'end':
                continue
            if firstPeerAddr == GLOBALS.NET_ADDR_self:
                continue
            time.sleep(2)
            print "connectToFirstPeer : ",firstPeerAddr
            #firstPeer = p2p.Peer(firstPeerAddr, self.network.supportServer)
            # self.network.supportServer.getcon(firstPeer.net_addr)
            # if firstPeer.makeConnection():
            #     self.network.peer_list.append((firstPeer,0))
            #     self.network.network.addNode(firstPeer)
            ret, firstPeer = self.network.connect2peer(firstPeerAddr)
            if ret:
                print "First peer connected"
                self.peerThreads.append(PeerListener(self.thread_count, firstPeer, self.network.PeerListenerThread, self.callInterrupt))
                self.peerThreads[self.thread_count].start()
                self.thread_count = self.thread_count + 1
                print "First peer thread started. Success"
                time.sleep(3)
                return

    def serverPollThreadFunc(self):
        #time.sleep(random.choice(range(5)))
        time.sleep(10)
        while True and self.notKillAll:
            time.sleep(20)
            #while self.newCallInterrupt:  #Disable thread during call
            #    time.sleep(10)
            
            connList = self.network.supportServer.poll()
            print "Poll thread running"
            if connList != None:
                connListNoDup = []
                for adr in connList:
                    if adr == GLOBALS.NET_ADDR_self:
                        continue
                    if not (adr in connListNoDup):
                        connListNoDup.append(adr)
                for adr in connListNoDup:
                    ret, newPeer = self.network.connect2peer(adr)
                    if ret:
                        #newPeer = p2p.Peer(adr, self.network.supportServer)
                        self.peerThreads.append(PeerListener(self.thread_count, newPeer, self.network.PeerListenerThread, self.callInterrupt))
                        self.peerThreads[self.thread_count].start()
                        self.thread_count = self.thread_count + 1
                        print "Server thread makes new peer thread", newPeer
                    #else:
                        #newPeer.makeConnection()
        


            

        


        

        
        
        
        



        
        
        
        
    
    


def saveContact(contact):
    try:
        with open(GLOBALS.contacts_file,"rb") as f:
            unpickler = pickle.Unpickler(f)
            contact_list = unpickler.load()
            if contact_list[0].name == "none":
                contact_list.remove(contact_list[0])
            contact_list.append(contact)
        with open(GLOBALS.contacts_file, "wb") as f: ##This is a potential error, fix ASAP. Initialise Pype must include an empty contact
            pickle.dump(contact_list, f)
            
    except IOError:
        with open(GLOBALS.contacts_file,"wb") as f:
            contact_list = [contact]
            pickle.dump(contact_list, f)

                  
def loadContacts():
    #contact_list = []
    try:
        with open(GLOBALS.contacts_file, "rb") as f:
            try:
                unpickler = pickle.Unpickler(f)
                contact_list = unpickler.load()
                #contact_list = pickle.load(f)
                #if contact_list[0].name == "none":
                #    contact_list.remove(contact_list[0])
                return contact_list
            except EOFError:
                print "No contacts found"
                saveContact(Contact("none",0,0))
                #contact_list = [Contact("None",0,0)]
                return contact_list

    except IOError:
        print "Contacts file does not exist, creating new"
        with open(GLOBALS.contacts_file,"wb") as f:
            contact_list = [Contact("none",0,0)]
            pickle.dump(contact_list, f)
            return contact_list


