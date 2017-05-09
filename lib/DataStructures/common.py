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
    def __init__(self, threadID, peer, listenerFunc):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.peer = peer
        self.listenerFunc = listenerFunc
    def run(self):
        print "Listener running for peer :",self.peer.net_addr
        self.listenerFunc(self.peer)
        print "Closing connection to peer :",self.peer.net_addr
## struct net_addr (ip_addr, port)

class ServerPollThread(threading.Thread):
    def __init__(self, listenerFunc):
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
        self.newPeers = False
        #Initialising bottom layers
        self.crypto = CryptoHandler()
        ##Loads keyring from file
        ##Sets current key to 0
        
        self.network = NetworkHandler(self.crypto)
        ##Finds current net address
        self.multi = AVHandler()
        
    def runPype():
        self.peerThreads = []

        #Server listener thread
        self.serverPollThread = ServerPollThread(self.serverPollThreadFunc)
        self.serverPollThread.start()
        
        
        while not self.network.getFirstPeer():
            print "Failed to get first peer. Retrying...."
            time.sleep(3)
        #Get first peer from server

        #Get address book

        #Update address book with self address

        #Populate peer_list
        for p in self.network.peer_list:
            peer_list = self.network.getPeerList(p[0])
            for peer in peer_list:
                #if random.choice([1,2,3]) == 3:
                if peer[0].net_addr != GLOBALS.NET_ADDR_self:
                    self.network.connect2peer(peer[0])

                    
        self.network.getAddrBook(self.network.peer_list[0][0])
        AddrBookDelta = [(self.crypto.pubKeyHashSelf(), self.crypto.generateSignature(Signature(GLOBALS.NET_ADDR_self, self.crypto.pubKeyHashSelf(), 0)))]
        network.addToAddrBook(AddrBookDelta)
        
        #Listening to all peers as threads

        for peer in self.network.peer_list:
            self.peerThreads.append(PeerListener(thread_count, peer[0], self.network.PeerListenerThread, self.mainInterrupt))
            self.peerThreads[thread_count].start()
            self.thread_count = self.thread_count + 1
            
                        
                    
                        
        
            

    def mainInterrupt(control, var):
        if control == 1:
            pass #Start calling thread with var as peer
                
    def serverPollThreadFunc(self):
        while True:
            if not self.newPeers:
                connList = self.network.supportServer.poll()
                for adr in connList:
                    newPeer = p2p.Peer(adr, self.network.supportServer)
                    if self.network.connect2peer(newPeer):
                        self.peerThreads.append(PeerListener(thread_count, newPeer, self.network.PeerListenerThread), self.mainInterrupt)
                        self.peerThreads[thread_count].start()
                        self.thread_count = self.thread_count + 1
                    
            time.sleep(5)

            

        


        

        
        
        
        



        
        
        
        
    
    


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


