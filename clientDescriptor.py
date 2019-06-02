import threading


class Descriptor(threading.Thread):
    def __init__(self):
        self.nome = ""
        self.ip = ""
        self.porta = 0

    def run(self) -> None:
        print("New thread called")

