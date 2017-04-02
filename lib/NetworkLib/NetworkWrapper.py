##Wrapper class for Network operations.
##Manages all high level applications of the network, works based on classes and functions defined in the network_support library and p2p library

#Control strings
import p2p

C_101 = b'101:NACK'
C_102 = b'102:ACK'
C_103 = b'103:CLOSE_CONNECTION'
C_104 = b'104:POLL'
C_105 = b'105:ENCRYPTION_KEY'
C_106 = b'106:READY_FOR_KEY'
C_107 = b'107:ENCRYPTION_READY'

C_201 = b'201:CONNECT_TO_PEER_REQ'
C_202 = b'202:PEER_ADDR_READY'
C_203 = b'203:NODE_ADDR_READY'
C_204 = b'204:REQ_SUCCESS'

C_301 = b'301:GET_PEER_LIST'

C_401 = b'401:NEW_PEER_REQ'
C_402 = b'402:READY_FOR_NEW_PEER'

C_501 = b'501:GET_PEER_LIST'
C_502 = b'502:PEER_LIST_READY'

C_601 = b'601:GET_ADDR_BOOK'
C_602 = b'602:ADDR_BOOK_READY'

C_701 = b'701:PUSH_NEW_ADDR'
C_702 = b'702:READY_TO_RECV_PUSH'

C_801 = b'801:NEW_CALL_REQ'
C_802 = b'802:CALL_ACK'
C_803 = b'803:PUB_KEY_VERIFICATION'
C_804 = b'803:CALLER_ID'
C_805 = b'803:READY_TO_RECV'
C_806 = b'804:DISCONNECT_CALL'

class NetworkHandler:
    def __init__(self, support_server_ip_addr, support_server_holePunchPort, support_server_getPeerPort):
        self.peer_list = [] ##peer_list is a dictionary that contains net_addr and control flags of peers
        self.network = P2PNetwork()
        self.supportServer = p2p.SupportServer(support_server_ip_addr, support_server_holePunch, support_server_getPeerPort)

    def getFirstPeer(self):
        ##Returns the net_addr of first peer returned by support server

    def connect2peer(self, net_addr):
        ##Hole punches a connection to a peer, returns true or false


    def getPeerList(self, net_addr):
        ##Returns a peer_list from selected peer.
        

    def getAddrBook(self, net_addr):
        ##Returns AddrBook of selected peer

    def pushAddrBook(self):
        ##Broadcasts updates to AddrBook
        
    def callPeer(self,net_addr):
        ##Used to call a peer.

    def sendAV(self, AV_encode_string):
        ##Called by AV Handler to send AV
    
    
