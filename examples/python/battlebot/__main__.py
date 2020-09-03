import argparse
import json
import os
import sys

from .app import play_turn


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("history", type=str, default="", nargs='?')
    args = parser.parse_args(argv)

    player_number = os.environ.get('PLAYER_NUMBER', '-')
    move = play_turn(args.history, player_number)
    print(move.to_json())


main(sys.argv[1:])
