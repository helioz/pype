peer = p2p.Peer(net_addr, supportServer)
peer.net_addr
peer.isPunched
peer.supportServer
peer.makeConnection() #Sends punch request to peer, returns true or False
peer.sendMediaPacket(string) #Sends media to peer
peer.recieveMediaPacket() #returns a string
peer.sendTextPacket(string)
peer.recieveTextPacket() #Return string or none
network = p2p.P2PNetwork()
network.nodeList #Array containing peers
network.addNode(peer) #Apends peer to nodeList
network.getPeerByAddr(net_addr) #Returns peer or none
network.pushBroadcast(string, ctrlString1, ctrlString2) #Sends ctrlStr1 asserts ctrlStr2 and sends string to all peers
supportServer = p2p.SupportServer()
supportServer.ip_addr
supportServer.sendTextPacket(string) #Sends string to ss and returns True, False if not sent
supportServer.recieveTextPacket() #Returns string or None from server
lib.NetworkLib.network_support.stringToTuple(net_addr) #Returns (ip, port)
sign = lib.DataStructures.common.Signature(net_addr, hash_addr, meta_data)
sign.net_addr
contact = lib.DataStructures.common.Contact(name, keyE, keyN)
contact.name
contact.keyE
contact.keyN
contact.h
crypto = lib.CryptoLib.CryptoWrapper.CryptoHandler()
crypto.generateNewKeys() #Adds new keys to keyring file and returns True
crypto.sha256(string) #returns b64 encoded sha256 of string
crypto.generateSignature(signatureP) #Returns b64encoded signature.
crypto.decryptSignature(signatureC, public_key) #Returns decrypted signatureC
crypto.rsaEncrypt(cleartext, public_key) #Returns b64encoded ciphertext
crypto.rsaDecrypt(ciphertext) #Decrypts c with current private key
crypto.enrcyptString(string, e_key) #Returns encrypted string
crypto.decrypString(string, d_key) #Returns decrypted string
crypto.public_key() #Returns current public key
crypto.private_key() #Returns current private key
crypto.pubKeyHash(keyE, keyN) #Returns hash address corresponding to given key
crypto.pubKeyHashSelf() #Returns hash address corresponding to current key
crypto.toPubKey(keyE, keyN) #Returns a public key object

