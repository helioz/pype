import lib.NetworkLib.p2p as p2p
from lib.AVLib.AVWrapper import AVHandler
import Resources._globals as G


G.PORT_local = 7500
peer = p2p.Peer("192.168.1.103+7500", p2p.SupportServer())

AVHandler(peer).callAV()
