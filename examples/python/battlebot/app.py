import random
import sys

from .move import Hand
from .move import Move

def play_turn(history, player_number):
    if player_number == '1':
        art = ['*']
    elif player_number == '2':
        art = ['**']
    return Move(random.choice(list(Hand)), art)
