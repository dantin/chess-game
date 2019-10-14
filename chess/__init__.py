# -*- coding: utf-8 -*-
"""chess

A library which is used for chess game GIF generation.

:copyright: @ 2019 by dantin.
:liencse: BSD

"""

# chesspieces
KING, QUEEN, BISHOP, KNIGHT, ROCK, PAWN = 'k', 'q', 'b', 'n', 'r', 'p'
# COLORS
BLACK, WHITE = 'b', 'w'

# COLORS stands for `black` and `white`.
COLORS = (BLACK, WHITE)
# PIECES stands for chesspiece, which are `king`, `queen`, `bishop`, `knight`, `rock` and `pawn`.
PIECES = (KING, QUEEN, BISHOP, KNIGHT, ROCK, PAWN)

# DEFAULT_STATE is the default state of a chess game.
DEFAULT_STATE = {
    'a8': BLACK + ROCK,
    'b8': BLACK + KNIGHT,
    'c8': BLACK + BISHOP,
    'd8': BLACK + QUEEN,
    'e8': BLACK + KING,
    'f8': BLACK + BISHOP,
    'g8': BLACK + KNIGHT,
    'h8': BLACK + ROCK,
    'a7': BLACK + PAWN,
    'b7': BLACK + PAWN,
    'c7': BLACK + PAWN,
    'd7': BLACK + PAWN,
    'e7': BLACK + PAWN,
    'f7': BLACK + PAWN,
    'g7': BLACK + PAWN,
    'h7': BLACK + PAWN,
    'a2': WHITE + PAWN,
    'b2': WHITE + PAWN,
    'c2': WHITE + PAWN,
    'd2': WHITE + PAWN,
    'e2': WHITE + PAWN,
    'f2': WHITE + PAWN,
    'g2': WHITE + PAWN,
    'h2': WHITE + PAWN,
    'a1': WHITE + ROCK,
    'b1': WHITE + KNIGHT,
    'c1': WHITE + BISHOP,
    'd1': WHITE + QUEEN,
    'e1': WHITE + KING,
    'f1': WHITE + BISHOP,
    'g1': WHITE + KNIGHT,
    'h1': WHITE + ROCK
}

# COLUMNS is in [`a`, `h`] including.
COLUMNS = [chr(ord('a') + i) for i in range(8)]
# ROWS is in [`1`, `8`] including.
ROWS = [chr(ord('1') + i) for i in range(8)]
