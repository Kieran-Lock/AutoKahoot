from __future__ import annotations
from dataclasses import dataclass
from contextlib import contextmanager
from typing import Iterator
from time import time
from requests import Response, session as requests_session
from .event import Event


@dataclass(frozen=True, slots=True)
class Kahoot:
    username: str
    pin: str
    game_id: str

    @contextmanager
    def connect(self) -> Iterator[Kahoot]:
        session_response = self.reserve_session()
        print(session_response, session_response.json(), sep="\n")
        yield self

    def events(self) -> Iterator[Event]:
        yield Event("Not Implemented")

    def reserve_session(self) -> Response:
        session = requests_session()
        url = f"https://play.kahoot.it/reserve/session/{self.pin}/?{int(time())}"
        response = session.get(url)
        if response.status_code != 200:
            raise ValueError(f"No game exists with pin '{self.pin}'") from None
        return response
