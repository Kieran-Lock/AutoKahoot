from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, TYPE_CHECKING
from aiocometd_noloop import Client as CometDClient
from json import dumps
from .quiz import QuizRound
if TYPE_CHECKING:
    from ..lobby import Lobby
from ..question_choice import QuestionChoice


@dataclass(frozen=True, slots=True)
class TypeAnswerRound(QuizRound):
    @classmethod
    def from_json(cls, json: dict[str, Any], index: int) -> TypeAnswerRound:
        return cls(
            index,
            json.get("type"),
            json.get("question"),
            json.get("time"),
            bool(json.get("pointsMultiplier")),
            json.get("pointsMultiplier"),
            [QuestionChoice.from_json(choice_json, index) for index, choice_json in enumerate(json.get("choices"))]
        )

    async def send_answer(self, client: CometDClient, lobby: Lobby) -> None:
        await lobby.send_packet(client, {
            "id": 45,
            "type": "message",
            "content": dumps({
                "text": self.correct_answer.answer_text,
                "questionIndex": self.index,
            })
        })
