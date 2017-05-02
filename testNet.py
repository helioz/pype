#!/usr/bin/python

import lib.NetworkLib.NetworkWrapper as net
import lib.CryptoLib.CryptoWrapper as crypto
from lib.NetworkLib.p2p import Peer
import Resources._globals as G
import time
import sys

cryptoObj = crypto.CryptoHandler()
n = net.NetworkHandler(cryptoObj)

print G.PORT_local
peer = Peer("192.168.1.106:6369", n.supportServer)

#peer.makeConnection()
n.getPeerList(peer)
#n.ThreadListener(peer)

