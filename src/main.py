import asyncio
import json
import logging
import time
from io import DEFAULT_BUFFER_SIZE

import websockets
from keys import get_client_data
from requests import Session

API_BASE = "https://openapi.vito.ai"

class Client :
    def __init__(self, client_data) :
        super().__init()
        self.logger = logging.getLogger(__name__)
        self.client_data = client_data
        self._sess = Session()
        self._token = None

    @property
    def token(self) :
        if self._token is None or self._token["expire_at"] < time.time() :
            resp = self._sess.post(
                API_BASE + "/v1/authenticate"
                data = client_data
            )
            resp.raise_for_status()
        return self._token["access_token"]


if __name__ == "__main__" :
    client_data = get_client_data()

