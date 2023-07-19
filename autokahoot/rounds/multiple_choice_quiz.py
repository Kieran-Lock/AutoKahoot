from __future__ import annotations
from dataclasses import dataclass, field
from aiocometd_noloop import Client as CometDClient
from json import dumps
from typing import TYPE_CHECKING
from .quiz import QuizRound
if TYPE_CHECKING:
    from ..lobby import Lobby
from ..question_choice import QuestionChoice


@dataclass(frozen=True, slots=True)
class MultipleChoiceQuizRound(QuizRound):
    correct_answers: list[QuestionChoice] = field(init=False, repr=False)

    def __post_init__(self) -> None:
        object.__setattr__(self, "correct_answers", list(filter(lambda choice: choice.is_correct, self.choices)))

    async def send_answer(self, client: CometDClient, lobby: Lobby) -> None:
        await lobby.send_packet(client, {
            "id": 45,
            "type": "message",
            "content": dumps({
                "choice": list(map(lambda answer: answer.index, self.correct_answers)),
                "questionIndex": self.index,
            })
        })
