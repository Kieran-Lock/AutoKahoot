from kahoot_bot import KahootBot


def run():
    bot = KahootBot(debug=True, minimum_answer_delay=0.5, maximum_answer_delay=1.5)
    username, game_pin, game_id = list(bot.get_game_data().values())
    for output_message in bot.play_game(username, game_pin, game_id):
        print(output_message)


if __name__ == "__main__":
    run()
