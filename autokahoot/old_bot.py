import asyncio
import base64
import json
import random
import re
import time
import aiocometd
import requests
from py_mini_racer import py_mini_racer


class KahootBot:
    def __init__(self, debug=False, minimum_answer_delay=0.0, maximum_answer_delay=0.0):
        self.session = requests.session()
        self.debug = debug
        self.minimum_answer_delay = minimum_answer_delay
        if maximum_answer_delay >= self.minimum_answer_delay:
            self.maximum_answer_delay = maximum_answer_delay
        else:
            self.maximum_answer_delay = self.minimum_answer_delay

    def play_game(self, username, pin, game_id):
        response = self.__reserve_session(pin)
        session_id = self.__solve_response_challenge(response.json()["challenge"],
                                                     response.headers["x-kahoot-session-token"])

        asyncio.get_event_loop().run_until_complete(self.__play(username, pin, game_id, session_id))

    async def __play(self, username, pin, game_id, session_id):
        url = f"wss://play.kahoot.it/cometd/{pin}/{session_id}"

        async with aiocometd.Client(url, ssl=True) as client:
            socket = await self.__get_socket(client, username, pin)
            answers = [answer async for answer in self.get_answers(game_id)]
            question_idx = -1
            answer_routines = {
                "quiz": self.__quiz_question
            }

            async for client_message in client:
                client_message = client_message["data"]
                if self.debug:
                    print(client_message)
                message_meaning = self.__decode_kahoot_code(client_message["id"]) \
                    if "id" in client_message else None

                if message_meaning is not None and self.debug:
                    print(f"\nServer Message: [{message_meaning}]")

                if message_meaning == "Username Rejected":
                    raise RuntimeError("The provided username was rejected") from None

                elif message_meaning == "Reset Controller":
                    if self.debug:
                        print("\nThe game was ended.")
                    exit()

                elif message_meaning == "Get Ready":
                    question_idx += 1

                elif message_meaning == "Start Question":
                    answer_data = answers[question_idx]

                    try:
                        delay = random.uniform(self.minimum_answer_delay, self.maximum_answer_delay)
                        answer = await answer_routines[f"{answer_data['Question Type']}"](answer_data)
                        if answer is not None:
                            print("Answer not None")
                            await self.__send_answer(socket, pin, answer, delay=delay)
                            print("Sent answer")
                        else:
                            if self.debug:
                                print("\nClient Message: [Impossible Question]")

                    except KeyError:
                        if self.debug:
                            print("\nClient Message: [Unexpected Question Type]"
                                  "---> This type of question has likely not been coded for yet.")

    @staticmethod
    async def __send_answer(socket, pin, answer, delay):
        answer_info = json.dumps({
            "choice": answer,
            "meta": {"lag": 0, "device": {"userAgent": "kbot", "screen": {"width": 1920, "height": 1080}}}
        })

        if delay != 0.0:
            await asyncio.sleep(delay)

        await socket.publish("/service/controller",
                             {"content": answer_info,
                              "gameid": pin, "host": "kahoot.it", "type": "message", "id": 45})

    @staticmethod
    async def __quiz_question(answer_data):
        correct_answer_indexes = [answer["Index"] for answer in answer_data["Correct Answers"]]
        return random.choice(correct_answer_indexes)

    async def get_answers(self, game_id):
        url = f"https://create.kahoot.it/rest/kahoots/{game_id}"
        response = self.session.get(url)

        if response.status_code == 400:
            raise ValueError("The provided game ID was invalid") from None
        elif response.status_code != 200:
            raise RuntimeError("An error occurred finding the answers. Tip: The Kahoot may be private") from None

        game = response.json()

        for idx, question in enumerate(game["questions"]):
            yield {"Question Type": question["type"], "Time Limit": question["time"],
                   "Correct Answers": [{"Answer": answer["answer"], "Index": idx}
                                       for idx, answer in enumerate(question["choices"]) if answer["correct"]],
                   "Incorrect Answers": [{"Answer": answer["answer"], "Index": idx}
                                         for idx, answer in enumerate(question["choices"]) if not answer["correct"]]}

    @staticmethod
    async def __get_socket(client, username, pin):
        for subscription in ["/service/controller", "/service/player", "/service/status"]:
            await client.subscribe(subscription)

        await client.publish('/service/controller', {"host": "kahoot.it", "gameid": pin, "captchaToken":
            "KAHOOT_TOKEN_frkdbxs3k7nf741hbvf=", "name": username, "type": "login"})

        return client

    def __reserve_session(self, pin):
        if type(pin) != str:
            raise TypeError("The provided game pin was not a string") from None

        url = f"https://play.kahoot.it/reserve/session/{pin}/?{int(time.time())}"
        res = self.session.get(url)
        if res.status_code != 200:
            raise ValueError("The provided game pin was non-existent") from None

        return res

    @staticmethod
    def __solve_response_challenge(challenge, session_token):
        # Credit to 'idiidk' for challenge solution
        js_engine = py_mini_racer.MiniRacer()
        decoded_session_token = base64.b64decode(session_token).decode('utf-8', 'strict')

        challenge = re.split("[{};]", challenge.replace('\t', '', -1).encode('ascii', 'ignore').decode('utf-8'))
        rebuilt_javascript = f"{challenge[1]}{{{challenge[2]};return message.replace(/./g, function(char, position)" \
                             f"{{{challenge[7]};}})}};{challenge[0]}"
        challenge_solution = js_engine.eval(rebuilt_javascript)

        solution_characters = [ord(char) for char in challenge_solution]
        session_characters = [ord(char) for char in decoded_session_token]
        session_id = "".join([chr(session_characters[i] ^ solution_characters[i % len(solution_characters)])
                              for i in range(len(session_characters))])

        return session_id

    @staticmethod
    def get_game_data():
        username = input("Enter your username.\n\nInput:\t")
        pin = input("\nEnter the game pin.\n\nInput:\t")
        game_id = input("\nEnter the game ID. (Found in the Browser URL)\n\nInput:\t")

        return {"Username": username, "Pin": pin, "Game ID": game_id}

    @staticmethod
    def __decode_kahoot_code(code_id):
        decode_table = {
            1: "Get Ready",
            2: "Start Question",
            3: "Game Over",
            4: "Time Up",
            5: "Play Again",
            6: "Answer Selected",
            7: "Answer Response",
            8: "Reveal Answer",
            9: "Start Quiz",
            10: "Reset Controller",
            11: "Submit Feedback",
            12: "Feedback",
            13: "Reveal Ranking",
            14: "Username Accepted",
            15: "Username Rejected",
            16: "Request Recovery Data From Player",
            17: "Send Recovery Data To Controller",
            18: "Join Team Members",
            19: "Join Team Members Response",
            20: "Start Team Talk",
            21: "Skip Team Talk",
            31: "iFrame Controller Event",
            32: "Server iFrame Event",
            40: "Story Block Get Ready",
            41: "Reaction Selected",
            42: "Reaction Response",
            43: "Game Block Start",
            44: "Game Block End",
            45: "Game Block Answer",
            50: "Submit Two Factor Authentication",
            51: "Two Factor Authentication Incorrect",
            52: "Two Factor Authentication Correct",
            53: "Reset Two Factor Authentication"}

        return decode_table[code_id]
