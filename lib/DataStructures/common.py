##All data structures to hold information is defined here

import Resources._globals as GLOBALS
from lib.CryptoLib.CryptoWrapper import CryptoHandler
from lib.NetworkLib.NetworkWrapper import NetworkHandler

import pickle

## struct net_addr (ip_addr, port)

class Signature:
    def __init__(self, net_addr, hash_addr, meta_data):
        self.net_addr = net_addr
        self.hash_addr = hash_addr
        self.meta_data = meta_data


#AddrBook = [("hash_address","encrypted_signature")]
#AddrDeltaDict = ["hash"]
#peer_list = [(Peer, control_flags), (Peer, control_flags)]


class Contact:
    def __init__(self, name, keyE, keyN):
        self.name = name
        self.keyN = keyN
        self.keyE = keyE
        self.h = CryptoWrapper().pubKeyHash(keyN, keyE)
        

class Pype:
    def __init__(self):
        self.crypto = CryptoHandler()
        self.network = NetworkHandler(self.crypto)
    
    


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

                  


