import falcon
import json


class MessageResource:
    def on_get(self, req, resp):
        """Handles GET requests"""
        resp.status = falcon.HTTP_200  # This is the default status
        resp.body = json.dumps({
            "status": "ok"
        })

# falcon.API instances are callable WSGI apps
app = falcon.API()

# Resources are represented by long-lived class instances
message = MessageResource()

# things will handle all requests to the '/things' URL path
app.add_route('/message', message)
