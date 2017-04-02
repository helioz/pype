##All data structures to hold information is defined here

import Resources._globals as GLOBALS
from lib.CryptoLib.CryptoWrapper import CryptoHandler
from lib.NetworkLib.NetworkWrapper import NetworkHandler

import pickle

class AddrBook:
    ## struct AddrBook{ String hash_addr; String signature}
    def __init__(self):
        pass

class PeerList:
    ## struct PeerList { struct Netaddr netaddr, String controlFlags}
    def __init__(self):
        pass


class Contact:
    def __init__(self, name, keyE, keyN):
        self.name = name
        self.keyN = keyN
        self.keyE = keyE
        
        #self.hash_addr = crypto.generateHashAddr(keyE, keyN)

class Pype:
    def __init__(self):
        self.crypto = CryptoHandler()
        self.network = NetworkHandler()
    
    


def saveContact(Contact):
    contact_list = []
    try:
        with open(GLOBALS.contacts_file,"rb") as f:
            contact_list = pickle.load(f)
            contact_list.append(Contact)
        with open(GLOBALS.contacts_file, "wb") as f: ##This is a potential error, fix ASAP. Initialise Pype must include an empty contact
            pickle.dump(contact_list, f)
            
    except IOError:
        with open(GLOBALS.contacts_file,"wb") as f:
                  contact_list.append(Contact)
                  pickle.dump(contact_list, f)

                  


