from socket import *
from descriptor import Descriptor
from message import Message

# VARIABLES
serverName = ''                              # server IP (blank)
serverPort = 65000                           # server port
serverSocket = socket(AF_INET, SOCK_STREAM)  # TCP socket creation
serverSocket.bind((serverName, serverPort))  # binding IP and server port
serverSocket.listen(1)                       # socket ready to listen to connections

clients = []                                 # client definitions dictionary

# print server status
print('Chatroom created and awaiting for connections on port %d ...' % serverPort)


def global_sender(origin_id, message):
    for c in clients:
        c.broadcast_from_outside(origin_id, message)


while True:
    # accepts a new connection into the socket server
    connectionSocket, addr = serverSocket.accept()

    # ask for a nickname
    nickname_message = Message(data="Please, type in a nickname for you: ")
    connectionSocket.send(nickname_message.encode().encode('utf-8'))

    # wait for nickname
    nickname_payload = connectionSocket.recv(1024).decode('utf-8')
    nickname_message = Message()
    nickname_message.decode(nickname_payload)
    nickname = nickname_message.data

    # initializes the client descriptor for its thread
    client = Descriptor(nickname, addr[0], addr[1], connectionSocket, global_sender)

    # starts the client thread
    clients.append(client)
    client.start()

#     sentence = connectionSocket.recv(1024) # recebe dados do cliente
#     sentence = sentence.decode('utf-8')
#     capitalizedSentence = sentence.upper() # converte em letras maiusculas
#     print ('Cliente %s enviou: %s, transformando em: %s' % (addr, sentence, capitalizedSentence))
#     connectionSocket.send(capitalizedSentence.encode('utf-8')) # envia para o cliente o texto transformado
#     connectionSocket.close() # encerra o socket com o cliente
#
# serverSocket.close()  # encerra o socket do servidor
