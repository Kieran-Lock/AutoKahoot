from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Event:
    payload: str
