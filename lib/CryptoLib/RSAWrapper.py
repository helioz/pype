import rsa.pkcs1 as cry
import rsa.key as key
import rsa.common as common
import rsa.transform as transform
import rsa.core as core

def generate(nbits):
    return key.newkeys(nbits, False)

def encrypt(cleartext, public_key):
    ciphertext = cry.encrypt(cleartext, public_key)
    return ciphertext

def decrypt(ciphertext, private_key):
    cleartext = cry.decrypt(ciphertext, private_key)
    return cleartext

def encryptSignature(signature, priv_key):
    cleartext = signature
    keylength = common.byte_size(priv_key.n)
    padded = cry._pad_for_encryption(cleartext, keylength)
    
    payload = transform.bytes2int(padded)
    encrypted = priv_key.blinded_encrypt(payload)
    block = transform.int2bytes(encrypted, keylength)

    return block


    
def decryptSignature(signature, pub_key):
    keylength = common.byte_size(pub_key.n)
    encrypted = transform.bytes2int(signature)
    decrypted = core.decrypt_int(encrypted, pub_key.e, pub_key.n)
    clearsig = transform.int2bytes(decrypted, keylength)
    if clearsig[0:2] != b'\x00\x02':
        raise DecryptionError('Decryption failed')
    
    # Find the 00 separator between the padding and the message
    try:
        sep_idx = clearsig.index(b'\x00', 2)
    except ValueError:
        raise DecryptionError('Decryption failed')

    return clearsig[sep_idx + 1:]
    

