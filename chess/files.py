# -*- coding: utf-8 -*-

import logging
import re


logger = logging.getLogger('ROOT')


def load_moves_from_file(pgn):
    logger.debug('load moves from png file "%s"', pgn)
    with open(pgn) as p:
        data = p.read()
        data = re.sub(r'\{.*?\}', '', data)  # remove png comments
        moves = re.findall(
            r'[a-h]x?[a-h]?[1-8]?=?[BKNRQ]?|O-O-?O?|[BKNRQ][a-h1-8]?[a-h1-8]?x?[a-h][1-8]',
            data)
        return [move.replace('x', '') for move in moves]


def load_state_from_file(file_path):
    logger.debug('load state from file "%s"', file_path)
    with open(file_path) as f:
        data = f.read()
        pairs = re.findall(
            r'[a-h][1-8]=[wb][bknrqp]',
            data)
        return {k: v for k, v in (p.split('=') for p in pairs)}
