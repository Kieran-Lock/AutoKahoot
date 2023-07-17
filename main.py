from autokahoot import Kahoot


def get_inputs() -> tuple[str, str, str]:
    username = input("Username:\t")
    pin = input("Pin:\t")
    game_id = input("Game ID:\t")
    return username, pin, game_id


def main() -> None:
    username, pin, game_id = get_inputs()
    with Kahoot(username, pin, game_id).connect() as kahoot:
        for event in kahoot.events():
            print(event)


if __name__ == "__main__":
    main()
