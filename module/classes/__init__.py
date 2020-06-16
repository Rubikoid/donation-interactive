import json
from copy import deepcopy
from typing import Dict, Tuple, Callable, List


class Donation:
    """Generic donation object, builds from dict like
    {
        'additional_data': '{}',
        'amount_main': 123,
        'username': 'aaa'
    }"""

    def __init__(self, message: Dict[str, object]):
        self.message = message
        self.additional_data = json.loads(self.message["additional_data"])
        self.amount = self.message["amount_main"]
        self.username = self.message["username"]

    def __repr__(self) -> str:
        return f"Msg: {self.message}, Data:{self.additional_data}, Size:{self.amount}, by {self.username}"

    def __str__(self) -> str:
        return f"{self.amount}"


class UnknownMessage:
    def __init__(self, message):
        self.message = message

    def __str__(self) -> str:
        return f"{self.message}"


class ConfigurableObject(object):
    """Virtual class for generic configurable object.
    On creation, do deepcopy of class atrributes config/secret_vars to save original class attributes from modifying by instance.

    Attributes
    ----------
    config_vars: Dict[str, object]
        vars, that can be configured and saved to file.
    secret_vars: Dict[str, object]
        vars like config_vars, but saved in the separate file. can be useful for tokens, etc..
    """

    config_vars: Dict[str, object] = {
        'type': 'obj',
        'name': 'empty obj',
    }
    secret_vars: Dict[str, object] = {}

    def __init__(self):
        # by the python magic, this will do deepcopy of any config vars in the children
        self.config_vars = deepcopy(self.config_vars)
        self.secret_vars = deepcopy(self.secret_vars)

    def short(self) -> str:
        return f"[{self.config_vars['type']}] {self.config_vars['name']}"

    def __str__(self) -> str:
        return f"Type: {self.config_vars['type']}, name: {self.config_vars['name']}\nVars: {self.config_vars}\nSecrets: {self.secret_vars.keys()}"


class Action(ConfigurableObject):
    """Virtual class for generic action, that can be performed after donate.

    Attributes
    ----------
    key_callback: Callable[[List[str]], None]
        Callback for sending currently pressed keys or any other data to display

    Methods
    -------
    async do(donate: Donation)
        Call on donation. Should call key_callback with pressed keys.
    """

    config_vars = ConfigurableObject.config_vars.copy()  # this is the right way to update parent's config_vars, and get many probles
    config_vars.update({
        'type': 'generic_action',
        'name': 'empty action',
        'enabled': False
    })

    def __init__(self, key_callback: Callable[[List[str]], None]):
        super().__init__()
        self.key_callback = key_callback

    async def do(self, donate: Donation):
        await self.key_callback([])


class Provider(ConfigurableObject):
    """Virtual class for generic donation provider, that catches donations/etc.

    Attributes
    ----------
    donation_callback: Callable[[Donation]
        callback for sending new donations

    Methods
    -------
    async connect()
        Call on programm init, should connect to site/start server/etc
    async disconnect()
        Call on programm exit, should disconnect from site/shutdown server/etc
    """

    config_vars = ConfigurableObject.config_vars.copy()
    config_vars.update({
        'type': 'generic_provider',
        'name': 'empty provider',
    })

    def __init__(self, donation_callback: Callable[[Donation], None]):
        super().__init__()
        self.callback = donation_callback

    async def connect(self):
        pass

    async def disconnect(self):
        pass
