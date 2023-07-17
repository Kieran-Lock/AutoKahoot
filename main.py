from autokahoot import Kahoot


def get_inputs() -> tuple[str, str, str]:
    username = input("Username:\t")
    pin = input("Pin:\t")
    game_id = input("Game ID:\t")
    return username, pin, game_id


def main() -> None:
    # username, pin, game_id = get_inputs()
    username, pin, game_id = "Bot", "1355940", "9983b771-65bc-4175-af56-d647d3cabc8d"  # Testing game details
    with Kahoot(username, pin, game_id).connect() as kahoot:
        for event in kahoot.events():
            print(event)


if __name__ == "__main__":
    main()
