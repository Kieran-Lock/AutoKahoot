from __future__ import annotations
from dataclasses import dataclass
from contextlib import contextmanager
from typing import Iterator
from .event import Event


@dataclass(frozen=True, slots=True)
class Kahoot:
    username: str
    pin: str
    game_id: str

    @contextmanager
    def connect(self) -> Iterator[Kahoot]:
        yield self

    def events(self) -> Iterator[Event]:
        yield Event("Not Implemented")
