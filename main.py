# -*- coding: utf-8 -*-

import argparse
import glob
import logging
import os
import sys

from chess import DEFAULT_STATE, ROWS, COLUMNS
from chess.board import Board
from chess.files import load_state_from_file


logger = logging.getLogger('ROOT')


def load_state(arg):
    valid_params = ('empty', 'default')

    state = {c + r: '' for c in COLUMNS for r in ROWS}
    current_state = {}

    if os.path.isfile(arg):
        logger.debug('using init state by file')
        current_state = load_state_from_file(arg)
    elif arg not in valid_params:
        logger.warning('init_state should be one of [%s]', ' | '.join(valid_params))
        logger.debug('using empty state')
    elif arg == 'default':
        logger.debug('using default state')
        current_state = DEFAULT_STATE

    for cord, tp in current_state.items():
        state[cord] = tp

    return state


def parse_args():
    # logging setup.
    default_handler = logging.StreamHandler()
    default_handler.setFormatter(logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
    ))
    logger.addHandler(default_handler)

    parser = argparse.ArgumentParser()
    parser.add_argument('path', nargs='*', help='path to the pgn file/folder')
    parser.add_argument('-i', '--init_state', help='initialize board state: empty, default, or the target state file path', default='default')
    parser.add_argument('-d', '--delay', help='delay between moves in seconds', default=1.6)
    parser.add_argument('-o', '--out', help='name of the output folder', default=os.getcwd())
    parser.add_argument('--black', help='color of the black in hex', default='#4B7399')
    parser.add_argument('--white', help='color of the white in hex', default='#EAE9D2')
    parser.add_argument('--font_path', help='path of the display font used in board', default='/Library/Fonts/Arial.ttf')
    parser.add_argument('-L','--level', choices=('debug', 'info', 'warn'), help='log level: debug, info', default='info')
    parser.add_argument('-V','--version', help='print version information', action='store_true')
    args = parser.parse_args()

    if args.version:
        print('Build dynamic GIF picture of Chess Game, version 1.0')
        sys.exit(0)

    if args.level == 'debug':
        logger.setLevel(logging.DEBUG)
    elif args.level == 'warn':
        logger.setLevel(logging.WARNING)
    else:
        logger.setLevel(logging.INFO)

    return args


def main():
    args = parse_args()

    logger.debug('load state')
    state = load_state(args.init_state)

    logger.debug('create chess board')
    board = Board(args.white, args.black, args.font_path)

    logger.debug('initialize board state')
    board.init_board(state)

    logger.debug('render picture')
    if not args.path:
        board.render(args.out, args.delay)

    for path in args.path:
        if os.path.isfile(path):
            board.render(args.out, args.delay, path)

    logger.debug('finish')


if __name__ == '__main__':
    main()
