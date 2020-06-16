from ..classes import Provider, Donation, UnknownMessage
from copy import deepcopy
from socketio import AsyncClient
import json
import sys


class DonationAlertsProvider(Provider):
    """DonationAlerts provider. Handles new donations on donation alerts

    Config:
    ---
    server: str = "https://socket11.donationalerts.ru/socket.io"
        Default donation alerts server.

    Secrets:
    ---
    donationalerts_token: str = ""
        Token for donation alerts
    """

    config_vars = Provider.config_vars.copy()
    config_vars.update({
        'type': 'DonationAlertsProvider',
        'name': 'DonationAlertsProvider_name',

        "server": "https://socket11.donationalerts.ru/socket.io",
    })

    secret_vars = Provider.secret_vars.copy()
    secret_vars.update({
        "donationalerts_token": ""
    })

    def __init__(self, donation_callback):
        super().__init__(donation_callback)
        self.sio_da = AsyncClient()
        self.sio_da.on("connect", handler=self.on_connect)
        self.sio_da.on("donation", handler=self.on_message)

    async def on_connect(self, *args):
        print(f"Connect event to donations alerts server {args}")

    async def on_message(self, data_str):
        # update_config()
        data = json.loads(data_str)
        print(data, file=sys.stderr)
        if str(data["alert_type"]) == "1":
            donation = Donation(data)
            await self.callback(donation)
        else:
            print(f"Unknown message comes from donation alerts{UnknownMessage(data)}")

    async def connect(self):
        await self.sio_da.connect(self.config_vars["server"])
        await self.sio_da.emit('add-user', {'token': self.secret_vars["donationalerts_token"], 'type': 'alert_widget'})
        print(f"Connected to donations alerts server {self.config_vars['server']}")

    async def disconnect(self):
        print("Stopping donation alerts")
        await self.sio_da.disconnect()
