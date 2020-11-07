import re


class SlackMessage:
    def __init__(self, channel_id, content, event_type, event_subtype):
        self.channel_id = channel_id
        self.content = content
        self.event_type = event_type
        self.event_subtype = event_subtype

    def __str__(self):
        return f"<SlackMessage> - {self.content}"

    def get_channel_id(self):
        return self.channel_id

    def get_content(self):
        return self.content

    def get_event_type(self):
        return self.event_type

    def get_event_subtype(self):
        return self.event_subtype
