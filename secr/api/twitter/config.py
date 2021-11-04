from pathlib import Path

import yaml
from secr.api.apicaller import ApiConfig
from secr.api.utils_config import anonymize
from yaml import Loader


class TwitterApiConfig(ApiConfig):
    def __init__(self, api_key: str, api_secret: str, bearer_token: str) -> None:
        super().__init__(api_key, api_secret)
        self.bearer_token = bearer_token

    def __repr__(self) -> str:

        super_repr_string = super().__repr__()
        return "\n".join(
            [
                "Twitter API config",
                super_repr_string,
                f"BEARER_TOKEN: {anonymize(self.bearer_token)}",
            ]
        )

    @staticmethod
    def from_yaml(path_str: str) -> "TwitterApiConfig":
        """Generates an instance of 'TwitterApiConfig' from a YAML file"""

        path = Path(path_str)
        with path.open() as f:
            yaml_config = yaml.load(f, Loader=Loader)["twitter"]

        api_key = yaml_config["API_KEY"]
        api_secret = yaml_config["API_SECRET"]
        bearer_token = yaml_config["BEARER_TOKEN"]

        return TwitterApiConfig(
            api_key=api_key, api_secret=api_secret, bearer_token=bearer_token
        )
