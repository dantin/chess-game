# -*- coding: utf-8 -*-

import os

from chess.codec import load_moves_from_file, load_state_from_file


def test_load_moves_from_file(input_path):
    moves = load_moves_from_file(os.path.join(input_path, 'sample.pgn'))

    assert isinstance(moves, list)
    assert len(moves) == 11
    assert moves[0] == 'e4'


def test_load_state_from_file(input_path):
    state = load_state_from_file(os.path.join(input_path, 'state.bd'))

    assert isinstance(state, dict)
    assert len(state) == 2
    assert state['a1'] == 'bk'
