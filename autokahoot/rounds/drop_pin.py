from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, TYPE_CHECKING
from aiocometd_noloop import Client as CometDClient
from json import dumps
from .round import Round
if TYPE_CHECKING:
    from ..lobby import Lobby


@dataclass(frozen=True, slots=True)
class DropPinRound(Round):
    @classmethod
    def from_json(cls, json: dict[str, Any], index: int) -> DropPinRound:
        return cls(
            index,
            json.get("type"),
            json.get("question")
        )

    async def send_answer(self, client: CometDClient, lobby: Lobby) -> None:
        await lobby.send_packet(client, {
            "id": 45,
            "type": "message",
            "content": dumps({
                "type": "drop_pin",
                "pin": {
                    "x": 50.0,
                    "y": 50.0
                },
                "questionIndex": self.index,
            })
        })


"""
content
: 
"{\"type\":\"drop_pin\",\"pin\":{\"x\":47.45958429561201,\"y\":76.76923076923077},\"questionIndex\":2,\"meta\":{\"lag\":52}}"
gameid
: 
"9221587"
host
: 
"kahoot.it"
id
: 
45
type
: 
"message"""
