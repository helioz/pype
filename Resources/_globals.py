name = "Pype"
version_no = "0.0.4"

MAX_Peers = 10

IPADDR_support_server = "31.171.246.149"
PORT_support_server = 9898

import random
PORT_local = random.choice(range(6000,7000))
NET_ADDR_self = "127.0.0.1:3457"


key_ring_binary = "Resources/key_ring.binary"
contacts_file = "Resources/contacts.binary"
nameCard = "Resources/nameCardFile.text"

key_size = 1024
hash_size = 15

frame_rate = 1.0/24.0

separator = '_'
port_separator = '+'


##Network globals
mediaPacket_maxsize = 15000
packet_maxsize = 2048
punchTimeout = 3
mediaTimeOut = 0.01
nOfIteration = 4
waiting_time = 3


#Network Codes
ack = "ack"

call_req = "call_req"
call_ready = "call_ready"
call_reject = "call_reject"

peer_list_req = "peer_list_req"

req_AddrBook = "req_AddrBook"

addr_book_delta = "delta"
