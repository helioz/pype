import lib.NetworkLib.p2p as p2p
from lib.AVLib.AVWrapper import AVHandler
import Resources._globals as G


G.PORT_local = 6021
peer = p2p.Peer("137.97.10.22+6821", p2p.SupportServer())

AVHandler(peer).callAV()
