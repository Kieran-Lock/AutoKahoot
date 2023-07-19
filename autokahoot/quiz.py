from __future__ import annotations
from dataclasses import dataclass, field
from requests import get
from .rounds import Round, Rounds


@dataclass(frozen=True, slots=True)
class Quiz:
    uuid: str
    language: str
    author: str
    title: str
    description: str = field(repr=False)
    rounds: list[Round] = field(repr=False)

    @classmethod
    def from_uuid(cls, uuid: str) -> Quiz:
        url = f"https://create.kahoot.it/rest/kahoots/{uuid}"
        json = get(url).json()
        return cls(
            uuid,
            json.get("language"),
            json.get("creator"),
            json.get("title"),
            json.get("description"),
            [
                Rounds.get(question_json.get("type", "NOT_IMPLEMENTED").upper()).from_json(question_json, index)
                for index, question_json in enumerate(json.get("questions"))
            ]
        )
