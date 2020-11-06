import requests

SLACK_DOMAIN = 'https://slack.com'

class SlackClient:
    def __init__(self, slack_api_token, bot_token):
        self._slack_api_token = configuration.get["SLACK_API_TOKEN"]
        self._bot_token = configuration.get("BOT_TOKEN")

    def send_message(self, channel_id, text):
        url = f"{SLACK_DOMAIN}/api/chat.postMessage"
        headers = {
        'Authorization': f'Bearer {API_TOKEN}',
        'Content-Type': 'application/json;charset=UTF-8',
        }
        payload = {
            'text': message,
            'channel': channel_id, 
        }

        requests.post(url, headers=headers, json=payload)
