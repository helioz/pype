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
    def __init__(self, peer, listenerFunc):
        threading.Thread.__init__(self)
        self.threadID = peer.net_addr
        self.peer = peer
        self.listenerFunc = listenerFunc

        
    def run(self):
        print "Listener running for peer :",self.peer.net_addr
        self.listenerFunc(self.peer)
        #Find a way to remove peer from peer list
        print "Closing connection to peer :",self.peer.net_addr
        

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


class Contact:
    def __init__(self, name, keyE, keyN):
        self.name = name
        self.keyN = keyN
        self.keyE = keyE
        self.h = CryptoHandler().pubKeyHash(keyN, keyE)
        
def saveContact(contact):
    try:
        with open(GLOBALS.contacts_file,"rb") as f:
            print "File operation"
            unpickler = pickle.Unpickler(f)
            contact_list = unpickler.load()
            if contact_list[0].name == "none":
                contact_list.remove(contact_list[0])
            contact_list.append(contact)
        with open(GLOBALS.contacts_file, "wb") as f: ##This is a potential error, fix ASAP. Initialise Pype must include an empty contact
            pickle.dump(contact_list, f)
            
    except IOError:
        with open(GLOBALS.contacts_file,"wb") as f:
            print "File operation"
            contact_list = [contact]
            pickle.dump(contact_list, f)



def loadContacts():
    #contact_list = []
    try:
        with open(GLOBALS.contacts_file, "rb") as f:
            print "File operation"
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
            print "File operations"
            contact_list = [Contact("none",0,0)]
            pickle.dump(contact_list, f)
            return contact_list


class Pype:
    def __init__(self):

        self.crypto = CryptoHandler()
        self.network = NetworkHandler(self.crypto)
        
        #self.peerThreads = []
        #self.thread_count = 0

        self.killFlag = False

        #self.runPype()
        


    def runPype(self):

        self.connectToFirstPeer()

        if self.killFlag:
            return


        self.serverPollThread = ServerPollThread(self.serverPollThreadFunc)
        self.serverPollThread.start()
        

        print "runPype: list population"
        for p in self.network.peer_list:
            peer_list = self.network.getPeerList(p)
            if peer_list == None:
                continue
            
            for peer in peer_list:
                #if random.choice([1,2,3]) == 3:         ##Add later for randomising peers
                if peer != GLOBALS.NET_ADDR_self: 
                    self.network.supportServer.getcon(peer)
                    ret, newPeer = self.network.connect2peer(peer)
                    #Replace thread_count with a better threadIdentification scheme, dict for example.
                    if ret: 
                        newPeer.listenerThread =  PeerListener( newPeer, self.network.PeerListenerThread )
                        newPeer.listenerThread.start()



        print "runPype : peer list populated and threads running"


        
        if self.killFlag:
            return


        
        
        print "runPype: getAddrBook"
        self.network.getAddrBook(self.network.peer_list[0])
        AddrBookDelta = [(self.crypto.pubKeyHashSelf(), self.crypto.generateSignature(Signature(GLOBALS.NET_ADDR_self, self.crypto.pubKeyHashSelf(), 0)))]
        time.sleep(random.choice(range(3)))
        self.network.addToAddrBook(AddrBookDelta)
        print "runPype: AddrBookDelta published"

        if self.killFlag:
            return


        print "pypeRun: Initialisation Complete, starting UI"


    def connectToFirstPeer(self):
        print "connectToFirstPeer: Attempting connection to first peer"
        while True:
            if self.killFlag:
                return
            
            firstPeerAddr = self.network.supportServer.getFirstPeer()
            
            if firstPeerAddr == 'end':
                time.sleep(2)
                continue
            if firstPeerAddr == GLOBALS.NET_ADDR_self:
                time.sleep(2)
                continue
            
            print "connectToFirstPeer : ",firstPeerAddr

            ret, firstPeer = self.network.connect2peer(firstPeerAddr)
            if ret:  
                print "First peer connected"
                firstPeer.listenerThread =  PeerListener( firstPeer, self.network.PeerListenerThread )
                firstPeer.listenerThread.start()
                print "First peer thread started. Success"
                time.sleep(3)
                return

    def serverPollThreadFunc(self):
        while True:
            if self.killFlag:
                return
            if self.network.callFlag:
                time.sleep(15)
                continue
            
            time.sleep(15)
            #while self.newCallInterrupt:  #Disable thread during call
            #    time.sleep(10)
            
            connList = self.network.supportServer.poll()
            #print "Poll thread running"
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
                        newPeer.listenerThread =  PeerListener( newPeer, self.network.PeerListenerThread )
                        newPeer.listenerThread.start()
                        print "Server thread makes new peer thread", newPeer


        


            

        


        

        
        
        
        



        
        
        
        
    
    


                  

