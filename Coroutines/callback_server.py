#!/usr/bin/python3

mport asyncio
import sys

class ChatServer:

    class ChatProtocol(asyncio.Protocol):

        def __init__(self, chat_server):
            self.chat_server = chat_server
            self.username = None
            self.buffer = ""
            self.transport = None

        def connection_made(self, transport):
            # Callback: when connection is established, pass in transport.
            self.transport = transport
            welcome = "Welcome to " + self.chat_server.server_name
            self.send_msg(welcome + "\nUsername: ")

        def data_received(self, data):
            # Callback: whenever data is received - not necessarily buffered.
            data = data.decode("utf-8")
            self.buffer += data
            self.handle_lines()

        def connection_lost(self, exc):
            # Callback: client disconnected.
            if self.username is not None:
                self.chat_server.remove_user(self.username)

        def send_msg(self, msg):
            self.transport.write(msg.encode("utf-8"))

        def handle_lines(self):
            while "\n" in self.buffer:
                line, self.buffer = self.buffer.split("\n", 1)
                if self.username is None:
                    if self.chat_server.add_user(line, self.transport):
                        self.username = line
                    else:
                        self.send_msg("Sorry, that name is taken\nUsername: ")
                else:
                    self.chat_server.user_message(self.username, line)


    def __init__(self, server_name, port, loop):
        self.server_name = server_name
        self.connections = {}
        self.server = loop.create_server(
                lambda: self.ChatProtocol(self),
                host="", port=port)

    def broadcast(self, message):
        for transport in self.connections.values():
            transport.write((message + "\n").encode("utf-8"))

    def add_user(self, username, transport):
        if username in self.connections:
            return False
        self.connections[username] = transport
        self.broadcast("User " + username + " joined the room")
        return True

    def remove_user(self, username):
        del self.connections[username]
        self.broadcast("User " + username + " left the room")

    def get_users(self):
        return self.connections.keys()

    def user_message(self, username, msg):
        self.broadcast(username + ": " + msg)


def main(argv):

    loop = asyncio.get_event_loop()
    chat_server = ChatServer("Test Server", 4455, loop)
    loop.run_until_complete(chat_server.server)
    try:
        loop.run_forever()
    finally:
        loop.close()


if __name__ == "__main__":
sys.exit(main(sys.argv))
