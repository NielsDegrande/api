"""Module to store a singleton of the API its global config."""

from dotenv import load_dotenv

from api.utils.config import load_config
from api.utils.constants import YAML_EXTENSION
from configs import CONFIGS_DIRECTORY

# Load environment variables.
load_dotenv()

# Load configuration.
config_path = CONFIGS_DIRECTORY / f"config{YAML_EXTENSION}"
authorization_config_path = CONFIGS_DIRECTORY / f"authorization{YAML_EXTENSION}"
common_config_path = CONFIGS_DIRECTORY / f"common{YAML_EXTENSION}"
sample_config_path = CONFIGS_DIRECTORY / f"sample{YAML_EXTENSION}"

config = load_config(
    [
        config_path,
        authorization_config_path,
        common_config_path,
        sample_config_path,
    ],
)
