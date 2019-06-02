from socket import *
from message import Message

# VARIABLES
serverName = 'localhost'                        # server IP
serverPort = 65000                              # server port
clientSocket = socket(AF_INET, SOCK_STREAM)     # TCP socket creation
clientSocket.connect((serverName, serverPort))  # TCP socket connection

# CLIENT
while True:
    sentence = input('> ')
    encodedCommand = ""

    # command parser
    if sentence.startswith("sair()"):
        break
    elif sentence.startswith("nome("):
        endOfParenthesis = sentence.find(')')
        name = sentence[5:endOfParenthesis]
        print(name)
    elif sentence.startswith("lista()"):
        message = Message("lista()", "")
        encodedCommand = message.encode()
    else:
        # this is a regular message
        message = Message("", sentence)
        encodedCommand = message.encode()

    clientSocket.send(encodedCommand.encode('utf-8'))
    modifiedSentence = clientSocket.recv(1024)  # recebe do servidor a resposta
    print('O servidor (\'%s\', %d) respondeu com: %s' % (serverName, serverPort, modifiedSentence.decode('utf-8')))

clientSocket.close()  # close server socket connection
