import falcon
import json
import requests
import re

from os import environ

from clients.slack_client import SlackClient
from controller import Controller 
from messages.message_builder import MessageBuilder, UnauthorizedSourceError
from messages.slack_message import SlackMessage


SLACK_API_TOKEN = environ.get('SLACK_API_TOKEN')
BOT_TOKEN = environ.get('BOT_TOKEN')

slack_client = SlackClient(SLACK_API_TOKEN, BOT_TOKEN)
controller = Controller(slack_client)


class MessageListenerResource:
    def __init__(self, controller):
        self.controller = controller

    def on_post(self, req, res):
        body = json.load(req.bounded_stream)

        if 'challenge' in body:
            res.status = falcon.HTTP_200
            res.body = json.dumps({
                'challenge': body['challenge']
            })
            return

        try:
            slack_message = MessageBuilder.build_slack_message(body)
            print(slack_message)

            slack_controller = Controller(slack_client)
            slack_controller.on_message_received(slack_message)
        except UnauthorizedSourceError:
            res.status = falcon.HTTP_401
            return

        res.status = falcon.HTTP_200


app = falcon.API()
message_listener_resource = MessageListenerResource(controller)

app.add_route('/message', message_listener_resource)
