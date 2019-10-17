# -*- coding: utf-8 -*-
"""game module contains classes and functions which represents a chess game."""

import logging

from . import ROWS, COLUMNS


LOGGER = logging.getLogger('ROOT')


def load_empty_state():
    """load_empty_state returns an empty board state."""
    return {c + r: '' for c in COLUMNS for r in ROWS}


def check_knight_move(lhs, rhs):
    """check_knight_move checks whether a knight move is ok."""
    col_diff = abs(ord(lhs[0]) - ord(rhs[0]))
    row_diff = abs(int(lhs[1]) - int(rhs[1]))
    return (col_diff == 2 and row_diff == 1) or (col_diff == 1 and row_diff == 2)


def check_line(state, lhs, rhs):
    """check_line checks whether a line move is ok."""
    row_1, col_1 = int(lhs[1]), lhs[0]
    row_2, col_2 = int(rhs[1]), rhs[0]

    if row_1 == row_2:
        i1, i2 = ord(col_1) - ord('a'), ord(col_2) - ord('a')
        return all(state[COLUMNS[i] + str(row_1)] == ''
                   for i in range(min(i1, i2) + 1, max(i1, i2)))
    if col_1 == col_2:
        return all(state[col_1 + str(i)] == ''
                   for i in range(min(row_1, row_2) + 1, max(row_1, row_2)))

    return False


def check_diagonal(state, lhs, rhs):
    """check_line checks whether a diagonal move is ok."""
    row_1, col_1 = int(lhs[1]), ord(lhs[0]) - ord('a')
    row_2, col_2 = int(rhs[1]), ord(rhs[0]) - ord('a')
    if abs(col_1 - col_2) == abs(row_1 - row_2):
        if (col_1 > col_2 and row_1 > row_2) or (col_2 > col_1 and row_2 > row_1):
            min_c = min(col_1, col_2)
            min_r = min(row_1, row_2)
            return all(state[COLUMNS[min_c + i] + str(min_r + i)] == ''
                       for i in range(1, abs(col_1 - col_2)))
        if col_1 > col_2 and row_2 > row_1:
            return all(state[COLUMNS[col_2 + i] + str(row_2 - i)] == ''
                       for i in range(1, col_1 - col_2))
        return all(state[COLUMNS[col_2 - i] + str(row_2 + i)] == ''
                   for i in range(1, col_2 - col_1))

    return False


class Game():  # pylint: disable=too-few-public-methods
    """Game is a class that represents chess game."""

    def __init__(self, state, is_white_run=True):
        self.is_white_run = is_white_run
        self.state = state

    def _update_state(self, src, dest, pt):
        self.state[src] = ''
        self.state[dest] = pt

    def _find_non_pawn(self, move, to, piece):
        if len(move) == 5:
            return move[1:3]

        p = piece[1]
        key = '' if len(move) == 3 else move[1]

        if p == 'r':
            return next(s for s, pt in self.state.items()
                        if pt == piece and key in s and check_line(self.state, s, to))
        if p == 'b':
            return next(s for s, pt in self.state.items()
                        if pt == piece and key in s and check_diagonal(self.state, s, to))
        if p == 'n':
            LOGGER.debug("move: %s, to: %s, pt: %s", move, to, piece)
            return next(s for s, pt in self.state.items()
                        if pt == piece and key in s and check_knight_move(s, to))
        return next(s for s, pt in self.state.items()
                    if pt == piece and key in s and (check_line(self.state, s, to) or
                                                     check_diagonal(self.state, s, to)))

    def _find_pawn(self, move):
        pt = 'wp' if self.is_white_run else 'bp'
        c = move[-2]
        r = int(move[-1])

        if len(move) == 2:
            # just pawn move.
            if self.is_white_run:
                origin = c + next(str(i) for i in range(r, 0, -1) if self.state[c + str(i)] == pt)
            else:
                origin = c + next(str(i) for i in range(r, 9) if self.state[c + str(i)] == pt)
        else:
            # with others.
            if self.state[move[-2:]] != '':
                origin = move[0] + (str(r - 1) if self.is_white_run else str(r + 1))
            else:
                nps = c + (str(r - 1)) if self.is_white_run else str(r + 1)
                self.state[nps] = ''
                origin = move[0] + nps[-1]

        return origin

    def _castle(self, move):
        row, color = ('1', 'w') if self.is_white_run else ('8', 'b')
        if move.count('O') == 2:
            r = 'h' + row
            k_to = 'g' + row
            r_to = 'f' + row
        else:
            r = 'a' + row
            k_to = 'c' + row
            r_to = 'd' + row

        self._update_state('e' + row, k_to, color + 'k')
        self._update_state(r, r_to, color + 'r')

    def _promote(self, move):
        pt = ('w' if self.is_white_run else 'b') + move[-1].lower()
        origin = move[0] + ('7' if self.is_white_run else '2')
        self._update_state(origin, move[-4:-2], pt)

    def apply(self, move):
        """apply make move on game."""
        if 'O' in move:
            self._castle(move)
        elif '=' in move:
            self._promote(move)
        else:
            dest = move[-2:]
            if move.islower():
                pt = ('w' if self.is_white_run else 'b') + 'p'
                origin = self._find_pawn(move)
            else:
                pt = ('w' if self.is_white_run else 'b') + move[0].lower()
                origin = self._find_non_pawn(move, dest, pt)

            self._update_state(origin, dest, pt)

        self.is_white_run = not self.is_white_run
