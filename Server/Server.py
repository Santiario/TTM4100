# -*- coding: utf-8 -*-
import SocketServer
import json
import time
"""
Variables and functions that must be used by all the ClientHandler objects
must be written here (e.g. a dictionary for connected clients)
"""

connected_clients = {}


class ClientHandler(SocketServer.BaseRequestHandler):
    """
    This is the ClientHandler class. Every time a new client connects to the
    server, a new ClientHandler object will be created. This class represents
    only connected clients, and not the server itself. If you want to write
    logic for the server, you must write it outside this class
    """

    def handle(self):
        """
        This method handles the connection between a client and the server.
        """
        self.ip = self.client_address[0]
        self.port = self.client_address[1]
        self.connection = self.request




        # Loop that listens for messages from the client
        while True:
            received_string = self.connection.recv(4096)
            message = json.loads(received_string)
            request = message['request']
            if request == 'login':
                user_taken = False
                for username in connected_clients.values():
                    if message['content'] == username:
                        user_taken = True
                if user_taken:
                    payload = {
                         'timestamp': time.time(),
                         'sender': "SERVER",
                         'response': 'error',
                         'content': 'Username taken.\n'
                     }
                    self.connection.sendall(json.dumps(payload))
                else:
                    connected_clients[self] = message['content']
                    payload = {
                         'timestamp': time.time(),
                         'sender': "SERVER",
                         'response': 'info',
                         'content': 'Login successful.\n'
                     }
                    self.connection.sendall(json.dumps(payload))
                    print message['content'] + " connected to server."

                    login_alert = {
                         'timestamp': time.time(),
                         'sender': "SERVER",
                         'response': 'message',
                         'content': message['content'] + " joined the chatroom"
                     }
                    json_object = json.dumps(login_alert)
                    for client in connected_clients:
                        if client == self:
                            continue
                        client.connection.sendall(json_object)
            elif request == 'logout':
                print connected_clients[self] + ' left the server'
                connected_clients.pop(self)
                self.connection.close()
                break
            elif request == 'msg':
                payload = {
                     'timestamp': time.time(),
                     'sender': connected_clients[self],
                     'response': 'message',
                     'content': message['content']
                 }
                json_object = json.dumps(payload)
                for client in connected_clients:
                    if client == self:
                        continue
                    client.connection.sendall(json_object)
            elif request == 'names':
                for client in connected_clients:
                    client.connection.sendall(connected_clients.values())
            elif request == 'help':
                self.connection.sendall("Velkommen til Chatteklient 2000.\nDette er en ny feature")
            else:
                self.connection.sendall("Not a valid message")



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
    HOST, PORT = 'localhost', 9998
    print 'Server running...'

    # Set up and initiate the TCP server
    server = ThreadedTCPServer((HOST, PORT), ClientHandler)
    server.serve_forever()
