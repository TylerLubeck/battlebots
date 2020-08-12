import os
from pathlib import Path

import typer

from battlebots.art_to_gif import create_frame, frames_to_gif

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

@main.callback()
def callback():
    """Placeholder"""
    pass
