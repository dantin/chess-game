# -*- coding: utf-8 -*-

import logging
import os

import imageio

from PIL import Image, ImageDraw, ImageFont
from numpy import array


logger = logging.getLogger('ROOT')


class Board():
    # board
    BOARD_EDGE = 480
    SQUARE_EDGE = BOARD_EDGE // 8
    # text font
    FONT_SIZE = 15
    BOARD_MARGIN = 20

    def __init__(self, white_color='#EAE9D2', black_color='#4B7399', font_path='/Library/Fonts/Arial.ttf'):
        # initialize black and white squares.
        logger.debug('setup squares by white color "%s", black color "%s"', white_color, black_color)
        self.white_square = Image.new(
            'RGBA', (self.SQUARE_EDGE, self.SQUARE_EDGE), white_color)
        self.black_square = Image.new(
            'RGBA', (self.SQUARE_EDGE, self.SQUARE_EDGE), black_color)

        # initialize board.
        width, height = self.BOARD_EDGE + 2 * self.BOARD_MARGIN, self.BOARD_EDGE + 2 * self.BOARD_MARGIN
        logger.debug('setup board size by width "%s px", height "%s px"', width, height)
        self.initial_board = Image.new('RGB', (width, height))
        self.draw = ImageDraw.Draw(self.initial_board)

        # initialize font.
        logger.debug('setup font by "%s"', font_path)
        self.ttfont = ImageFont.truetype(font_path, self.FONT_SIZE)

        # load chess images, king, queen, bishop, knight, rock and pawn.
        chess_icon_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'asset')
        logger.debug('setup chess icon by loading images from path "%s"', chess_icon_dir)
        colors = ('b', 'w')
        pieces = ('k', 'q', 'b', 'n', 'r', 'p')
        self.chesspieces = {c + p: Image.open(os.path.join(chess_icon_dir, c + p + '.png')) for c in colors for p in pieces}

    def _clear(self, image, crd):
        if (crd[0] < (self.BOARD_EDGE + self.BOARD_MARGIN)
                and crd[1] < (self.BOARD_EDGE + self.BOARD_MARGIN)):
            if (crd[0] + crd[1] - 2 * self.BOARD_MARGIN) % (self.SQUARE_EDGE * 2) == 0:
                image.paste(self.white_square, crd, self.white_square)
            else:
                image.paste(self.black_square, crd, self.black_square)

    def init_board(self, init_state):
        # draw empty board.
        logger.debug('draw empty board squares')
        for i in range(0 + self.BOARD_MARGIN, self.BOARD_EDGE + 2 * self.BOARD_MARGIN, self.SQUARE_EDGE):
            for j in range(0 + self.BOARD_MARGIN, self.BOARD_EDGE + 2 * self.BOARD_MARGIN, self.SQUARE_EDGE):
                self._clear(self.initial_board, (i, j))

        # draw chess.
        for i in ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'):
            for j in ('1', '2', '3', '4', '5', '6', '7', '8'):
                pos = i + j
                if init_state[pos]:
                    row = self.SQUARE_EDGE * (ord(i) - ord('a'))
                    col = self.SQUARE_EDGE * abs(ord(j) - ord('8'))
                    img = self.chesspieces[init_state[pos]]
                    self.initial_board.paste(img, (row + self.BOARD_MARGIN, col + self.BOARD_MARGIN), img)
    
        # draw text.
        logger.debug('draw cord text on board margins')
        for i in range(8):
            col = self.SQUARE_EDGE * i
            text = chr(ord('a') + i)
            width, height = self.ttfont.getsize(text)
            padding_vert = (self.BOARD_MARGIN - height) // 2
            padding_hor = (self.SQUARE_EDGE - width) // 2
            # draw top 'a' to 'h'
            self.draw.text(
                (col + self.BOARD_MARGIN + padding_hor, padding_vert), text,
                fill=(255, 255, 255), font=self.ttfont)
            # draw bottom 'a' to 'h'
            self.draw.text(
                (col + self.BOARD_MARGIN + padding_hor, self.BOARD_EDGE + self.BOARD_MARGIN),
                text, fill=(255, 255, 255), font=self.ttfont)
    
            text = chr(ord('8') - i)
            width, height = self.ttfont.getsize(text)
            padding_vert = (self.BOARD_MARGIN - height) // 2
            padding_hor = (self.SQUARE_EDGE - width) // 2
            # draw left '1' to '8'
            self.draw.text(
                (self.BOARD_MARGIN - padding_vert - width, self.BOARD_MARGIN + col + padding_hor),
                text, fill=(255, 255, 255), font=self.ttfont)
            self.draw.text(
                (self.BOARD_EDGE + self.BOARD_MARGIN + padding_vert, self.BOARD_MARGIN + col + padding_hor),
                text, fill=(255, 255, 255), font=self.ttfont)

    def _create_gif(self, filename, moves, duration):
        board_image = self.initial_board.copy()
        images = [array(board_image)]
        imageio.mimsave(filename, images, duration=duration)

    def render(self, output_dir, duration, pgn=None):
        if not pgn:
            name = 'board.gif'
            moves = []
        else:
            filename, extension = os.path.splitext(os.path.basename(pgn))
            name = filename + '.gif'
            # TODO: load png
            moves = []
        if name in os.listdir(output_dir):
            logger.info('gif with name "%s" already exists, skip', name)
        else:
            logger.info('creating "%s"...', name)
            self._create_gif(os.path.join(output_dir, name), moves, duration)
