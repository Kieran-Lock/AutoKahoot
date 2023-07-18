from autokahoot import Kahoot
from asyncio import run


def get_inputs() -> tuple[str, str, str]:
    username = input("Username:\t")
    pin = input("Pin:\t")
    game_id = input("Game ID:\t")
    return username, pin, game_id


async def main() -> None:
    # username, pin, game_id = get_inputs()
    username, pin, game_id = "Bot", "9058527", "4113d397-ab64-4245-a94e-77fc2a81c48f"  # Testing game details
    kahoot = Kahoot(username, pin, game_id)
    async with kahoot.connect() as client:
        async for event in kahoot.events(client):
            print(event)


if __name__ == "__main__":
    run(main())
