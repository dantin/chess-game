# -*- coding: utf-8 -*-
"""
main

Bootstrap scripts for chess game utilities.
"""

import argparse
import logging
import os
import sys

from chess import DEFAULT_STATE, ROWS, COLUMNS
from chess.board import Board
from chess.files import load_state_from_file


LOGGER = logging.getLogger('ROOT')


def load_state(arg):
    """
    load_state

    Load state using argument.
    """
    valid_params = ('empty', 'default')

    state = {c + r: '' for c in COLUMNS for r in ROWS}
    current_state = {}

    if os.path.isfile(arg):
        LOGGER.debug('using init state by file')
        current_state = load_state_from_file(arg)
    elif arg not in valid_params:
        LOGGER.warning('init_state should be one of [%s]', ' | '.join(valid_params))
        LOGGER.debug('using empty state')
    elif arg == 'default':
        LOGGER.debug('using default state')
        current_state = DEFAULT_STATE

    for pos, piece in current_state.items():
        state[pos] = piece

    return state


def init():
    """
    init

    script initialization.
    """
    # logging setup.
    default_handler = logging.StreamHandler()
    default_handler.setFormatter(logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
    ))
    LOGGER.addHandler(default_handler)


def parse_args():
    """
    parse_args

    parses command line arguments.
    """

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
    """
    main

    The main function.
    """
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
