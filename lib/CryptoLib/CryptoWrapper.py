##Wrapper class for cryptographic operations

class CryptoHandler:
    def __init__(self):
        self.key_ring = []  ##A list containing (pub_key, priv_key)
        
        self.cur_key = (0,0) ##Stores current (pub_key, priv_key)
        self.cur_hash_addr = 0 ##Stores current hash_addr (base64 encoding)
        
    def generateNewKeys(self):
        ##Generates a new pair of keys and adds it to key_ring

    def sha256(self,inp_string):
        ##Returns a base64 sha256 string corresponding to inp_string

    def generateSignature(self, signatureP):
        ##Encrypts signatureC plaintext string with current private key

    def decryptSignature(self, signatureC, d_key):
        ##Decrypts signatureC cyphertext string using d_key

    def encryptAVString(self, AV_encode_string_d,e_key):
        ##Returns a ciphertext of encrypted AV_encode_string

    def decryptAVString(self,AV_encode_string_e, d_key):
        ##Returns a plaintext of decrypted AV_encode_string
