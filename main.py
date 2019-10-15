# -*- coding: utf-8 -*-
"""Bootstrap scripts for chess game utilities."""

import argparse
import logging
import os
import sys

from chess.board import Board
from chess.codec import load_moves_from_file, load_state_from_file, save_image_to_file
from chess.game import load_empty_state
from chess import list_supported_state_files, EMPTY_STATE


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
    parser.add_argument('-d', '--delay', default=1.62, help='delay between moves in seconds')
    parser.add_argument('-o', '--out', default=os.getcwd(), help='name of the output folder')
    parser.add_argument('-b', '--black_first', help='run black first', action='store_true')
    parser.add_argument('--black', default='#4B7399', help='color of the black in hex')
    parser.add_argument('--white', default='#EAE9D2', help='color of the white in hex')
    parser.add_argument('--font_path', default='/Library/Fonts/Arial.ttf',
                        help='path of the display font used in board')
    parser.add_argument('-v', '--verbose', help='print final board state', action='store_true')
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


def load_state(param):
    """parse_state returns."""
    supported_states = list_supported_state_files()
    state = load_empty_state()

    if os.path.isfile(param):
        LOGGER.debug('using init state by file')
        state_path = param
    elif param in supported_states.keys():
        LOGGER.debug('using %s state', param)
        state_path = supported_states[param]
    else:
        LOGGER.warning('using empty state, the init_state should be one of [%s]',
                       ' | '.join(supported_states.keys()))
        state_path = supported_states[EMPTY_STATE]

    current_state = load_state_from_file(state_path)

    for pos, piece in current_state.items():
        state[pos] = piece

    return state_path, state


def image_name(output_dir, filename):
    """output_image_name returns the output image name."""
    name, _ = os.path.splitext(os.path.basename(filename))
    output_file = os.path.join(output_dir, name + '.gif')
    return output_file, os.path.exists(output_file)


def main():
    """The main function."""
    args = parse_args()

    LOGGER.debug('load init state')
    state_path, state = load_state(args.init_state)

    LOGGER.debug('create chess board')
    board = Board(state, font_path=args.font_path,
                  white_color=args.white, black_color=args.black,
                  is_white_run=(not args.black_first),
                  verbose=args.verbose)

    if not args.path:
        name, is_exists = image_name(args.out, state_path)
        if is_exists:
            LOGGER.info('gif with name "%s" already exists, skip', name)
        else:
            moves = []
            images = board.render(moves)
            LOGGER.debug('creating "%s"...', name)
            save_image_to_file(name, images, args.delay)

    for path in args.path:
        if os.path.isfile(path):
            name, is_exists = image_name(args.out, path)
            if is_exists:
                LOGGER.info('gif with name "%s" already exists, skip', name)
                continue

            moves = load_moves_from_file(path)
            images = board.render(moves)
            LOGGER.debug('creating "%s"...', name)
            save_image_to_file(name, images, args.delay)
            # reset state.
            board.game.state = state


if __name__ == '__main__':
    init()
    main()
    LOGGER.debug('finish')
