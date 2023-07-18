from autokahoot import Kahoot
from asyncio import run
from threading import Thread


def get_inputs() -> tuple[str, str, str]:
    # username = input("Username:\t")
    # pin = input("Pin:\t")
    # game_id = input("Game ID:\t")
    # return username, pin, game_id
    return (
        "Pickles9",
        "4642201",
        "739c6780-b383-463f-9a9c-c9d1d9214fab"
    )


async def main() -> None:
    username, pin, game_id = get_inputs()
    kahoot = Kahoot(username, pin, game_id)
    async with kahoot.connect() as client:
        async for event in kahoot.events(client):
            pass
            # print(event)


def run_program():
    run(main())


if __name__ == "__main__":
    t = Thread(target=run_program)
    t.start()
    t.join()
