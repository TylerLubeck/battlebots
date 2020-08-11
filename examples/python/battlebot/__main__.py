import argparse
import json
import sys

from .app import play_turn


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("history", type=str, default="", nargs='?')
    args = parser.parse_args(argv)

    move = play_turn(args.history)
    print(move.to_json())


main(sys.argv[1:])
