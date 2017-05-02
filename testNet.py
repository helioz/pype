#!/usr/bin/python

import lib.NetworkLib.NetworkWrapper as net
import lib.CryptoLib.CryptoWrapper as crypto
from lib.NetworkLib.p2p import Peer
import Resources._globals as G
import time
import sys
cryptoObj = crypto.CryptoHandler()
netHandler = net.NetworkHandler(cryptoObj)

#netHandler.getFirstPeer()
#G.PORT_local = 7005
print G.PORT_local
peer = Peer("192.168.1.106:6369", netHandler.supportServer)
#netHandler.connect2peer(peer)
#netHandler.getPeerList(peer)


if peer.makeConnection():
    print "Connection made"
else:
    print "Connection failed"
    
# for i in range(5):
#     print peer.sendTextPacket("Hello from the other peer")

