from enum import Enum
from .not_implemented import NotImplementedRound
from .quiz import QuizRound
from .multiple_choice_quiz import MultipleChoiceQuizRound
from .slide import SlideRound
from .round import Round
from .poll import PollRound
from .type_answer import TypeAnswerRound
from .drop_pin import DropPinRound


class Rounds(Enum):
    NOT_IMPLEMENTED = NotImplementedRound  # Fallback
    QUIZ = QuizRound  # Quiz, True / False
    MULTIPLE_SELECT_QUIZ = MultipleChoiceQuizRound  # Multiple Choice Quiz
    CONTENT = SlideRound  # Slide
    SURVEY = PollRound  # Poll
    OPEN_ENDED = TypeAnswerRound  # Type Answer, Open-Ended
    DROP_PIN = DropPinRound  # Drop Pin

    @classmethod
    def get(cls, item: str) -> type[Round]:
        try:
            return cls[item].value
        except KeyError:
            return cls.NOT_IMPLEMENTED.value
