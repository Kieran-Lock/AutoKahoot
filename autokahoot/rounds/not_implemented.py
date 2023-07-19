from __future__ import annotations
from dataclasses import dataclass
from typing import Any, TYPE_CHECKING
from aiocometd_noloop import Client as CometDClient
from .round import Round
if TYPE_CHECKING:
    from ..lobby import Lobby


@dataclass(frozen=True, slots=True)
class NotImplementedRound(Round):
    @classmethod
    def from_json(cls, json: dict[str, Any], index: int) -> NotImplementedRound:
        return cls(
            index,
            json.get("type"),
            "NOT IMPLEMENTED"
        )

    async def send_answer(self, client: CometDClient, lobby: Lobby) -> None:
        return
