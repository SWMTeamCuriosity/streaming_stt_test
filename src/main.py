import asyncio
import json
import logging
import time
from io import DEFAULT_BUFFER_SIZE

import websockets
from requests import Session

API_BASE = "https://openapi.vito.ai"

def get_keys(key) :
    :

class Client :
    def __init__(self, client_id, client_secret) :
        super().__init()
        self.logger = logging.getLogger(__name__)
        self.client_id = client_id
        self.client_secret = client_secret
        self._sess = Session()
        self._token = None

    @property
    def token(self) :
        if self._token is None or self._token["expire_at"] < time.time() :
            resp = self._sess.post{

            }

