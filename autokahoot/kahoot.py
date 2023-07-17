from __future__ import annotations
from dataclasses import dataclass
from contextlib import contextmanager
from typing import Iterator
from time import time
from py_mini_racer import MiniRacer
from base64 import b64decode
from re import split as re_split
from itertools import cycle
from requests import Response, session as requests_session
from .event import Event


@dataclass(frozen=True, slots=True)
class Kahoot:
    username: str
    pin: str
    game_id: str

    @contextmanager
    def connect(self) -> Iterator[Kahoot]:
        response = self.reserve_session()
        session_id = self.solve_challenge(
            response.json().get("challenge"), response.headers.get("x-kahoot-session-token")
        )
        yield self

    def events(self) -> Iterator[Event]:
        yield Event(f"Developing solution for game with ID '{self.game_id}'")

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
