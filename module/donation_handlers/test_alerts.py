from ..classes import Provider, Donation, UnknownMessage
import asyncio
from aiohttp import web
import json
import sys


class TestingProvider(Provider):
    name = "TestingProvider"

    config_vars = Provider.config_vars.copy()
    config_vars.update({
        "host": "127.0.0.1",
        "port": 9999
    })

    secret_vars = Provider.secret_vars.copy()
    secret_vars.update({})

    def __init__(self, action_callback):
        super().__init__(action_callback)
        self.app = web.Application()
        self.app.add_routes([
            web.get('/', self.index),
            web.get("/donate", self.test_donate)
        ])

    async def index(self, data):
        return web.Response(text="<h2>Test donation</h2><form action='/donate'><input name='size'/><button type='submit'>ok</button></form>", content_type='text/html')

    async def test_donate(self, data: web.Request):
        # update_config()
        print(data, file=sys.stderr)
        print(data.query["size"], file=sys.stderr)
        donation = Donation({
            "additional_data": "{}",
            "amount_main": int(data.query["size"]),
            "username": "FAKE"
        })

        asyncio.get_running_loop().create_task(self.callback(donation))
        return web.HTTPPermanentRedirect("/")

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
        await self.runner.cleanup()
