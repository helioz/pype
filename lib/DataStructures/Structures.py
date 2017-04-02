##All data structures to hold information is defined here

import Resources._globals as GLOBALS
import lib.CryptoLib.CryptoWrapper as crypto
import pickle

class Contact:
    def __init__(self, name, keyE, keyN):
        self.name = name
        self.keyN = keyN
        self.keyE = keyE
        #self.hash_addr = crypto.generateHashAddr(keyE, keyN)


def saveContact(Contact):
    contact_list = []
    try:
        with open(GLOBALS.contacts_file,"rb") as f:
            contact_list = pickle.load(fp)
            contact_list.append(Contact)
        with open(GLOBALS.contacts_file, "wb") as f: ##This is a potential error, fix ASAP.
            pickle.dump(contact_list, f)
            
    except IOError:
        with open(GLOBALS.contacts_file,"wb") as f:
                  contact_list.append(Contact)
                  pickle.dump(contact_list, f)

                  

                  
