# -*- coding: utf-8 -*-
"""Bootstrap scripts for chess game utilities."""

import argparse
import logging
import os
import sys

from chess.board import Board
from chess.codec import load_moves_from_file, load_state_from_file, save_image_to_file
from chess.game import load_empty_state
from chess import list_supported_state_files, EMPTY_STATE, __version__


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

    parser = argparse.ArgumentParser('main.py')
    subparsers = parser.add_subparsers(help='sub-command help')

    parser_image = subparsers.add_parser('image', help='tool that generates GIF picture')
    parser_image.add_argument('path', nargs='*', help='path to the pgn file/folder')
    parser_image.add_argument('-i', '--init_state', default='default',
                              help='initialize board state:'
                              ' empty, default, or target state file path')
    parser_image.add_argument('-d', '--delay', default=1.62, help='delay between moves in seconds')
    parser_image.add_argument('-o', '--out', default=os.getcwd(), help='name of the output folder')
    parser_image.add_argument('-b', '--black_first', help='run black first', action='store_true')
    parser_image.add_argument('--black', default='#4B7399', help='color of the black in hex')
    parser_image.add_argument('--white', default='#EAE9D2', help='color of the white in hex')
    parser_image.add_argument('--font_path', default='/Library/Fonts/Arial.ttf',
                              help='path of the display font used in board')
    parser_image.add_argument('-v', '--verbose', help='print final board state',
                              action='store_true')
    parser_image.add_argument('-L', '--level', choices=('debug', 'info', 'warn'), default='info',
                              help='log level: debug, info')
    parser_image.set_defaults(func=run_image)

    parser_manual = subparsers.add_parser('manual', help='tool that loads chess manual text')
    parser_manual.add_argument('path', nargs='*', help='path to the pgn file/folder')
    parser_manual.add_argument('-n', '--num', default=1, type=int, help='start number')
    parser_manual.add_argument('-b', '--black_first', help='run black first', action='store_true')
    parser_manual.add_argument('-L', '--level', choices=('debug', 'info', 'warn'), default='info',
                               help='log level: debug, info')
    parser_manual.set_defaults(func=run_manual)

    parser.add_argument('-V', '--version', help='print version information', action='store_true')

    args = parser.parse_args()

    if args.version:
        print('Tools of Chess Game, version ', __version__)
        sys.exit(0)

    return args


def logger(func):
    """logger decorator sets logger level."""
    def wrapper(args):
        level = args.level
        if level == 'debug':
            LOGGER.setLevel(logging.DEBUG)
        elif level == 'warn':
            LOGGER.setLevel(logging.WARNING)
        else:
            LOGGER.setLevel(logging.INFO)
        func(args)

    return wrapper


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
        LOGGER.debug('init state should be one of [%s]',
                     '|'.join(supported_states.keys()))
        LOGGER.debug('using empty state by default')
        state_path = supported_states[EMPTY_STATE]

    current_state = load_state_from_file(state_path)
    state.update(current_state)

    return state_path, state


def image_name(output_dir, filename):
    """output_image_name returns the output image name."""
    name, _ = os.path.splitext(os.path.basename(filename))
    output_file = os.path.join(output_dir, name + '.gif')
    return output_file, os.path.exists(output_file)


@logger
def run_image(args):
    """image sub-command function."""

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


@logger
def run_manual(args):
    """manual sub-command function."""
    LOGGER.debug('run manual')

    move_holder = '...'
    item_sep, move_sep = ', ', '; '

    def pair_chunks(moves, idx=1):
        step = 2
        for i in range(0, len(moves), step):
            chunk = moves[i:i + step]
            if len(chunk) == 1:
                chunk += [move_holder]
            yield '{}. {}'.format(idx, item_sep.join(chunk))
            idx += 1

    for path in args.path:
        if os.path.isfile(path):
            moves = load_moves_from_file(path)
            if args.black_first:
                moves = [move_holder] + moves
            print(move_sep.join(pair_chunks(moves, idx=args.num)))


def main():
    """The main function."""
    args = parse_args()
    args.func(args)


if __name__ == '__main__':
    init()
    main()
    LOGGER.debug('finish')
