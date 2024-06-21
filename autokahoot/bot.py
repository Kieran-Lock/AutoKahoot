from __future__ import annotations
from dataclasses import dataclass
from aiocometd_noloop import Client as CometDClient
from contextlib import asynccontextmanager
from typing import AsyncIterator
from json import loads
from .events import Events
from .lobby import Lobby


@dataclass(frozen=True, slots=True)
class Bot:
    username: str

    @asynccontextmanager
    async def connect(self, lobby: Lobby) -> AsyncIterator[CometDClient]:
        async with lobby.connection() as client:
            for subscription in ("controller", "player", "status"):
                await client.subscribe(f"/service/{subscription}")
            for packet in ({"name": self.username, "type": "login"}, {"id": 16, "type": "message"}):
                await lobby.send_packet(client, packet)
            yield client

    @staticmethod
    async def play(lobby: Lobby, client: CometDClient) -> None:
        from pprint import pformat

        async for event in client:
            print(f"Received Event: {pformat(event)}")
            if lobby.get_event_id(event) == Events.START_QUESTION.value:
                print("Starting question!")
                question_index = loads(event.get("data").get("content")).get("gameBlockIndex")
                await lobby.quiz.rounds[question_index].send_answer(client, lobby)
