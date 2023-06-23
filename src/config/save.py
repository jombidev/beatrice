import json

import src.config.state as s


def save_states():
    with open("config.json", 'w') as f:
        json.dump(s.CONFIGS, f, indent=4)


def save_state(k: str, v):
    if k not in s.CONFIGS:
        raise SyntaxError(f'"{k}" not exists in config.')

    if s.CONFIGS[k] != v:
        s.CONFIGS[k] = v

    with open("config.json", 'w') as f:
        json.dump(s.CONFIGS, f, indent=4)
