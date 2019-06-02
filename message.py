class Message:
    def __init__(self, command="", data=""):
        if len(command) > 8:
            raise Exception("Command is invalid.")

        # define class properties
        self.recipient = ""
        self.command = command
        self.data = data[:80] if len(data) > 80 else data
        self.size = len(self.data)

    def encode(self, public=True, recipient=""):
        if public:
            self.recipient = "EVERYONE"
        else:
            self.recipient = recipient

        return str(self.size) + "\t" + self.recipient + "\t" + self.command + "\t" + self.data

    def decode(self, payload):
        fields = str(payload).split('\t', maxsplit=3)

        self.size = fields[0]
        self.recipient = fields[1]
        self.command = fields[2]
        self.data = fields[3]
