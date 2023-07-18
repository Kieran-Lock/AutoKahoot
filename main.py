from autokahoot import Kahoot
from asyncio import run


def get_inputs() -> tuple[str, str, str]:
    username = input("Username:\t")
    pin = input("Pin:\t")
    game_id = input("Game ID:\t")
    return username, pin, game_id


async def main() -> None:
    # username, pin, game_id = get_inputs()
    username, pin, game_id = "Bot", "2864568", "9983b771-65bc-4175-af56-d647d3cabc8d"  # Testing game details
    kahoot = Kahoot(username, pin, game_id)
    async with kahoot.connect() as client:
        async for event in kahoot.events(client):
            print(event)


if __name__ == "__main__":
    run(main())
