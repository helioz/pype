import lib.AVLib.AVWrapper
import lib.NetworkLib.NetworkWrapper
from lib.CryptoLib.CryptoWrapper import CryptoHandler

def testCrypto():
    c = CryptoHandler()
    c.generateNewKeys()
    c.setCurKey(1)
    print c.public_key().e
    print c.public_key().n
    print c.private_key().d
    print c.sha256("Hello")
    if "MTg1ZjhkYjMyMjcxZmUyNWY1NjFhNmZjOTM4YjJlMjY0MzA2ZWMzMDRlZGE1MTgwMDdkMTc2NDgyNjM4MTk2OQ==" == c.sha256("Hello"):
        print "SHA256 passed"
    else:
        print "SHA256 failed"
    
    
    if "Hello" == c.decryptSignature(c.generateSignature("Hello"),c.public_key()):
        print "Signature Encryption/Decryption successful"
    else:
        print "Signature Encryption/Decryption failed"
    
    if "Hello" ==  c.rsaDecrypt(c.rsaEncrypt("Hello",c.public_key())):
        print "RSA Encryption/Decryption successful"
    else:
        print "RSA Encryption/Decryption successful"

def testNetwork():
    return True
    
def run_diag():
    testCrypto()
    testNetwork()
