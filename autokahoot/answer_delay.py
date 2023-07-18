from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AnswerDelay:
    mean: float
    spread: float
