import logging
from pathlib import Path  # For Typing
import string
from typing import Any
from typing import BinaryIO
from typing import List
from typing import Union

import PIL
import PIL.Image
import PIL.ImageFont
import PIL.ImageDraw

PIXEL_ON = 0
PIXEL_OFF = 255

logger = logging.getLogger(__name__)

def _point_to_pixel(point: int) -> int:
    """IDK but it was in the example so"""
    return int(round(point * 96.0 / 72))


def _get_font(font_path='cour.ttf', font_size=20) -> PIL.ImageFont.ImageFont:
    """Load the specified font, or fallback to the system default

    Args:
        font_path: The path to the truetype font file to load
        font_size: The size of the font to load

    Returns:
        A loaded ImageFont file

    Notes:
        If the specified font_path is not available, we load the system default font
    """
    try:
        font = PIL.ImageFont.truetype(font_path, size=font_size)
    except IOError:
        font = PIL.ImageFont.load_default()
        logger.info("Failed to load font, using default", exc_info=True)

    return font


def _get_size(lines: List[str], font: PIL.ImageFont.ImageFont) -> (int, int, int):
    """Determine image width, height, and line spacing

    Args:
        lines: The lines that will make up the ASCII Image
        font: The font to be used

    Returns:
        (width, height, line_spacing)
    """
    max_width_line = max(lines, key=lambda s: font.getsize(s)[0])
    test_string = string.ascii_uppercase
    max_height = _point_to_pixel(font.getsize(string.ascii_uppercase)[1])
    max_width = _point_to_pixel(font.getsize(max_width_line)[0])

    height = max_height * len(lines)
    width = int(round(max_width + 10))  # Little padding makes it nicer to see
    line_spacing = int(round(max_height * 0.8))

    return width, height, line_spacing


def create_frame(art: List[str]) -> PIL.Image.Image:
    """Create an image from the ascii art array

    Args:
        art: A list of strings comprising an ASCII art image

    Returns:
        An image object with the rendered ASCII art
    """
    lines = [l.rstrip() for l in art]  # We don't need trailing whitespace on the right hand side

    font = _get_font()
    width, height, line_spacing = _get_size(lines, font)

    # 'P' means palette image
    image = PIL.Image.new('P', (width, height), color=PIXEL_OFF)
    draw = PIL.ImageDraw.Draw(image)

    vertical_position = 5  # Start 5 pixels from the top
    horizontal_position = 5  # Always start 5 pixels from the left
    for line in lines:
        position = (horizontal_position, vertical_position)
        draw.text(position, line, fill=PIXEL_ON, font=font)
        vertical_position += line_spacing

    image = image.crop(image.getbbox())
    return image


def frames_to_gif(filename: Union[str, Path, BinaryIO], frames: List[PIL.Image.Image], frame_length=150):
    """Generate a gif file from the supplied frames

    Args:
      filename: The file path, or file pointer, to save the file to.
      frames: A list of PIL images to include in the gif
      frame_length: The amount of time, in ms, that a frame is displayed for
    """
    frames[0].save(filename, save_all=True, append_images=frames[1:], optimize=False, duration=frame_length, loop=0)
