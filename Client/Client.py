# -*- coding: utf-8 -*-
import socket
import json
from MessageReceiver import MessageReceiver
from MessageParser import MessageParser


class Client:
    """
    This is the chat client class
    """
    def __init__(self, host, server_port):
        """
        This method is run when creating a new Client object
        """

        self.host = host
        self.server_port = server_port

        # Set up the socket connection to the server
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect()

        # Instantiate a MessageReciever to handle recieved messages in parallell
        # MessageReceiver calls receive_message to print the message to the console
        self.parser = MessageParser()
        self.receiver = MessageReceiver(self, self.connection, self.parser)
        self.run()

    def connect(self):
        self.connection.connect((self.host, self.server_port))
        self.logged_in = False
        while not self.logged_in:
            username = raw_input('Please enter username: ')
            self.login(username)
            response = json.loads(self.connection.recv(4096))
            if response['response'] == 'info':
                self.logged_in = True
                print response['content']
            else:
                print response['response'] + ": " + response['content']


    def run(self):
        # Code that runs in a loop until the user exits
        while True:
            command = raw_input()
            if command.lower() == 'logout' or \
                command.lower() == 'names' or \
                command.lower() == 'help':
                payload = {
                    'request': command.lower(),
                    'content': None
                }
                self.connection.sendall(json.dumps(payload))
                if command.lower() == 'logout':
                    self.disconnect()
                    break
            else:
                payload = {
                    'request': 'msg',
                    'content': command
                }
                self.connection.sendall(json.dumps(payload))
        print "Chatroom disconnected."

    def login(self, username):
        payload = {
            'request': 'login',
            'content': username
        }
        payload = json.dumps(payload)
        self.connection.sendall(payload)

    def disconnect(self):
        self.connection.close()

    def receive_message(self, message):
        pass
        # This method is not supposed to be used?

    def send_payload(self, data):
        # TODO: Handle sending of a payload

        self.connection.send(data)
        print "Payload sent"
        pass
        
    # More methods may be needed!


if __name__ == '__main__':
    """
    This is the main method and is executed when you type "python Client.py"
    in your terminal.

    No alterations are necessary
    """
    client = Client('localhost', 9998)
