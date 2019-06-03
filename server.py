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
    for cli in list(filter(lambda c: not c.in_private, clients)):
        cli.send_message_from_outside(origin_id, message)


def send_to_client(origin_id, dest_id, message):
    for c in clients:
        if c.id == dest_id:
            c.send_message_from_outside(origin_id, message)
            break


def get_connected_clients():
    return list(filter(lambda c: c.active, clients))


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
    client = Descriptor(nickname, addr[0], addr[1], connectionSocket,
                        get_connected_clients, global_sender, send_to_client)

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
