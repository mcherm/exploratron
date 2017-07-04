
import time
from socket import *
from exploranetworking import *
import select
import random

sampleKeys = [115, 97, 119, 100]

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

    while True:
        readyToReadSockets, (), () = select.select([clientSocket], [], [], 0)
        if readyToReadSockets:
            byteStr, address = readyToReadSockets[0].recvfrom(UDP_MAX_SIZE)
            message = bytesToMessage(byteStr)
            if isinstance(message, WelcomeClientMessage):
                print(f"Server sent WelcomeClientMessage: {message}.")
            elif isinstance(message, NewRoomMessage):
                print(f"Server sent NewRoomMessage: {message}.")
            else:
                raise Exception(f"Message type {message} not supported.")
        if random.randrange(600000) < 1:
            keyCode = random.choice(sampleKeys)
            print(f"About to send a {keyCode} key...")
            byteStr = KeyPressedMessage(keyCode).toBytes()
            if len(byteStr) > UDP_MAX_SIZE:
                raise Exception("Message too long for our UDP buffers.")
            clientSocket.sendto(byteStr, serverAddr)


messageClient()
