from __future__ import annotations
from dataclasses import dataclass
from contextlib import asynccontextmanager
from typing import AsyncIterator, Any
from aiocometd_noloop import Client as CometDClient
from requests import Response, session as requests_session
from base64 import b64decode
from re import split as re_split
from py_mini_racer import MiniRacer
from itertools import cycle
from time import time
from .quiz import Quiz


@dataclass(frozen=True, slots=True)
class Lobby:
    pin: str
    quiz: Quiz

    @classmethod
    def from_quiz_uuid(cls, uuid: str, pin: str) -> Lobby:
        return cls(pin, Quiz.from_uuid(uuid))

    @asynccontextmanager
    async def connection(self) -> AsyncIterator[CometDClient]:
        response = self.reserve_session()
        session_id = self.solve_challenge(
            response.json().get("challenge"), response.headers.get("x-kahoot-session-token")
        )
        url = f"wss://play.kahoot.it/cometd/{self.pin}/{session_id}"
        async with CometDClient(url, ssl=True) as client:
            yield client

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

    @staticmethod
    def get_event_id(event: dict[str, Any]) -> int:
        return event.get("data", {}).get("id", 0)

    async def send_packet(self, client: CometDClient, packet: dict[str, Any]) -> None:
        await client.publish("/service/controller", {
            "host": "kahoot.it",
            "gameid": self.pin,
            **packet
        })
