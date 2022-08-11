import asyncio
import json
import logging
import time
from io import DEFAULT_BUFFER_SIZE

import websockets
from keys import get_client_data
import requests

API_BASE = "https://openapi.vito.ai"

def get_keys() :
    data = get_client_data()
    resp = requests.post(
        API_BASE +"/v1/authenticate",
        data = data
    )
    resp.raise_for_status()
    return resp.json()

class Client :
    def __init__(self, client_id, client_secret) :
        super().__init()
        self.logger = logging.getLogger(__name__)
        self.client_id = client_id
        self.client_secret = client_secret
        self._sess = Session()
        self._token = None


if __name__ == "__main__" :
    print(get_keys())
