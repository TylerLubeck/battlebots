from collections import Counter
from dataclasses import dataclass
from dataclasses import InitVar
import dataclasses
from enum import IntEnum
from itertools import zip_longest
import random

from battlebots.games import BattleBotGame

class Hand(IntEnum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3

    def __str__(self):
        return str(self.name[0].lower())


PLAYER_ONE_WINS = frozenset((
    Hand.ROCK     - Hand.SCISSORS,
    Hand.PAPER    - Hand.ROCK,
    Hand.SCISSORS - Hand.PAPER,
))


PLAYER_ONE_LOSES = frozenset((
    Hand.ROCK     - Hand.PAPER,
    Hand.PAPER    - Hand.SCISSORS,
    Hand.SCISSORS - Hand.ROCK,
))


# Yeah this is redundant, but it's also super clear
DRAW = frozenset((
    Hand.ROCK     - Hand.ROCK,
    Hand.PAPER    - Hand.PAPER,
    Hand.SCISSORS - Hand.SCISSORS,
))


DEFEATED_BY = {
    Hand.ROCK:     Hand.PAPER,
    Hand.PAPER:    Hand.SCISSORS,
    Hand.SCISSORS: Hand.ROCK,
}

P1_POINT = -1
P2_POINT = 1

@dataclass
class PlayerMove:
    move: InitVar[str]
    hand: Hand = None
    art: str = None

    def __post_init__(self, move):
        self.hand = Hand[move.upper()]


    def to_dict(self):
        d = dataclasses.asdict(self)
        d["hand"] = d["hand"].name
        return d

class Player:

    def __init__(self, bot_runner, player_name, image, player_number):
        self.bot_runner = bot_runner
        self.player_name = player_name
        self.image = image
        self.player_number = str(player_number)

    def play_turn(self, game_id, history):
        try:
            output = self.bot_runner.run_container(
                self.image,
                command=[history],
                environment={'PLAYER_NUMBER': self.player_number},
                game_id=game_id,
            )
            return output
        except self.bot_runner.RunnerFailure:
            return None

    def to_dict(self):
        return {
            "name": self.player_name,
            "image": self.image
        }


def check_winner(p1_move: PlayerMove, p2_move: PlayerMove, move_counter: Counter) -> int:
    outcome = p1_move.hand - p2_move.hand

    # If you won, you won
    if outcome in PLAYER_ONE_WINS:
        return P1_POINT
    elif outcome in PLAYER_ONE_LOSES:
        return P2_POINT

    # if nobody won, whoever played that hand more often wins
    # We subtract 1 from move_count[hand] when p1 plays hand
    # We add 1 to move_count[hand] when p2 plays hand
    # this means that move_count[hand] will be
    #    < 0 if p1 has played it more
    #    > 0 if p2 has played it more
    #    = 0 if tied
    assert p1_move.hand == p2_move.hand
    tied_move = p1_move.hand
    if move_counter[tied_move] <= P1_POINT:
        return P1_POINT
    elif move_counter[tied_move] >= P2_POINT:
        return P2_POINT

    # Same as before, but this time we check for the beating move
    beating_move = DEFEATED_BY[tied_move]
    if move_counter[beating_move] <= P1_POINT:
        return P1_POINT
    elif move_counter[beating_move] > P2_POINT:
        return P2_POINT

    # Fuck it, random winner
    return random.choice([P1_POINT, P2_POINT])



class RockPaperScissorsGame:

    def __init__(self, game_id, player_one, player_two):
        self.player_one = player_one
        self.player_two = player_two

        self.move_counter = Counter()

        self.p1_moves = []
        self.p2_moves = []
        self.history = ''
        self.overall_winner = 0

        self.game_id = game_id

    def play_round(self):
        raw_p1_move = self.player_one.play_turn(self.game_id, self.history)
        p1_move = PlayerMove(**raw_p1_move) if raw_p1_move else None
        self.p1_moves.append(p1_move)

        raw_p2_move = self.player_two.play_turn(self.game_id, self.history)
        p2_move = PlayerMove(**raw_p2_move) if raw_p2_move else None
        self.p2_moves.append(p2_move)

        # Winner by forfeit
        if p1_move is None or p2_move is None:
            if p1_move is None and p2_move is None:
                # Everybody forfeit, no points for aybody
                self.history = f'{self.history};--0'
            elif p1_move is None:
                # Player 1 forefeit, point for Player 2
                self.history = f'{self.history};-{str(p2_move.hand)}2'
                self.overall_winner += P2_POINT
            elif p2_move is None:
                # Player 2 forefeit, point for Player 1
                self.history = f'{self.history};{str(p1_move.hand)}-1'
                self.overall_winner += P1_POINT
            return

        self.move_counter[p1_move.hand] += P1_POINT
        self.move_counter[p2_move.hand] += P2_POINT

        winner = check_winner(p1_move, p2_move, self.move_counter.copy())
        self.overall_winner += winner

        self.history = f'{self.history};{str(p1_move.hand)}{str(p2_move.hand)}{1 if winner == -1 else 2};'

    def play_game(self, rounds, callback=None):
        for _ in range(rounds):
            self.play_round()
            callback()

    @property
    def current_winner(self) -> Player:
        if self.overall_winner <= P1_POINT:
            winner = self.player_one
        elif self.overall_winner >= P2_POINT:
            winner = self.player_two
        else:
            winner = None

        return winner

    def stats(self):
        return {
            "game_id": self.game_id,
            "is_tie": self.overall_winner == 0,
            "winner": self.current_winner.player_name if self.current_winner else None,
            "players": {
                "player_one": self.player_one.to_dict(),
                "player_two": self.player_two.to_dict(),
            },
            "rounds": [
                {"player_one": p1.to_dict(), "player_two": p2.to_dict()}
                for p1, p2 in zip_longest(self.p1_moves, self.p2_moves)
            ]
        }
