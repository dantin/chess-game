# -*- coding: utf-8 -*-

from . import COLUMNS


class Game():

    def __init__(self, state):
        self.is_white_run = True
        self.state = state

    def _check_knight_move(self, sqr1, sqr2):
        cd = abs(ord(sqr1[0]) - ord(sqr2[0]))
        rd = abs(int(sqr1[1]) - int(sqr2[1]))
        return (cd == 2 and rd == 1) or (cd == 1 and rd == 2)

    def _check_line(self, sqr1, sqr2):
        c1 = sqr1[0]
        c2 = sqr2[0]
        r1 = int(sqr1[1])
        r2 = int(sqr2[1])
        if r1 == r2:
            i1, i2 = ord(c1) - ord('a'), ord(c2) - ord('a')
            return all(self.state[COLUMNS[i] + str(r1)] == '' for i in range(min(i1, i2) + 1, max(i1, i2)))
        elif c1 == c2:
            return all(self.state[c1 + str(i)] == '' for i in range(min(r1, r2) + 1, max(r1, r2)))

        return False

    def _check_diagonal(self, sqr1, sqr2):
        c1 = ord(sqr1[0]) - ord('a')
        c2 = ord(sqr2[0]) - ord('a')
        r1 = int(sqr1[1])
        r2 = int(sqr2[1])
        if abs(c1 - c2) == abs(r1 - r2):
            if c1 > c2 and r1 > r2 or c2 > c1 and r2 > r1:
                min_c = min(c1, c2)
                min_r = min(r1, r2)
                return all(self.state[COLUMNS[min_c + i] + str(min_r + i)] == '' for i in range(1, abs(c1 - c2)))
            elif c1 > c2 and r2 > r1:
                return all(self.state[COLUMNS[c2 + i] + str(r2 - i)] == '' for i in range(1, c1 - c2))
            else:
                return all(self.state[COLUMNS[c2 - i] + str(r2 + i)] == '' for i in range(1, c2 - c1))

        return False

    def _update_state(self, src, dest, pt):
        self.state[src] = ''
        self.state[dest] = pt

    def _find_non_pawn(self, move, to, piece):
        if len(move) == 5:
            return move[1:3]

        p = piece[1]
        key = '' if len(move) == 3 else move[1]

        if p == 'r':
            return next(s for s, pt in self.state.items() if pt == piece and key in s and self._check_line(s, to))
        elif p == 'b':
            return next(s for s, pt in self.state.items() if pt == piece and key in s and self._check_diagonal(s, to))
        elif p == 'n':
            return next(s for s, pt in self.state.items() if pt == piece and key in s and self._check_knight_move(s, to))
        else:
            return next(s for s, pt in self.state.items() if pt == piece and key in s and (self._check_line(s, to) or self._check_diagonal(s, to)))

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

    def push(self, move):
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
