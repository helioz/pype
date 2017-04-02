#import UXWrapper
from ui import loadHomeScreen
import lib.AVLib.AVWrapper
import lib.NetworkLib.NetworkWrapper
from lib.CryptoLib.CryptoWrapper import CryptoHandler

##Check GTK Version


IPADDR_support_server = "127.0.0.1"
PORT_support_server_get_peer = 80
PORT_Node = 3755

def testCrypto():
    c = CryptoHandler()
    #c.generateNewKeys()
    c.setCurKey(2)
    print c.sha256("Hello")
    print c.decryptSignature(c.generateSignature("Hello"),c.public_key())
    print c.rsaDecrypt(c.rsaEncrypt("Hello",c.public_key()))
    c.setCurKey(1)
    print c.public_key().e
    print c.public_key().n
    c.setCurKey(2)
    print c.public_key().e
    print c.public_key().n
    c.setCurKey(3)
    print c.public_key().e
    print c.public_key().n

#testCrypto()
loadHomeScreen()

