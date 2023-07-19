from __future__ import annotations
from dataclasses import dataclass, field
from requests import get
from .question import Question


@dataclass(frozen=True, slots=True)
class Quiz:
    uuid: str
    language: str
    author: str
    title: str
    description: str = field(repr=False)
    questions: list[Question] = field(repr=False)

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
            [Question.from_json(question_json) for question_json in json.get("questions")]
        )
