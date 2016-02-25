import json
import math

class MessageParser():
    def __init__(self):

        self.possible_responses = {
            'error': self.parse_error,
            'info': self.parse_info,
            'message': self.parse_response,
            'history': self.parse_history
        }

    def parse(self, payload):
        payload = json.loads(payload)  # decode the JSON object

        if payload['response'] in self.possible_responses:
            return self.possible_responses[payload['response']](payload)
        else:
            pass

    def parse_error(self, payload):
        return payload['content']

    def parse_info(self, payload):
        return payload['content']

    def parse_response(self, payload):
        return payload['sender'] + ": " + payload['content']

    def parse_history(self, payload):
        return

    # Include more methods for handling the different responses... 
