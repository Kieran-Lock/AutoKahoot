from __future__ import annotations
from dataclasses import dataclass
from typing import Any, TYPE_CHECKING
from aiocometd_noloop import Client as CometDClient
from .round import Round
if TYPE_CHECKING:
    from ..lobby import Lobby


@dataclass(frozen=True, slots=True)
class SlideRound(Round):
    description: str

    @classmethod
    def from_json(cls, json: dict[str, Any], index: int) -> SlideRound:
        return cls(
            index,
            json.get("type"),
            json.get("title"),
            json.get("description")
        )

    async def send_answer(self, client: CometDClient, lobby: Lobby) -> None:
        return
