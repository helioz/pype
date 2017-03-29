##Wrapper class for cryptographic operations

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto import Random
from Crypto.Hash import SHA256
from Crypto.Cipher import AES
import ast
import base64 as b64
import pickle

Key_Size = 1024

# #random_generator = Random.new().read
# #key = RSA.generate(1024, random_generator) #generate pub and priv key

# #publickey = key.publickey() # pub key export for exchange

# encrypted = publickey.encrypt('encrypt this message', 32)
# #message to encrypt is in the above line 'encrypt this message'

# print 'encrypted message:', b64.b64encode(encrypted[0]) #ciphertext
# f = open ('encryption.txt', 'w')
# f.write(b64.b64encode(encrypted[0])) #write ciphertext to file
# f.close()

# #decrypted code below

# f = open('encryption.txt', 'r')
# message = f.read()

# encrypted = b64.b64decode(message)


# decrypted = key.decrypt(encrypted)

# print 'decrypted', decrypted

# f = open ('encryption.txt', 'w')
# f.write(str(message))
# f.write(str(decrypted))
# f.close()

class CryptoHandler:
    def __init__(self):
        self.key_ring = []  ##A list containing (pub_key, priv_key)
        #self.generateNewKeys()
        with open ('key_ring.binary', 'rb') as fp:
            self.key_ring = pickle.load(fp)
        if self.key_ring.count == 0:
            self.generateNewKeys
        self.setCurKey(0)
        ##self.cur_key ##Stores current (pub_key, priv_key)
        ##self.cur_hash_addr = 0 ##Stores current hash_addr (base64 encoding)
        
    def generateNewKeys(self):
        ##Generates a new pair of keys and adds it to key_ring
        random_generator = Random.new().read
        key = RSA.generate(Key_Size, random_generator) #generate pub and priv key
        self.key_ring.append(key)
        with open('key_ring.binary', 'wb') as fp:
            pickle.dump(self.key_ring, fp)

    def setCurKey(self, keyIndex):
        self.cur_key = self.key_ring[keyIndex]
        
    def sha256(self,inp_string):
        ##Returns a base64 sha256 string corresponding to inp_string
        h = SHA256.new(inp_string)
        h = b64.b64encode(h.hexdigest())
        #print h
        return h

    def generateSignature(self, signatureP):
        ##Encrypts signatureC plaintext string with current private key

        #Fix signatureP to be a bytestring

        enc = self.cur_key.publickey()
        enc.e = self.cur_key.d
        
        cipher = PKCS1_OAEP.new(enc)
        #signatureC = cipher.encrypt(signatureP)
        signatureC = enc.encrypt(signatureP,32)
        print b64.b64encode(signatureC[0])
        return signatureC[0]

    
    def decryptSignature(self, signatureC, d_key):
        ##Decrypts signatureC cyphertext string using d_key
        dec = RSA.generate(1024)
        dec.d = d_key.e
        dec.n = d_key.n
        cipher = PKCS1_OAEP.new(dec)
        #signatureP = cipher.decrypt(signatureC)
        signatureP = dec.decrypt(signatureC)
        print b64.b64encode(signatureP)
        return signatureP
    
    def encryptAVString(self, AV_encode_string_d,e_key):
        ##Returns a ciphertext of encrypted AV_encode_string
        pass

    
    def decryptAVString(self,AV_encode_string_e, d_key):
        ##Returns a plaintext of decrypted AV_encode_string
        pass


c = CryptoHandler()
print c.decryptSignature(c.generateSignature("Hello, a string"),c.cur_key.publickey())


# random_generator = Random.new().read
# key = RSA.generate(1024, random_generator) #generate pub and priv key


# msg = 'Attack at eastern frontier'
# keyPub = key.publickey()
# keyPub.e = key.d

# print keyPub.e

# cipher = PKCS1_OAEP.new(keyPub)
# ciphertext = cipher.encrypt(msg)

# print b64.b64encode(ciphertext)
# keyPub = key.publickey()

# msg1 = cipher.decrypt(ciphertext)

# print msg1
