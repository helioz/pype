#!/usr/bin/python

import lib.NetworkLib.NetworkWrapper as net
import lib.CryptoLib.CryptoWrapper as crypto
from lib.NetworkLib.p2p import Peer
import Resources._globals as G
import time
cryptoObj = crypto.CryptoHandler()
netHandler = net.NetworkHandler(cryptoObj)

#netHandler.getFirstPeer()
peer = Peer("192.168.1.102:"+str(G.PORT_local), netHandler.supportServer)
#netHandler.connect2peer(peer)
#netHandler.getPeerList(peer)

for i in range(20):
    print peer.recieveTextPacket()

