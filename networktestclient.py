
import time
from socket import *
from exploranetworking import *



def messageClient():
    print(f'Test Client')
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    clientSocket.settimeout(1)
    serverAddr = ("127.0.0.1", 12000)

    start = time.time()
    byteStr = JoinServerMessage().toBytes()
    if len(byteStr) > UDP_MAX_SIZE:
        raise Exception("Message too long for our UDP buffers.")
    clientSocket.sendto(byteStr, serverAddr)
    try:
        data, server = clientSocket.recvfrom(UDP_MAX_SIZE)
        end = time.time()
        elapsed = end - start
        print(f"{data} {elapsed}")
    except timeout:
        print("REQUEST TIMED OUT")
    byteStr = KeyPressedMessage(115).toBytes()
    if len(byteStr) > UDP_MAX_SIZE:
        raise Exception("Message too long for our UDP buffers.")
    clientSocket.sendto(byteStr, serverAddr)

messageClient()
