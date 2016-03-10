# -*- coding: utf-8 -*-
import SocketServer
import json
import time
import re

"""
Variables and functions that must be used by all the ClientHandler objects
must be written here (e.g. a dictionary for connected clients)
"""

connected_clients = {}  # The users are added when they successfully log in on the format client:'username'
history = []
help_text = "login <username> - log in with the given username \nlogout - log out \n<message> - send message \n\
names - list users in chat\nhelp - view help text"


class ClientHandler(SocketServer.BaseRequestHandler):
    """
    This is the ClientHandler class. Every time a new client connects to the
    server, a new ClientHandler object will be created. This class represents
    only connected clients, and not the server itself. If you want to write
    logic for the server, you must write it outside this class
    """
    def __init__(self, request, client_address, tcp_server):
        SocketServer.BaseRequestHandler.__init__(self, request, client_address, tcp_server)

    def handle(self):
        """
        This method handles the connection between a client and the server.
        """

        # Loop that listens for messages from the client
        while True:
            try:
                received_json = self.request.recv(4096)
                message = json.loads(received_json)  # Decodes the JSON object

                if message['request'] == 'login' and self not in connected_clients:
                    user_taken = False
                    for username in connected_clients.values():
                        if message['content'] == username:
                            user_taken = True

                    if user_taken:
                        self.request.sendall(self.make_payload('SERVER', 'error', 'Username taken.'))

                    elif not self.valid_username(message['content']):
                        self.request.sendall(self.make_payload('SERVER', 'error', 'Invalid username'))

                    else:  # The username is valid and not taken
                        connected_clients[self] = message['content']  # Adds the client to the global connected_clients
                        self.request.sendall(self.make_payload('SERVER', 'info', 'Login successful.'))
                        print message['content'] + " connected to server."
                        self.send_to_all_other_clients(self.make_payload('SERVER', 'message', message['content'] +
                                                                         " joined the chatroom"))
                        if history:
                            self.request.sendall(self.make_payload('SERVER', 'history', history))

                elif message['request'] == 'logout' and self in connected_clients:
                    print connected_clients[self] + ' left the server'
                    connected_clients.pop(self)
                    self.request.close()
                    break

                elif message['request'] == 'msg' and self in connected_clients:
                    payload = self.make_payload(connected_clients[self], 'message', message['content'])
                    history.append(payload)
                    self.send_to_all_other_clients(payload)

                elif message['request'] == 'names' and self in connected_clients:
                    self.request.sendall(self.make_payload('SERVER', 'info', connected_clients.values()))

                elif message['request'] == 'help':
                    self.request.sendall(self.make_payload('SERVER', 'info', help_text))

                else:
                    self.request.sendall(self.make_payload('SERVER', 'error', 'Not a valid argument'))
            except ValueError:
                if self in connected_clients.keys():
                    print connected_clients[self] + ' left the server'
                    connected_clients.pop(self)
                    self.request.close()
                    break

    def send_to_all_other_clients(self, payload):
        for client in connected_clients:
            if client == self:
                continue
            client.request.sendall(payload)

    @staticmethod
    def make_payload(sender, response, content):
        payload = {
                     'timestamp': time.time(),
                     'sender': sender,
                     'response': response,
                     'content': content
                 }
        return json.dumps(payload)

    @staticmethod
    def valid_username(username):
        return re.match('[a-zA-Z0-9]+', username)


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    """
    This class is present so that each client connected will be ran as a own
    thread. In that way, all clients will be served by the server.

    No alterations are necessary
    """
    allow_reuse_address = True

if __name__ == "__main__":
    """
    This is the main method and is executed when you type "python Server.py"
    in your terminal.

    No alterations are necessary
    """
    HOST, PORT = '0.0.0.0', 9998
    print 'Server running...'

    # Set up and initiate the TCP server
    server = ThreadedTCPServer((HOST, PORT), ClientHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print 'Server halted.'