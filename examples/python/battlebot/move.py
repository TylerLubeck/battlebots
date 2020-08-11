import dataclasses
from enum import Enum
import json

from typing import List

class Hand(str, Enum):
    ROCK = "ROCK"
    PAPER = "PAPER"
    SCISSORS = "SCISSORS"

@dataclasses.dataclass
class Move:
    move: Hand
    art: List[str]

    def to_json(self):
        return json.dumps(dataclasses.asdict(self))

