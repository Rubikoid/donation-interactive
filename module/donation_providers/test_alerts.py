from ..classes import Provider, Donation, UnknownMessage
import asyncio
from aiohttp import web
import json
import sys


class TestingProvider(Provider):
    """Testing provider, which creates simple web interface for sending donates with some price

    Config:
    ---
    host: str = "127.0.0.1"
        Default host for server
    port: int = 9999
        Default port for server
    """

    config_vars = Provider.config_vars.copy()
    config_vars.update({
        'type': 'TestingProvider',
        'name': 'TestingProvider_name',

        "host": "127.0.0.1",
        "port": 9999
    })

    secret_vars = Provider.secret_vars.copy()
    secret_vars.update({})

    def __init__(self, donation_callback):
        super().__init__(donation_callback)
        self.app = web.Application()
        self.app.add_routes([
            web.get('/', self.index),
            web.get("/donate", self.test_donate)
        ])

    async def index(self, data):
        return web.Response(text="<h2>Test donation</h2><form action='/donate'><input name='size'/><button type='submit'>ok</button></form>", content_type='text/html')

    async def test_donate(self, data: web.Request):
        # update_config()
        print(f"New test donation amount: {data.query['size']}", file=sys.stderr)

        donation = Donation({
            "additional_data": "{}",
            "amount_main": int(data.query["size"]),
            "username": "FAKE"
        })

        await self.callback(donation)
        # asyncio.get_running_loop().create_task(self.callback(donation))
        # asyncio.get_running_loop().create_task()
        return web.HTTPTemporaryRedirect("/")

    async def connect(self):
        loop = asyncio.get_event_loop()
        host = self.config_vars["host"]
        port = self.config_vars["port"]
        self.runner = web.AppRunner(self.app)
        await self.runner.setup()
        site = web.TCPSite(self.runner, host, port)
        await site.start()
        print(f"aiohttp prepared")

    async def disconnect(self):
        print("Stopping aiohttp")
        await self.runner.cleanup()
