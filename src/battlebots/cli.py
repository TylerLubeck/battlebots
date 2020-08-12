import os
from pathlib import Path
import uuid
import random
import json
import string
from typing import List
from typing import Optional

import typer

from battlebots.art_to_gif import create_frame, frames_to_gif
from battlebots.games.rps import RockPaperScissorsGame
from battlebots.games.rps import Player
from battlebots.runners.docker import DockerRunner

main = typer.Typer()

@main.command()
def generate_gif(
    directory: Path = typer.Argument(..., help="The directory to scan for ascii art"),
    output: Path = typer.Argument(..., help="The name of the file the gif should be written to"),
    frame_length: int = typer.Option(default=150, help="The length of a frame, in ms"),
):
    """Generate an animated GIF from a series of ascii art files

    The files in DIRECTORY will be alphabetized, turned in to images, and smashed together to create an animated GIF

    The resulting gif will be written to OUTPUT
    """
    file_names = []
    typer.secho("Loading Image Files...")
    with os.scandir(directory) as it, typer.progressbar(it) as progress:
        for entry in progress:
            if entry.is_file() and entry.name.endswith('.ascii'):
                file_names.append(entry.path)

    file_names.sort()

    typer.secho("Generating Frames...")
    frames = []
    with typer.progressbar(file_names) as progress:
        for fname in progress:
            with open(fname, 'r') as f:
                frames.append(create_frame(f.readlines()))

    typer.secho("Writing GIF...")
    frames_to_gif(output, frames, frame_length)
    
    typer.secho("done", bold=True, fg="green")


@main.command()
def rps(
    player_one_name: str = typer.Argument(..., help="The name of Player One"),
    player_one_image: str = typer.Argument(..., help="The docker image for the Player One"),
    player_two_name: str = typer.Argument(..., help="The name of Player Two"),
    player_two_image: str = typer.Argument(..., help="The docker image for the Player Two"),
    output_dir: Path = typer.Argument(..., help="The directory to output game results to"),
    rounds: int = typer.Option(11, "--rounds"),
    debug: bool = typer.Option(False, "--debug"),
    skip_gif: bool = typer.Option(False, "--skip-gif"),
    game_id: str = typer.Option(''.join(random.choice(string.ascii_lowercase) for _ in range(10))),
):
    """Run a Battle"""
    bot_runner = DockerRunner()
    p1 = Player(bot_runner, player_one_name, player_one_image)
    p2 = Player(bot_runner, player_two_name, player_two_image)

    typer.secho("Starting Game!", err=True)
    game = RockPaperScissorsGame(game_id, p1, p2)

    try:
        with typer.progressbar(length=rounds) as progress:
            # Some wonkiness to keep the game play and cli separate
            progress_iter = iter(progress)
            game.play_game(rounds=rounds, callback=lambda: next(progress_iter))
    finally:
        bot_runner.cleanup(game_id)


    valid_p1_art = [m.art for m in game.p1_moves if m and m.art]
    valid_p2_art = [m.art for m in game.p1_moves if m and m.art]

    if not skip_gif and valid_p1_art:
        p1_path = output_dir / 'p1.gif'
        typer.secho(f"Generating GIF for {p1.player_name} at {p1_path}", color=green, err=True)
        p1_frames = []
        for art in valid_p1_art:
            p1_frames.append(create_frame(art))
        frames_to_gif(p1_path, p1_frames, 120)

    if not skip_gif and valid_p2_art:
        p2_path = output_dir / 'p2.gif'
        typer.secho(f"Generating GIF for {p2.player_name} at {p2_path}", color=green, err=True)
        p2_frames = []
        for art in valid_p2_art:
            p2_frames.append(create_frame(art))
        frames_to_gif(p2_path, p2_frames, 120)

    winner = game.current_winner
    if winner is not None:
        typer.secho(f"{winner.player_name} Wins!", color="green")
    else:
        typer.secho("Draw!", color="red")

    with open(output_dir / 'results.json', 'w') as f:
        stats = game.stats()
        json.dump(game.stats(), f)
