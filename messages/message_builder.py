from messages.slack_message import SlackMessage


class UnauthorizedSourceError(Exception):
    def __init__(self, raw_message):
        self.raw_message = raw_message

    def __str__(self):
        return f"An unauthorized source sent: {self.raw_message}"


class MessageBuilder:
    @staticmethod
    def build_slack_message(bot_token, raw_message):
        if bot_token != raw_message.get("token"):
            raise UnauthorizedSourceError(raw_message)

        event = raw_message.get("event", {})

        event_type = event.get("type")
        event_subtype = event.get("subtype")
        content = re.sub("<@[\w]+>", "", event.get("text", ""))
        channel_id = event.get("channel")

        return SlackMessage(channel_id, content, event_type, event_subtype)
