# -*- coding: utf-8 -*-
"""board module contains classes and functions used while rendering board image."""

import logging
import os


from PIL import Image, ImageDraw, ImageFont
from numpy import array

from .game import Game
from . import COLORS, PIECES


LOGGER = logging.getLogger('ROOT')
# board
BOARD_EDGE = 480
SQUARE_EDGE = BOARD_EDGE // 8
# text font
FONT_SIZE = 15
BOARD_MARGIN = 20


def _get_text_loc(text, font, box):
    box_width, box_height = box[0], box[1]
    text_width, text_height = font.getsize(text)
    left = (box_width - text_width) // 2
    top = (box_height - text_height) // 2
    return left, top


def _show_copyright(initial_board, text='头条@淞南北丁巷',
                    font_path='/Library/Fonts/Arial Unicode.ttf'):
    font_size = int(FONT_SIZE * 2.5)
    LOGGER.debug('setup copyright font by "%s", size %s', font_path, font_size)

    board_image = initial_board.copy()
    draw = ImageDraw.Draw(board_image)
    ttfont = ImageFont.truetype(font_path, font_size)
    left, top = _get_text_loc(text, ttfont,
                              (BOARD_EDGE + 2 * BOARD_MARGIN, BOARD_EDGE + 2 * BOARD_MARGIN))
    draw.text((left, top), text, fill=(255, 0, 0), font=ttfont)

    return board_image


def coordinates_of_square(crd):
    """coordinates_of_square convert coordinations of square in board to pixel in image."""
    col = ord(crd[0]) - ord('a')
    row = int(crd[1]) - 1
    return (col * SQUARE_EDGE + BOARD_MARGIN, (7 - row) * SQUARE_EDGE + BOARD_MARGIN)


class Board(): # pylint: disable=too-few-public-methods
    """Board is a class that represents chess board."""

    def __init__(self, init_state,
                 white_color='#EAE9D2', black_color='#4B7399',
                 font_path='/Library/Fonts/Arial.ttf',
                 is_white_run=True,
                 show_copyright=True,
                 verbose=False):
        self.verbose = verbose
        self.show_copyright = show_copyright
        # initialize black and white squares.
        LOGGER.debug('setup squares by white color "%s", black color "%s"',
                     white_color, black_color)
        self.white_square = Image.new(
            'RGBA', (SQUARE_EDGE, SQUARE_EDGE), white_color)
        self.black_square = Image.new(
            'RGBA', (SQUARE_EDGE, SQUARE_EDGE), black_color)

        # initialize font.
        LOGGER.debug('setup border font by "%s", size %s', font_path, FONT_SIZE)
        self.ttfont = ImageFont.truetype(font_path, FONT_SIZE)

        # load chess images, king, queen, bishop, knight, rock and pawn.
        icons_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'asset')
        LOGGER.debug('setup chess icon by loading images from path "%s"', icons_dir)
        self.chesspieces = {c + p: Image.open(os.path.join(icons_dir, c + p + '.png'))
                            for c in COLORS for p in PIECES}

        self.game = Game(init_state, is_white_run=is_white_run)

    def _clear(self, image, crd):
        if (crd[0] < (BOARD_EDGE + BOARD_MARGIN)
                and crd[1] < (BOARD_EDGE + BOARD_MARGIN)):
            if (crd[0] + crd[1] - 2 * BOARD_MARGIN) % (SQUARE_EDGE * 2) == 0:
                image.paste(self.white_square, crd, self.white_square)
            else:
                image.paste(self.black_square, crd, self.black_square)

    def _init_board(self):

        # initialize board.
        width, height = BOARD_EDGE + 2 * BOARD_MARGIN, BOARD_EDGE + 2 * BOARD_MARGIN
        LOGGER.debug('setup board size by width "%s px", height "%s px"', width, height)
        initial_board = Image.new('RGB', (width, height))
        draw = ImageDraw.Draw(initial_board)

        # draw empty board.
        LOGGER.debug('draw empty board squares')
        for i in range(0 + BOARD_MARGIN, BOARD_EDGE + 2 * BOARD_MARGIN, SQUARE_EDGE):
            for j in range(0 + BOARD_MARGIN, BOARD_EDGE + 2 * BOARD_MARGIN, SQUARE_EDGE):
                self._clear(initial_board, (i, j))

        # draw text.
        LOGGER.debug('draw cord text on board margins')
        for i in range(8):
            col = SQUARE_EDGE * i
            text = chr(ord('a') + i)
            left, top = _get_text_loc(text, self.ttfont, (SQUARE_EDGE, BOARD_MARGIN))
            # draw top 'a' to 'h'
            draw.text(
                (col + BOARD_MARGIN + left, top), text,
                fill=(255, 255, 255), font=self.ttfont)
            # draw bottom 'a' to 'h'
            draw.text(
                (col + BOARD_MARGIN + left, BOARD_EDGE + BOARD_MARGIN),
                text, fill=(255, 255, 255), font=self.ttfont)

            text = chr(ord('8') - i)
            left, top = _get_text_loc(text, self.ttfont, (BOARD_MARGIN, SQUARE_EDGE))
            # draw left '1' to '8'
            draw.text(
                (left, BOARD_MARGIN + col + top),
                text, fill=(255, 255, 255), font=self.ttfont)
            draw.text(
                (BOARD_EDGE + BOARD_MARGIN + left, BOARD_MARGIN + col + top),
                text, fill=(255, 255, 255), font=self.ttfont)

        return initial_board

    def _update_state(self, initial_board):
        board_image = initial_board.copy()
        # draw chess.
        for pos, piece in self.game.state.items():
            if piece:
                row = SQUARE_EDGE * (ord(pos[0]) - ord('a'))
                col = SQUARE_EDGE * (8 - int(pos[1]))
                img = self.chesspieces[piece]
                board_image.paste(img, (row + BOARD_MARGIN, col + BOARD_MARGIN), img)
        return board_image


    def _apply_move(self, board_image, current, previous):
        changed = [s for s in current.keys() if current[s] != previous[s]]

        for square in changed:
            crd = coordinates_of_square(square)
            self._clear(board_image, crd)

            if current[square] != '':
                pt = current[square] # pylint: disable=invalid-name
                img = self.chesspieces[pt]
                board_image.paste(img, crd, img)

    def _create_images(self, initial_board, moves):
        board_image = initial_board.copy()
        images = [array(board_image)]

        for move in moves:
            LOGGER.debug('move %s', move)
            previous = self.game.state.copy()
            self.game.apply(move)
            self._apply_move(board_image, self.game.state, previous)
            images.append(array(board_image))

        return images

    def _print_state(self):
        for pos, chesspiece in self.game.state.items():
            if chesspiece != '':
                print('{}={}'.format(pos, chesspiece))

    def render(self, moves, copyright_slide=2):
        """render generate GIF image serial using moves."""
        LOGGER.debug('initialize board state')
        empty_board = self._init_board()
        initial_board = self._update_state(empty_board)

        LOGGER.debug('filter out "x" in each move')
        moves = [x.replace('x', '') for x in moves]

        LOGGER.debug('render moves on board')
        images = self._create_images(initial_board, moves)
        LOGGER.debug('len of images: %s, show_copyright: %s', len(images), self.show_copyright)

        if len(images) > 1 and self.show_copyright:
            # avoid appending copyright slide if there is only one image.
            LOGGER.debug('append copyright')
            _copyright = _show_copyright(empty_board)
            images += [_copyright] * copyright_slide

        if self.verbose:
            self._print_state()

        return images
