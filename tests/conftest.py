# -*- coding: utf-8 -*-
"""Shared fixture functions in multiple tests."""

import os

import pytest


@pytest.fixture
def base_path():
    """Base path."""
    return os.path.join(os.curdir, 'misc')


@pytest.fixture
def input_path(base_path):
    """Input path."""
    return os.path.join(base_path, 'input')
