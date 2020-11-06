from semantic_analyzer import SemanticAnalyzer


class Controller:
    def __init__(self, client):
        self.client = client
        self.semantic_analyzer = SemanticAnalyzer()

    def on_message_received(self, message):
        response_message = self.semantic_analyzer.get_response(message.get_content())

        channel_id = message.get_channel_id()
        self.client.send_message(channel_id, response_message)
