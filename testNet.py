#!/usr/bin/python

import lib.NetworkLib.NetworkWrapper as net
import lib.CryptoLib.CryptoWrapper as crypto
from lib.NetworkLib.p2p import Peer
cryptoObj = crypto.CryptoHandler()
netHandler = net.NetworkHandler(cryptoObj)

netHandler.getFirstPeer()
peer = Peer("127.0.0.1:85", netHandler.supportServer)
#netHandler.connect2peer(peer)
#netHandler.getPeerList(peer)
netHandler.getAddrBook(peer)
