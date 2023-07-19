from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, TYPE_CHECKING
from aiocometd_noloop import Client as CometDClient
from json import dumps
from random import randint
from .round import Round
if TYPE_CHECKING:
    from ..lobby import Lobby
from ..question_choice import QuestionChoice


@dataclass(frozen=True, slots=True)
class PollRound(Round):
    time_allowed_ms: int
    choices: list[QuestionChoice] = field(repr=False)

    @classmethod
    def from_json(cls, json: dict[str, Any], index: int) -> PollRound:
        return cls(
            index,
            json.get("type"),
            json.get("question"),
            json.get("time"),
            [QuestionChoice.from_json(choice_json, index) for index, choice_json in enumerate(json.get("choices"))]
        )

    async def send_answer(self, client: CometDClient, lobby: Lobby) -> None:
        await lobby.send_packet(client, {
            "id": 45,
            "type": "message",
            "content": dumps({
                "choice": randint(0, len(self.choices) - 1),
                "questionIndex": self.index,
            })
        })
