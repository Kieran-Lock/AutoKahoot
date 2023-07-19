from __future__ import annotations
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class QuestionChoice:
    answer_text: str
    is_correct: bool
    index: int

    @classmethod
    def from_json(cls, json: dict[str, Any], index: int) -> QuestionChoice:
        return cls(
            json.get("answer"),
            json.get("correct"),
            index
        )
