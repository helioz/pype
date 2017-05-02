#!/usr/bin/python

import lib.NetworkLib.NetworkWrapper as net
import lib.CryptoLib.CryptoWrapper as crypto
from lib.NetworkLib.p2p import Peer
import Resources._globals as G
import time
cryptoObj = crypto.CryptoHandler()
netHandler = net.NetworkHandler(cryptoObj)

#netHandler.getFirstPeer()
G.PORT_local = 7006
print G.PORT_local
peer = Peer("127.0.0.1:7005", netHandler.supportServer)
#netHandler.connect2peer(peer)
#netHandler.getPeerList(peer)

for i in range(5):
   peer.makeConnection()

# for i in range(5):
#    print peer.recieveTextPacket()
#    print "Recieve",i
