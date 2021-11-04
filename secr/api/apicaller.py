from abc import ABC, abstractmethod, abstractstaticmethod
from typing import Any, Dict

import requests


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


class ApiSaver(ABC):
    def __init__(self, folder: str) -> None:
        self.folder = folder

    @abstractmethod
    def save_dataframe(self, response: str) -> None:
        pass


class ApiCaller:
    def __init__(self, config: ApiConfig, saver: ApiSaver) -> None:
        self.config = config
        self.saver = saver

    def call(self, url: str, query_params: Dict[str, Any], headers: Dict[str, str]):

        response = requests.request("GET", url, headers=headers, params=query_params)
        print("Endpoint Response Code: " + str(response.status_code))
        if response.status_code != 200:
            raise Exception(response.status_code, response.text)

        return response.json()
