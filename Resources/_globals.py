name = "Pype"
version_no = "0.0.1"

MAX_Peers = 10

IPADDR_support_server = "127.0.0.1"
PORT_support_server = 80

PORT_local = 3755
NET_ADDR_self = "127.0.0.1:3457"


key_ring_binary = "Resources/key_ring.binary"
contacts_file = "Resources/contacts.binary"

key_size = 1024

##Network globals
packet_maxsize = 4096
punchTimeout = 10
nOfIteration = 10
waiting_time = 10

#Network Codes

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
C_302 = b'302:NO_PEER'

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
C_804 = b'804:CALLER_ID'
C_805 = b'805:READY_TO_RECV'
C_806 = b'806:DISCONNECT_CALL'

C_901 = b'901:AV'
