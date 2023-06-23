import json

import src.config.state as s


def load_states():
    with open("config.json", 'r') as f:
        d = json.load(f)
        for k, v in d.items():
            if k in s.CONFIGS and v != s.CONFIGS[k]:
                s.CONFIGS[k] = v


def load_state(key: str):
    if key not in s.CONFIGS:
        raise SyntaxError(f'"{key}" not exists in config.')

    with open("config.json", 'r') as f:
        d = json.load(f)
        for k, v in d.items():
            if k == key and v != s.CONFIGS[k]:
                s.CONFIGS[k] = v
