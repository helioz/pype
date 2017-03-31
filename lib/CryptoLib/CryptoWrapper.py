##Wrapper class for cryptographic operations


from Crypto.Hash import SHA256
import base64 as b64
import pickle
import RSAWrapper as RSA



Key_Size = 2048




class CryptoHandler:
    def __init__(self):
        self.key_ring = []
        try:
            with open ('key_ring.binary', 'rb') as fp:
                self.key_ring = pickle.load(fp)
        except IOError:
            self.generateNewKeys()
        self.setCurKey(0)


        
    def generateNewKeys(self):
        ##Generates a new pair of keys and adds it to key_ring
        
        key = RSA.generate(Key_Size) #generate pub and priv key
        self.key_ring.append(key)
        with open('key_ring.binary', 'wb') as fp:
            pickle.dump(self.key_ring, fp)

    def setCurKey(self, keyIndex):
        self.cur_key = self.key_ring[keyIndex]
        
    def sha256(self, inp_string):
        ##Returns a base64 sha256 string corresponding to inp_string
        h = SHA256.new(inp_string)
        h = b64.b64encode(h.hexdigest())
        return h

    def generateSignature(self, signatureP):
        ##Encrypts signatureC plaintext string with current private key

        #Fix signatureP to be a bytestring
        signatureC = RSA.encryptSignature(signatureP,self.cur_key[1])
        return b64.b64encode(signatureC)
    
    def decryptSignature(self, signatureC, public_key):
        ##Decrypts signatureC cyphertext string using d_key
        nonb64 = b64.b64decode(signatureC)
        signatureP = RSA.decryptSignature(nonb64,public_key)
        return signatureP

    def rsaEncrypt(self, cleartext, public_key):
        #Encrypts cleartext with corresponding public_key
        ciphertext = b64.b64encode(RSA.encrypt(cleartext,public_key))
        return ciphertext

    def rsaDecrypt(self, ciphertext):
        ##Decrypts ciphertext with corresponding private_key
        cleartext = RSA.decrypt(b64.b64decode(ciphertext), self.private_key())
        return cleartext
    
    def encryptAVString(self, AV_encode_string_d,e_key):
        ##Returns a ciphertext of encrypted AV_encode_string

        #Add security according to network lib security.
        
        return AV_encode_string_d

    
    def decryptAVString(self,AV_encode_string_e, d_key):
        ##Returns a plaintext of decrypted AV_encode_string

        #Add encryption according to network library security
        return AV_encode_string_e
    def public_key(self):
        return self.cur_key[0]
    def private_key(self):
        return self.cur_key[1]



c = CryptoHandler()
c.generateNewKeys()
c.setCurKey(2)
print c.sha256("Hello")
print c.decryptSignature(c.generateSignature("Hello"),c.public_key())
print c.rsaDecrypt(c.rsaEncrypt("Hello",c.public_key()))

