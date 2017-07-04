
import time
from socket import *
from exploranetworking import *



def messageClient():
    print(f'Test Client')
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    clientSocket.settimeout(1)
    addr = ("127.0.0.1", 12000)

    start = time.time()
    byteStr = JoinServerMessage().toBytes()
    if len(byteStr) > UDP_MAX_SIZE:
        raise Exception("Message too long for our UDP buffers.")
    clientSocket.sendto(byteStr, addr)
    try:
        data, server = clientSocket.recvfrom(1024)
        end = time.time()
        elapsed = end - start
        print(f"{data} {elapsed}")
    except timeout:
        print("REQUEST TIMED OUT")
    
messageClient()
