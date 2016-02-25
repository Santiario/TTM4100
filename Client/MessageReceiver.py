# -*- coding: utf-8 -*-
from threading import Thread


class MessageReceiver(Thread):
    """
    This is the message receiver class. The class inherits Thread, something that
    is necessary to make the MessageReceiver start a new thread, and it allows
    the chat client to both send and receive messages at the same time
    """

    def __init__(self, client, connection):
        super(MessageReceiver, self).__init__()
        """
        This method is executed when creating a new MessageReceiver object
        """

        # Flag to run thread as a deamon. A deamon is a process that runs in the background.
        self.daemon = True


        # TODO: Finish initialization of MessageReceiver
        self.client = client
        self.connection = connection
        self.start()

    def run(self):
        # TODO: Make MessageReceiver receive and handle payloads
        while True:
            received_message = self.connection.recv(4096)
            print received_message

