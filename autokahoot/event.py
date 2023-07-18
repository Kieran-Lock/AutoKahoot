from dataclasses import dataclass


@dataclass(frozen=True)
class Event:
    __slots__ = "payload"

    payload: str
