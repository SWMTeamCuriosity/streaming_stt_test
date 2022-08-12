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
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.client_data = client_data
        self._sess = Session()
        self._token = None

    @property
    def token(self) :
        if self._token is None or self._token["expire_at"] < time.time() :
            resp = self._sess.post(
                API_BASE + "/v1/authenticate",
                data = self.client_data
            )

            resp.raise_for_status()
            self._token = resp.json()
        return self._token["access_token"]

    async def streaming_transcribe(self, filename, config=None) :
        if config is None:
            config = dict(sample_rate = "8000", encoding = "LINEAR16", use_itn = "true", use_disfluency_filter = "true", use_profanity_filter = "false")

        STREAMING_ENDPOINT = "wss://{}/v1/transcribe:streaming?{}".format(
            API_BASE.split("//")[1], "&".join(map("=".join, config.items()))
        )
        print(STREAMING_ENDPOINT)

        conn_kwargs = dict(extra_headers={"Authorization" : "bearer " + self.token})

        async def streamer(websocket) :
            with open(filename, "rb") as f:
                while True :
                    buff = f.read(DEFAULT_BUFFER_SIZE * 4)
                    if buff is None or len(buff) == 0 :
                        break
                    await websocket.send(buff)
                await websocket.send("EOS")

        async def transcriber(websocket) :
            async for msg in websocket :
                msg = json.loads(msg)
                print(msg)
                if msg["final"] :
                    print("final ended with " + msg["alternatives"][0]["text"])

        async with websockets.connect(STREAMING_ENDPOINT, **conn_kwargs) as websocket :
            await asyncio.gather(
                streamer(websocket),
                transcriber(websocket),
            )

if __name__ == "__main__" :
    client_data = get_client_data()
    client = Client(client_data)

    fname = "../data/test.pcm"
    asyncio.run(client.streaming_transcribe(fname))
