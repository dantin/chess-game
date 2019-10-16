# -*- coding: utf-8 -*-
"""chess

A library which is used for chess game GIF generation.

:copyright: @ 2019 by dantin.
:liencse: BSD

"""

import os


__version__ = '1.0.0-git'

# chesspieces
KING, QUEEN, BISHOP, KNIGHT, ROCK, PAWN = 'k', 'q', 'b', 'n', 'r', 'p'
# COLORS
BLACK, WHITE = 'b', 'w'

# COLORS stands for `black` and `white`.
COLORS = (BLACK, WHITE)
# PIECES stands for chesspiece, which are `king`, `queen`, `bishop`, `knight`, `rock` and `pawn`.
PIECES = (KING, QUEEN, BISHOP, KNIGHT, ROCK, PAWN)

# COLUMNS is in [`a`, `h`] including.
COLUMNS = [chr(ord('a') + i) for i in range(8)]
# ROWS is in [`1`, `8`] including.
ROWS = [chr(ord('1') + i) for i in range(8)]

EMPTY_STATE = 'empty'


def list_supported_state_files():
    """load_supported_states returns predefined state dict."""
    states_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'state')
    return dict((os.path.splitext(os.path.basename(fn))[0], os.path.join(states_dir, fn))
                for fn in os.listdir(states_dir))
