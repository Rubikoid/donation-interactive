from ..classes import Provider, Donation, UnknownMessage
import asyncio
import json
import sys


class ProviderExample(Provider):
    """Example provider, which sends one simple donate every period.

    Config:
    ---
    amount: int = 1337
        donate amount
    period: int = 2222
        period of donate sending
    """

    name = "ProviderExample"

    config_vars = Provider.config_vars.copy()
    config_vars.update({
        'amount': 1337,
        'period': 2222
    })

    secret_vars = Provider.secret_vars.copy()
    secret_vars.update({})

    _running = False

    def __init__(self, donation_callback):
        super().__init__(donation_callback)

    async def test_donate(self):
        # update_config()
        if self._running:
            donation = Donation({
                "additional_data": "{}",
                "amount_main": self.config_vars["amount"],
                "username": "FAKE"
            })
            await self.callback(donation)
            asyncio.get_event_loop().call_later(self.config_vars["period"], self.test_donate)

    async def connect(self):
        self._running = True
        asyncio.get_event_loop().call_later(self.config_vars["period"], self.test_donate)

    async def disconnect(self):
        await self.runner.cleanup()
