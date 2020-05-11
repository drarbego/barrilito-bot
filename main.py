import falcon
import json
import requests
import re

from os import environ

API_TOKEN = environ.get('SLACK_API_TOKEN')
BOT_TOKEN = environ.get('BOT_TOKEN')
BICI_STATIONS_URL = 'https://guadalajara-mx.publicbikesystem.net/ube/gbfs/v1/en/station_information'

def respond(channel_id, message='YIII'):
    headers = {
      'Authorization': f'Bearer {API_TOKEN}',
      'Content-Type': 'application/json;charset=UTF-8',
    }
    response = requests.post(
        'https://slack.com/api/chat.postMessage',
        headers=headers,
        json={
            'text': message,
            'channel': channel_id, 
        }
    )
    print('channel ', channel_id)
    print('response ', response)
    print('response.json() ', response.json())

def check_bicis():
    response = requests.get(
        BICI_STATIONS_URL,
    )

    json_response = response.json()
    stations_lists = json_response.get('data', {}).get('stations', [])
    station_count = 0

    for stations in stations_lists:
        station_count += len(stations)

    return str(len(station_count))

def parse_message(message):
    return re.sub('<@[\w]+>', '', message)


class MessageResource:
    def on_get(self, req, resp):
        """Handles GET requests"""
        resp.status = falcon.HTTP_200  # This is the default status
        resp.body = json.dumps({
            "status": "ok"
        })

    def on_post(self, req, res):
        body = json.load(req.bounded_stream)
        print('body ', body)

        if 'challenge' in body:
            res.status = falcon.HTTP_200
            res.body = json.dumps({
                'challenge': body['challenge']
            })
            return

        if 'token' not in body or body['token'] != BOT_TOKEN:
            res.status = falcon.HTTP_401
            return

        event = body.get('event', {})

        event_type = event.get('type')
        event_subtype = event.get('subtype')
        message_text = event.get('text')
        channel_id = event.get('channel')

        if event_subtype == 'bot_message':
            res.status = falcon.HTTP_200
            return

        if event_type != 'app_mention':
            return

        parsed_text = parse_message(message_text)
        if 'bicis' in parsed_text:
            stations_count = check_bicis()
            respond(channel_id, stations_count)
        else:
            respond(channel_id)

        res.status = falcon.HTTP_200


# falcon.API instances are callable WSGI apps
app = falcon.API()

# Resources are represented by long-lived class instances
message = MessageResource()

# things will handle all requests to the '/things' URL path
app.add_route('/message', message)
