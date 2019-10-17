# -*- coding: utf-8 -*-

from chess import list_supported_state_files
from chess.codec import load_state_from_file


def test_list_supported_state_files():
    supported_states = list_supported_state_files()

    assert len(supported_states) == 2
    assert len(load_state_from_file(supported_states['empty'])) == 0
    assert len(load_state_from_file(supported_states['default'])) == 32
