import json


class MessageParser:
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

    @staticmethod
    def parse_error(payload):
        return payload['content']

    @staticmethod
    def parse_info(payload):
        return payload['content']

    @staticmethod
    def parse_response(payload):
        return payload['sender'] + ": " + payload['content']

    @staticmethod
    def parse_history(payload):
        messages = ''
        for jsonobj in payload['content']:
            message = json.loads(jsonobj)
            messages += message['sender'] + ": " + message['content'] + '\n'
        return messages[:-1]
