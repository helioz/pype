import lib.NetworkLib.p2p as p2p
from lib.AVLib.AVWrapper import AVHandler
import Resources._globals as G
peer = p2p.Peer("127.0.0.1+8052", p2p.SupportServer())
AVHandler(peer).callAV()
