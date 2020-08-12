import os
from pathlib import Path
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
    gif_output_dir: Path = typer.Argument(..., help="The directory to output gifs in"),
    rounds: int = typer.Option(11, "--rounds"),
    debug: bool = typer.Option(False, "--debug"),
    skip_gif: bool = typer.Option(False, "--skip-gif"),
):
    """Run a Battle"""
    bot_runner = DockerRunner()
    p1 = Player(bot_runner, player_one_name, player_one_image)
    p2 = Player(bot_runner, player_two_name, player_two_image)
    game = RockPaperScissorsGame(p1, p2)

    typer.secho("Starting Game!", err=True)
    with typer.progressbar(range(rounds)) as progress:
        for round in progress:
            game.play_round()

    typer.secho(f"The winner is {game.current_winner}", err=True)
    if skip_gif:
        return

    typer.secho(f"Generating Gifs")

    valid_p1_art = [m.art for m in game.p1_moves if m and m.art]
    valid_p2_art = [m.art for m in game.p1_moves if m and m.art]

    if valid_p1_art:
        p1_frames = []
        for art in valid_p1_art:
            p1_frames.append(create_frame(art))
        frames_to_gif(gif_output_dir / 'p1.gif', p1_frames, 120)

    if valid_p2_art:
        p2_frames = []
        for art in valid_p2_art:
            p2_frames.append(create_frame(art))
        frames_to_gif(gif_output_dir / 'p2.gif', p2_frames, 120)
