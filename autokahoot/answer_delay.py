from dataclasses import dataclass


@dataclass(frozen=True)
class AnswerDelay:
    __slots__ = "mean", "spread"

    mean: float
    spread: float
