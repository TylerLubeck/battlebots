import dataclasses
from enum import Enum
import json

class Hand(str, Enum):
    ROCK = "ROCK"
    PAPER = "PAPER"
    SCISSORS = "SCISSORS"

@dataclasses.dataclass
class Move:
    move: Hand
    art: str

    def to_json(self):
        return json.dumps(dataclasses.asdict(self))

