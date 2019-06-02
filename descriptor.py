import uuid
import threading
from message import Message


class Descriptor(threading.Thread):
    def __init__(self, nome, ip, porta, socket_connection, broadcast):
        super().__init__()
        self.id = uuid.uuid4()
        self.nome = nome
        self.ip = ip
        self.porta = porta
        self.connection = socket_connection
        self.active = True
        self.broadcast = broadcast

    def broadcast_from_outside(self, origin_id, message):
        if self.id != origin_id and self.active:
            self.connection.send(message.encode().encode('utf-8'))

    def run(self) -> None:
        welcome_data = f"{self.nome} entrou na sala..."
        welcome_message = Message(data=welcome_data)
        print(welcome_message.data)
        self.broadcast(self.id, welcome_message)

        while True:
            try:
                payload = self.connection.recv(1024)
                payload = payload.decode('utf-8')

                # decodes a message from received payload
                message = Message()
                message.decode(payload)

                if message.command == "nome()":
                    name_announcement = f"{self.nome} agora é {message.data}"
                    name_message = Message(data=name_announcement)
                    self.nome = message.data
                    self.broadcast(self.id, name_message)
                    continue

                # broadcast received message to other connections
                # and print at server level
                if len(self.nome) == 0:
                    self.connection.send("You don't have a name yet. Message not sent".encode('utf-8'))
                else:
                    broadcast_message = f"{self.nome} says: {message.data}"
                    message = Message(data=broadcast_message)
                    print(broadcast_message)
                    self.broadcast(self.id, message)

            except ConnectionResetError:
                exit_announcement = f"{self.nome} saiu..."
                print(exit_announcement)
                exit_message = Message(data=exit_announcement)
                self.broadcast(self.id, exit_message)
                self.active = False
                break
