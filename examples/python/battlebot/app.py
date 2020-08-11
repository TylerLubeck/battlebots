import random
import sys

from .move import Hand
from .move import Move

def play_turn(history):
    return Move(random.choice(list(Hand)), [])
