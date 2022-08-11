import asyncio
import json
import logging
import time
from io import DEFAULT_BUFFER_SIZE

import websockets
from keys import get_client_data
from requests import Session

API_BASE = "https://openapi.vito.ai"

def get_keys() :
    data = get_client_data()
    print(data)


class Client :
    def __init__(self, client_id, client_secret) :
        super().__init()
        self.logger = logging.getLogger(__name__)
        self.client_id = client_id
        self.client_secret = client_secret
        self._sess = Session()
        self._token = None


if __name__ == "__main__" :
    get_keys()
