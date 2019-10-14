# -*- coding: utf-8 -*-
"""chess

A library which is used for chess game GIF generation.

:copyright: @ 2019 by dantin.
:liencse: BSD

"""

# DEFAULT_STATE is the default state of a chess game.
DEFAULT_STATE = {
    'a8': 'br',
    'b8': 'bn',
    'c8': 'bb',
    'd8': 'bq',
    'e8': 'bk',
    'f8': 'bb',
    'g8': 'bn',
    'h8': 'br',
    'a7': 'bp',
    'b7': 'bp',
    'c7': 'bp',
    'd7': 'bp',
    'e7': 'bp',
    'f7': 'bp',
    'g7': 'bp',
    'h7': 'bp',
    'a2': 'wp',
    'b2': 'wp',
    'c2': 'wp',
    'd2': 'wp',
    'e2': 'wp',
    'f2': 'wp',
    'g2': 'wp',
    'h2': 'wp',
    'a1': 'wr',
    'b1': 'wn',
    'c1': 'wb',
    'd1': 'wq',
    'e1': 'wk',
    'f1': 'wb',
    'g1': 'wn',
    'h1': 'wr'
}

# COLUMNS is in [`a`, `h`] including.
COLUMNS = [chr(ord('a') + i) for i in range(8)]
# ROWS is in [`1`, `8`] including.
ROWS = [chr(ord('1') + i) for i in range(8)]

# COLORS stands for `black` and `white`.
COLORS = ('b', 'w')
# PIECES stands for chesspiece, which are `king`, `queen`, `bishop`, `knight`, `rock` and `pawn`.
PIECES = ('k', 'q', 'b', 'n', 'r', 'p')
