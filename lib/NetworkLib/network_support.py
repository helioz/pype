##All support functions for network handler class goes here.

def stringToTuple(addr):
    ip, port = addr.split('+')
    return ip, int(port)
