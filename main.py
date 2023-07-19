from autokahoot import Bot, Lobby
from asyncio import run


def get_inputs() -> tuple[str, str, str]:
    uuid = input("Game ID:\t")
    pin = input("Pin:\t")
    username = input("Username:\t")
    return uuid, pin, username


async def main() -> None:
    uuid, pin, username = get_inputs()
    lobby = Lobby.from_quiz_uuid(uuid, pin)
    bot = Bot(username)
    async with bot.connect(lobby) as client:
        await bot.play(lobby, client)


if __name__ == "__main__":
    run(main())
