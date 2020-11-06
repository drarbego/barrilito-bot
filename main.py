import falcon
import json
import requests
import re

from os import environ

from clients.slack_client import SlackClient
from controller import Controller 
from messages.slack_message import SlackMessage


SLACK_API_TOKEN = environ.get('SLACK_API_TOKEN')
BOT_TOKEN = environ.get('BOT_TOKEN')
BICI_STATIONS_URL = 'https://guadalajara-mx.publicbikesystem.net/ube/gbfs/v1/en/station_status'
OIL_PRICES_URL = 'https://datasource.kapsarc.org/api/records/1.0/search/?dataset=opec-crude-oil-price&q=&rows=1&facet=date&refine.date=2020'

slack_client = SlackClient(SLACK_API_TOKEN, BOT_TOKEN)
controller = Controller(slack_client)


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

def check_oil():
    response = requests.get(
        OIL_PRICES_URL,
    )

    json_response = response.json()
    print(json_response)

    results = json_response.get('records', [])
    
    total = 0
    if results:
        total = results[0].get('fields', {}).get('value', 0)

    return 'El precio del barril al día de hoy es de {total} USD'.format(total=total)


def check_bicis(station_id='192'):
    response = requests.get(
        BICI_STATIONS_URL,
    )

    json_response = response.json()
    stations = json_response.get('data', {}).get('stations', [])
    station_count = 0

    found_station = {}
    for station in stations:
        if station.get('station_id') == station_id:
            found_station = station
            break

    return 'Hay {bikes}/{docks} bici(s) disponible(s)'.format(
        bikes=str(found_station.get('num_bikes_available')),
        docks=str(found_station.get('num_docks_available')),
    )

def parse_message(message):
    return re.sub('<@[\w]+>', '', message)


class MessageListenerResource:
    def __init__(self, controller):
        self.controller = controller

    def on_get(self, req, resp):
        """Handles GET requests"""
        resp.status = falcon.HTTP_200  # This is the default status
        resp.body = json.dumps({
            "status": "ok"
        })

    def on_post(self, req, res):
        body = json.load(req.bounded_stream)

        received_message = SlackMessage(body)
        print(received_message)

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

        self.controller.on_message_received(received_message)
        if 'bicis' in parsed_text:
            message = check_bicis()
            respond(channel_id, message)
        elif 'cuestas' in parsed_text:
            message = check_oil()
            respond(channel_id, message)
        else:
            respond(channel_id)

        res.status = falcon.HTTP_200


# falcon.API instances are callable WSGI apps
app = falcon.API()

# Resources are represented by long-lived class instances
message_listener_resource = MessageListenerResource(controller)

# things will handle all requests to the '/things' URL path
app.add_route('/message', message_listener_resource)
