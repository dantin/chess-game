# -*- coding: utf-8 -*-
"""files module contains functions that load data from files."""

import logging
import re

import imageio


LOGGER = logging.getLogger('ROOT')


def load_moves_from_file(pgn):
    """load_moves_from_file loads moves from pgn file."""
    LOGGER.debug('load moves from png file "%s"', pgn)
    with open(pgn) as f: # pylint: disable=invalid-name
        data = f.read()
        data = re.sub(r'\{.*?\}', '', data)  # remove png comments
        moves = re.findall(
            r'[a-h]x?[a-h]?[1-8]?=?[BKNRQ]?|O-O-?O?|[BKNRQ][a-h1-8]?[a-h1-8]?x?[a-h][1-8]',
            data)
        return [move.replace('x', '') for move in moves]


def load_state_from_file(file_path):
    """load_state_from_file load initial state from file."""
    LOGGER.debug('load state from file "%s"', file_path)
    with open(file_path) as f: # pylint: disable=invalid-name
        data = f.read()
        pairs = re.findall(
            r'[a-h][1-8]=[wb][bknrqp]',
            data)
        return dict(p.split('=') for p in pairs)


def save_image_to_file(file_path, images, duration):
    """save_image_to_file dump image serial in GIF format to file."""
    LOGGER.debug('create GIF image "%s"', file_path)
    imageio.mimsave(file_path, images, duration=duration)
