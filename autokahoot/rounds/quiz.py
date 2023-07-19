from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, TYPE_CHECKING
from aiocometd_noloop import Client as CometDClient
from json import dumps
from .round import Round
if TYPE_CHECKING:
    from ..lobby import Lobby
from ..question_choice import QuestionChoice


@dataclass(frozen=True, slots=True)
class QuizRound(Round):
    time_allowed_ms: int
    points_enabled: bool
    points_multiplier: float
    choices: list[QuestionChoice] = field(repr=False)
    correct_answer: QuestionChoice = field(init=False, repr=False)

    def __post_init__(self) -> None:
        object.__setattr__(self, "correct_answer", next(filter(lambda choice: choice.is_correct, self.choices)))

    @classmethod
    def from_json(cls, json: dict[str, Any], index: int) -> QuizRound:
        return cls(
            index,
            json.get("type"),
            json.get("question"),
            json.get("time"),
            json.get("points"),
            json.get("pointsMultiplier"),
            [QuestionChoice.from_json(choice_json, index) for index, choice_json in enumerate(json.get("choices"))]
        )

    async def send_answer(self, client: CometDClient, lobby: Lobby) -> None:
        await lobby.send_packet(client, {
            "id": 45,
            "type": "message",
            "content": dumps({
                "choice": self.correct_answer.index,
                "questionIndex": self.index,
            })
        })
