import os

from pyaml_env import parse_config

config_location = os.getenv("CONFIG_CONTEXT")

if not config_location:
    raise ValueError("CONFIG_CONTEXT not set")

config = parse_config(config_location)
