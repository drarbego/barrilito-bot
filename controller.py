from datetime import datetime

from semantic_analyzer import SemanticAnalyzer


class Controller:
    def __init__(self, client):
        self.client = client
        self.semantic_analyzer = SemanticAnalyzer()

    def on_message_received(self, message):
        print(f"Message received {message} at {str(datetime.now())}")
        response_message = self.semantic_analyzer.get_response(message.get_content())

        if message.get_event_subtype() == 'bot_message':
            return

        if message.get_event_type() != 'app_mention':
            return

        channel_id = message.get_channel_id()
        self.client.send_message(channel_id, response_message)
