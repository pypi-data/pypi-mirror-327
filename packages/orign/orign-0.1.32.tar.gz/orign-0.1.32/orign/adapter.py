from typing import Optional

import requests

from orign.config import GlobalConfig


class Adapter:
    @classmethod
    def get(cls, name: Optional[str] = None, config: Optional[GlobalConfig] = None):
        config = config or GlobalConfig.read()

        # Construct the WebSocket URL with query parameters
        adapters_url = f"{config.server}/v1/adapters"

        response = requests.get(
            adapters_url, headers={"Authorization": f"Bearer {config.api_key}"}
        )
        response.raise_for_status()
        response_jdict = response.json()
        adapters = response_jdict.get("adapters", [])
        if name:
            adapters = [a for a in adapters if a == name]
        return adapters
