import uuid
import threading
from message import Message


class Descriptor(threading.Thread):
    def __init__(self, name, ip, port, socket_connection, get_connected_clients, broadcast_to_others, send_to_client):
        super().__init__()
        self.id = uuid.uuid4()
        self.name = name
        self.ip = ip
        self.port = port
        self.connection = socket_connection
        self.active = True
        self.in_private = False
        self.private_dest_id = uuid.uuid4()
        self.get_connected_clients = get_connected_clients
        self.broadcast_to_others = broadcast_to_others
        self.send_to_client = send_to_client

    def send_message_from_outside(self, origin_id, message):
        if self.id != origin_id and self.active:
            self.connection.send(message.encode().encode('utf-8'))

    def run(self) -> None:
        welcome_data = f"{self.name} entrou na sala..."
        welcome_message = Message(data=welcome_data)
        print(welcome_message.data)
        self.broadcast_to_others(self.id, welcome_message)

        while True:
            try:
                payload = self.connection.recv(1024)
                payload = payload.decode('utf-8')

                # decodes a message from received payload
                message = Message()
                message.decode(payload)

                if message.command == "nome()":
                    name_announcement = f"{self.name} agora é {message.data}"
                    name_message = Message(data=name_announcement)
                    self.name = message.data
                    self.broadcast_to_others(self.id, name_message)
                    continue
                elif message.command == "lista()":
                    response = ""
                    for client in self.get_connected_clients():
                        if client.in_private:
                            response += f"<{client.name}(privado), {client.ip}, {client.port}>\n"
                        else:
                            response += f"<{client.name}, {client.ip}, {client.port}>\n"
                    response_message = Message(data=response)
                    self.connection.send(response_message.encode(public=False, recipient=self.name).encode('utf-8'))
                    continue
                elif message.command == "privado()":
                    self.in_private = True
                    clients = self.get_connected_clients()
                    # get the client this person wants to connect to
                    for c in clients:
                        if c.name == message.data:
                            self.in_private = True
                            c.in_private = True
                            self.private_dest_id = c.id
                            c.private_dest_id = self.id
                            break
                    continue

                # broadcast received message to other connections
                # and print at server level
                if len(self.name) == 0:
                    self.connection.send("You don't have a name yet. Message not sent".encode('utf-8'))
                else:
                    message_content = f"{self.name} says: {message.data}"
                    message = Message(data=message_content)
                    if self.in_private:
                        self.send_to_client(self.id, self.private_dest_id, message)
                    else:
                        print(message_content)
                        self.broadcast_to_others(self.id, message)

            except ConnectionResetError:
                exit_announcement = f"{self.name} saiu..."
                print(exit_announcement)
                exit_message = Message(data=exit_announcement)
                self.broadcast_to_others(self.id, exit_message)
                self.active = False
                break
