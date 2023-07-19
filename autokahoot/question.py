from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any
from .question_choice import QuestionChoice


@dataclass(frozen=True, slots=True)
class Question:
    type: str
    question_text: str
    time_allowed_ms: int
    points_enabled: bool
    points_multiplier: float
    choices: list[QuestionChoice] = field(repr=False)
    correct_answer: QuestionChoice = field(init=False, repr=False)

    def __post_init__(self) -> None:
        object.__setattr__(self, "correct_answer", next(filter(lambda choice: choice.is_correct, self.choices)))

    @classmethod
    def from_json(cls, json: dict[str, Any]) -> Question:
        return cls(
            json.get("type"),
            json.get("question"),
            json.get("time"),
            json.get("points"),
            json.get("pointsMultiplier"),
            [QuestionChoice.from_json(choice_json, index) for index, choice_json in enumerate(json.get("choices"))]
        )
