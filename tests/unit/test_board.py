# -*- coding: utf-8 -*-

import pytest

from PIL import ImageFont

from chess.board import _get_text_loc, coordinates_of_square, BOARD_MARGIN, SQUARE_EDGE


@pytest.fixture()
def font():
    font_path = '/Library/Fonts/Arial.ttf'
    font_size = 20

    return ImageFont.truetype(font_path, font_size)


@pytest.mark.parametrize(
    "text,box,expected",
    [
        ('text', (200, 200), (83, 90)),
    ]
)
def test_get_text_loc(text, font, box, expected):
    assert _get_text_loc(text, font, box) == expected


@pytest.mark.parametrize(
    "crd,expected",
    [
        ('a1', (BOARD_MARGIN, 7 * SQUARE_EDGE + BOARD_MARGIN)),
    ]
)
def test_coordinates_of_square(crd, expected):
    assert coordinates_of_square(crd) == expected
