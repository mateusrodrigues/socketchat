import threading
from socket import *
from message import Message
from clientDescriptor import Descriptor

# VARIABLES
serverName = ''                              # server IP (blank)
serverPort = 65000                           # server port
serverSocket = socket(AF_INET, SOCK_STREAM)  # TCP socket creation
serverSocket.bind((serverName, serverPort))  # binding IP and server port
serverSocket.listen(1)                       # socket ready to listen to connections

clients = {}                                 # client definitions dictionary

# print server status
print('Chatroom created and awaiting for connections on port %d ...' % serverPort)

while True:


    connectionSocket, addr = serverSocket.accept()  # aceita as conexoes dos clientes
    sentence = connectionSocket.recv(1024) # recebe dados do cliente
    sentence = sentence.decode('utf-8')
    capitalizedSentence = sentence.upper() # converte em letras maiusculas
    print ('Cliente %s enviou: %s, transformando em: %s' % (addr, sentence, capitalizedSentence))
    connectionSocket.send(capitalizedSentence.encode('utf-8')) # envia para o cliente o texto transformado
    connectionSocket.close() # encerra o socket com o cliente

serverSocket.close() # encerra o socket do servidor
