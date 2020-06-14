import json
from copy import deepcopy


class ConfigurableObject(object):
    name = "obj"
    config_vars = {}
    secret_vars = {}

    def __init__(self):
        # by the python magic, this will do deepcopy of any config vars in the children
        self.config_vars = deepcopy(self.config_vars)
        self.secret_vars = deepcopy(self.secret_vars)

    def __str__(self):
        return f"Name: {self.name}\nVars: {self.config_vars}\nSecrets: {self.secret_vars}"


class Action(ConfigurableObject):
    config_vars = ConfigurableObject.config_vars.copy()
    config_vars.update({
        "conditions": [
            {"price": 0},
        ]
    })

    def __init__(self):
        super().__init__()

    def do(self):
        pass


class Provider(ConfigurableObject):
    config_vars = ConfigurableObject.config_vars.copy()
    config_vars.update({

    })

    def __init__(self, action_callback):
        super().__init__()
        self.callback = action_callback

    def connect(self):
        pass

    def disconnect(self):
        pass


class Donation:
    def __init__(self, message):
        self.message = message
        self.additional_data = json.loads(self.message["additional_data"])
        self.amount = self.message["amount_main"]
        self.username = self.message["username"]

    def __repr__(self):
        return f"Msg: {self.message}, Data:{self.additional_data}, Size:{self.amount}, by {self.username}"

    def __str__(self):
        return f"{self.amount}"


class UnknownMessage:
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return f"{self.message}"
