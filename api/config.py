"""Module to store a singleton of the API its global config."""

from dotenv import load_dotenv

from api.utils.config import load_config
from api.utils.constants import YAML_EXTENSION
from configs import CONFIGS_DIRECTORY

# Load environment variables.
load_dotenv()

# Load configuration.
configs = [
    CONFIGS_DIRECTORY / f"{config_name}{YAML_EXTENSION}"
    for config_name in [
        "config",
        "authorization",
        "common",
        "sample",
    ]
]

config = load_config(configs)
