"""Module to store a singleton of the API its global config."""

from dotenv import load_dotenv

from api.utils.config import load_config
from configs import CONFIGS_DIRECTORY

# Load environment variables.
load_dotenv()

# Load configuration.
config_path = CONFIGS_DIRECTORY / "config.yaml"
authorization_config_path = CONFIGS_DIRECTORY / "authorization.yaml"
common_config_path = CONFIGS_DIRECTORY / "common.yaml"
sample_config_path = CONFIGS_DIRECTORY / "sample.yaml"

config = load_config(
    [
        config_path,
        authorization_config_path,
        common_config_path,
        sample_config_path,
    ],
)
