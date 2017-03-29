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




class CryptoHandler:
    def __init__(self):
        self.key_ring = [] 
        with open ('key_ring.binary', 'rb') as fp:
            self.key_ring = pickle.load(fp)
        if self.key_ring.count == 0:
            self.generateNewKeys
        self.setCurKey(0)


        
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
        
        return string(signatureC)
    
    def decryptSignature(self, signatureC, d_key):
        ##Decrypts signatureC cyphertext string using d_key
        
        return string(signatureP)
    
    def encryptAVString(self, AV_encode_string_d,e_key):
        ##Returns a ciphertext of encrypted AV_encode_string

        #Add security according to network lib security.
        
        return AV_encode_string_d

    
    def decryptAVString(self,AV_encode_string_e, d_key):
        ##Returns a plaintext of decrypted AV_encode_string

        #Add encryption according to network library security
        return AV_encode_string_e 




