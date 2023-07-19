from autokahoot import Bot, Lobby
from asyncio import run


def get_inputs() -> tuple[str, str, str]:
    # uuid = input("Quiz ID:\t")
    # pin = input("Lobby Pin:\t")
    # username = input("Bot Username:\t")
    # return uuid, pin, username
    return (
        "ae0e4ffc-30d0-43b6-a236-8612a583011c",
        "1205671",
        "Bot"
    )


async def main() -> None:
    uuid, pin, username = get_inputs()
    lobby = Lobby.from_quiz_uuid(uuid, pin)
    bot = Bot(username)
    async with bot.connect(lobby) as client:
        await bot.play(lobby, client)


if __name__ == "__main__":
    run(main())
