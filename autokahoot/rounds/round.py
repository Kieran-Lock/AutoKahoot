from __future__ import annotations
from dataclasses import dataclass
from typing import Any, TYPE_CHECKING
from aiocometd_noloop import Client as CometDClient
from abc import ABC, abstractmethod
if TYPE_CHECKING:
    from ..lobby import Lobby


@dataclass(frozen=True, slots=True)
class Round(ABC):
    index: int
    type: str
    title: str

    @classmethod
    @abstractmethod
    def from_json(cls, json: dict[str, Any], index: int) -> Round:
        ...

    @abstractmethod
    async def send_answer(self, client: CometDClient, lobby: Lobby) -> None:
        ...
