from ..classes import Provider, Donation, UnknownMessage
from copy import deepcopy
import socketio
import json
import sys


class DonationAlertsProvider(Provider):
    name = "DonationAlertsProvider"

    config_vars = Provider.config_vars.copy()
    config_vars.update({
        "server": "https://socket11.donationalerts.ru/socket.io",
    })

    secret_vars = Provider.secret_vars.copy()
    secret_vars.update({
        "donationalerts_token": ""
    })

    def __init__(self, action_callback):
        super().__init__(action_callback)
        self.sio_da = socketio.Client()
        self.sio_da.on("connect", handler=self.on_connect)
        self.sio_da.on("donation", handler=self.on_message)

    def on_connect(self, *args):
        print(f"Connect event to donations alerts server {args}")

    def on_message(self, data_str):
        # update_config()
        data = json.loads(data_str)
        print(data, file=sys.stderr)
        if str(data["alert_type"]) == "1":
            donation = Donation(data)
            self.callback(donation)
            # if not gtasa.universal_handler(Donation(data).amount):
            #    for k, price in CONFIG["price_handlers"].items():
            #        if Donation(data).amount == price:
            #           eval(f"{k}()")
            pass
        else:
            print(UnknownMessage(data))
            pass

    def connect(self):
        self.sio_da.connect(self.config_vars["server"])
        self.sio_da.emit('add-user', {'token': self.secret_vars["donationalerts_token"], 'type': 'alert_widget'})
        print(f"Connected to donations alerts server {self.config_vars['server']}")
        # self.sio_da.wait()
        print(f"Waited?")

    def disconnect(self):
        self.sio_da.disconnect()
