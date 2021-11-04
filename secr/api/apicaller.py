from abc import ABC, abstractstaticmethod


class ApiConfig(ABC):
    """Abstract class for keeping API configs"""

    def __init__(self, api_key: str, api_secret: str) -> None:
        self.api_key = api_key
        self.api_secret = api_secret

    def __repr__(self) -> str:

        anonymized_api_key = "*" * (len(self.api_key) - 4) + self.api_key[-4:]
        anonymized_api_secret = "*" * (len(self.api_secret) - 4) + self.api_secret[-4:]

        return "\n".join(
            [f"API_KEY: {anonymized_api_key}", f"API_SECRET: {anonymized_api_secret}"]
        )

    @abstractstaticmethod
    def from_yaml(path_str: str) -> "ApiConfig":
        """Generates an instance of 'ApiConfig' from a YAML file"""


class ApiCaller:
    def __init__(self, config: ApiConfig) -> None:
        self.config = config
