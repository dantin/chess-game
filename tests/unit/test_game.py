# -*- coding: utf-8 -*-

import pytest

from chess.game import load_empty_state, check_knight_move, check_line


@pytest.fixture(scope='function')
def empty_board():
    # print(' SETUP board')
    yield load_empty_state()
    # print(' TEARDOWN board')


def test_load_empty_state():
    empty_state = load_empty_state()

    assert isinstance(empty_state, dict)
    assert len(empty_state) == 8 * 8
    assert empty_state['a1'] == ''


@pytest.mark.parametrize(
    "lhs,rhs,expected",
    [
        ('d4', 'e6', True),
        ('d4', 'c6', True),
        ('d4', 'b5', True),
        ('d4', 'b3', True),
        ('d4', 'c2', True),
        ('d4', 'e2', True),
        ('d4', 'f5', True),
        ('d4', 'f3', True),
        ('e6', 'd4', True),
        ('c6', 'd4', True),
        ('b5', 'd4', True),
        ('b3', 'd4', True),
        ('c2', 'd4', True),
        ('e2', 'd4', True),
        ('f5', 'd4', True),
        ('f3', 'd4', True),
        ('d4', 'f7', False),
    ]
)
def test_check_knight_move(lhs, rhs, expected):
    assert check_knight_move(lhs, rhs) == expected


@pytest.mark.parametrize(
    "lhs,rhs,expected",
    [
        ('a4', 'e4', True),
        ('h4', 'e4', True),
        ('a5', 'e4', False),
    ]
)
def test_check_line(empty_board, lhs, rhs, expected):
    assert check_line(empty_board, lhs, rhs) == expected
