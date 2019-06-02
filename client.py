import threading
from socket import *
from message import Message

# VARIABLES
serverName = 'localhost'                        # server IP
serverPort = 65000                              # server port
clientSocket = socket(AF_INET, SOCK_STREAM)     # TCP socket creation
clientSocket.connect((serverName, serverPort))  # TCP socket connection


def receive_message():
    while True:
        received_payload = clientSocket.recv(1024)
        received_payload = received_payload.decode('utf-8')

        received_message = Message()
        received_message.decode(received_payload)
        print(received_message.data)


messageReceiver = threading.Thread(target=receive_message, daemon=True)
messageReceiver.start()

# CLIENT
while True:
    sentence = input()
    encodedCommand = ""

    # command parser
    if sentence.startswith("sair()"):
        break
    elif sentence.startswith("nome("):
        endOfParenthesis = sentence.find(')')
        name = sentence[5:endOfParenthesis]
        message = Message("nome()", name)
        encodedCommand = message.encode()
    elif sentence.startswith("lista()"):
        message = Message("lista()", "")
        encodedCommand = message.encode()
    else:
        # this is a regular message
        message = Message("", sentence)
        encodedCommand = message.encode()

    clientSocket.send(encodedCommand.encode('utf-8'))

clientSocket.close()  # close server socket connection
