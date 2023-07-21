from autokahoot import Bot, Lobby
from asyncio import run


def get_inputs() -> tuple[str, str, str]:
    uuid = input("Quiz ID:\t")
    pin = input("Lobby Pin:\t")
    username = input("Bot Username:\t")
    return uuid, pin, username


async def main() -> None:
    uuid, pin, username = get_inputs()
    lobby = Lobby.from_quiz_uuid(uuid, pin)
    bot = Bot(username)
    async with bot.connect(lobby) as client:
        await bot.play(lobby, client)


if __name__ == "__main__":
    run(main())
