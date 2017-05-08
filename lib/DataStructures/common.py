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

noCallGlobal = True

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
        global noCallGlobal
        #Initialising bottom layers
        self.crypto = CryptoHandler()
        ##Loads keyring from file
        ##Sets current key to 0
        
        self.network = NetworkHandler(self.crypto)
        ##Finds current net address
        self.multi = AVHandler()

        self.peerThreads = []
        
        while not self.network.getFirstPeer():
            print "Failed to get first peer. Retrying...."
            time.sleep(1)
        #Get first peer from server

        #Get address book
        self.network.getAddrBook(self.network.peer_list[0][0])
        #Update address book with self address
        AddrBookDelta = [(self.crypto.pubKeyHashSelf(), self.crypto.generateSignature(Signature(GLOBALS.NET_ADDR_self, self.crypto.pubKeyHashSelf(), 0)))]
        #Populate peer_list
        for p in self.network.peer_list:
            peer_list = self.network.getPeerList(p[0])
            for peer in peer_list:
                if random.choice([1,2,3]) == 3:
                    self.network.connect2peer(peer[0])

        network.addToAddrBook(AddrBookDelta)
        
        #Listening to all peers as threads
        self.thread_count = 0
        for peer in self.network.peer_list:
            self.peerThreads.append(PeerListener(thread_count, peer[0], self.network.PeerListenerThread))
            self.peerThreads[thread_count].start()
            self.thread_count = self.thread_count + 1
            

        try:
            while True:
                while noCallGlobal:
                    #listenToServer
                    pass

        except KeyboardInterrupt:
            print "Fin"
            
            
                
                
            

        


        

        
        
        
        



        
        
        
        
    
    


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


