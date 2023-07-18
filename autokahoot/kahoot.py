from __future__ import annotations
from dataclasses import dataclass
from contextlib import asynccontextmanager
from typing import AsyncIterator
from time import time
from py_mini_racer import MiniRacer
from base64 import b64decode
from re import split as re_split
from itertools import cycle
from aiocometd_noloop import Extension, Client as CometDClient
from requests import Response, session as requests_session
from .event import Event


class LoggingExtension(Extension):
    async def incoming(self, payload, headers=None):
        if payload[0].get("channel").startswith("/meta"):
            return payload
        print("Incoming:", payload, end="\n\n")
        return payload

    async def outgoing(self, payload, headers):
        if isinstance(payload[0].get("channel"), MetaChannel):
            return payload
        print("Outgoing:", payload, end="\n\n")
        return payload


@dataclass(frozen=True, slots=True)
class Kahoot:
    username: str
    pin: str
    game_id: str

    @asynccontextmanager
    async def connect(self) -> AsyncIterator[CometDClient]:
        response = self.reserve_session()
        session_id = self.solve_challenge(
            response.json().get("challenge"), response.headers.get("x-kahoot-session-token")
        )
        url = f"wss://play.kahoot.it/cometd/{self.pin}/{session_id}"
        async with CometDClient(url, ssl=True, extensions=[LoggingExtension()]) as client:
            yield client

    async def events(self, client: CometDClient) -> AsyncIterator[Event]:
        for subscription in ("controller", "player", "status"):
            await client.subscribe(f"/service/{subscription}")
        await client.publish(
            "/service/controller",
            {
                "host": "kahoot.it", "gameid": self.pin,
                "name": self.username, "type": "login",
                "content": "{\"device\":{\"userAgent\":\"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.82\",\"screen\":{\"width\":1920,\"height\":1080}}}"
            }
        )
        async for message in client:
            if message.get("data", {}).get("type") == "loginResponse":
                break

        await client.publish(
            "/service/controller",
            {
                "type": "message",
                "gameid": int(self.pin),
                "host": "kahoot.it",
                "content": "{\"usingNamerator\":false}",
                "id": 16
            }
        )
        # # input("b\n")
        # await client.publish(
        #     "/service/controller",
        #     {
        #         "id": 46,
        #         "type": "message",
        #         "gameid": "3647098",
        #         "host": "kahoot.it",
        #         "content": {"avatar": {"type": 2200, "item": 1550}}
        #     }
        # )
        async for client_message in client:
            yield Event(client_message.get("data"))

    def reserve_session(self) -> Response:
        session = requests_session()
        url = f"https://play.kahoot.it/reserve/session/{self.pin}/?{int(time())}"
        response = session.get(url)
        if response.status_code != 200:
            raise ValueError(f"No game exists with pin '{self.pin}'") from None
        return response

    @staticmethod
    def solve_challenge(challenge: str, session_token: str) -> str:
        session_token = b64decode(session_token).decode("utf-8", "strict")
        challenge = re_split("[{};]", challenge.replace("\t", "", -1).encode("ascii", "ignore").decode("utf-8"))
        solution = MiniRacer().eval(
            f"{challenge[1]}{{{challenge[2]};return message.replace(/./g, function(char, position)"
            f"{{{challenge[7]};}})}};{challenge[0]}"
        )
        return "".join(chr(ord(session_token_character) ^ ord(solution_character))
                       for session_token_character, solution_character in zip(session_token, cycle(solution)))
