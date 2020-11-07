import requests

SLACK_DOMAIN = 'https://slack.com'

class SlackClient:
    def __init__(self, slack_api_token, bot_token):
        self._slack_api_token = slack_api_token
        self._bot_token = bot_token

    def send_message(self, channel_id, text):
        url = f"{SLACK_DOMAIN}/api/chat.postMessage"
        headers = {
        'Authorization': f'Bearer {self._slack_api_token}',
        'Content-Type': 'application/json;charset=UTF-8',
        }
        payload = {
            'text': text,
            'channel': channel_id, 
        }

        requests.post(url, headers=headers, json=payload)
