# -*- coding: utf-8 -*-
"""
main

Bootstrap scripts for chess game utilities.
"""

import argparse
import logging
import os
import sys

from chess.board import Board
from chess.game import load_state


LOGGER = logging.getLogger('ROOT')


def init():
    """ init runs initialization."""
    # logging setup.
    default_handler = logging.StreamHandler()
    default_handler.setFormatter(logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
    ))
    LOGGER.addHandler(default_handler)


def parse_args():
    """parse_args parses command line arguments."""

    parser = argparse.ArgumentParser()
    parser.add_argument('path', nargs='*', help='path to the pgn file/folder')
    parser.add_argument('-i', '--init_state', default='default',
                        help='initialize board state: empty, default, or target state file path')
    parser.add_argument('-d', '--delay', help='delay between moves in seconds', default=1.6)
    parser.add_argument('-o', '--out', help='name of the output folder', default=os.getcwd())
    parser.add_argument('--black', help='color of the black in hex', default='#4B7399')
    parser.add_argument('--white', help='color of the white in hex', default='#EAE9D2')
    parser.add_argument('--font_path', default='/Library/Fonts/Arial.ttf',
                        help='path of the display font used in board')
    parser.add_argument('-L', '--level', choices=('debug', 'info', 'warn'), default='info',
                        help='log level: debug, info')
    parser.add_argument('-V', '--version', help='print version information', action='store_true')
    args = parser.parse_args()

    if args.version:
        print('Build dynamic GIF picture of Chess Game, version 1.0')
        sys.exit(0)

    if args.level == 'debug':
        LOGGER.setLevel(logging.DEBUG)
    elif args.level == 'warn':
        LOGGER.setLevel(logging.WARNING)
    else:
        LOGGER.setLevel(logging.INFO)

    return args


def main():
    """The main function."""
    init()
    args = parse_args()

    LOGGER.debug('load state')
    state = load_state(args.init_state)

    LOGGER.debug('create chess board')
    board = Board(state, args.white, args.black, args.font_path)

    LOGGER.debug('render picture')
    if not args.path:
        board.render(args.out, args.delay)

    for path in args.path:
        if os.path.isfile(path):
            board.render(args.out, args.delay, path)

    LOGGER.debug('finish')


if __name__ == '__main__':
    main()
