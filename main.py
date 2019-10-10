# -*- coding: utf-8 -*-

import argparse
import glob
import os

import imageio

from PIL import Image, ImageDraw, ImageFont
from numpy import array


# board
BOARD_EDGE = 480
SQUARE_EDGE = BOARD_EDGE // 8
# text font
FONT_SIZE = 15
BOARD_MARGIN = 20


def create_gif(pgn, output_dir, out_name, duration):
    board_image = initial_board.copy()
    images = [array(board_image)]
    imageio.mimsave(os.path.join(output_dir, out_name), images, duration=duration)


def process_file(pgn, duration, output_dir):
    filename, extension = os.path.splitext(os.path.basename(pgn))
    name = filename + '.gif'
    if name in os.listdir(output_dir):
        print('gif with name %s already exists.' % name)
    else:
        print('creating', name, end='...\n')
        create_gif(pgn, output_dir, name, duration)
        print('done')


def clear(image, crd):
    global white_square, black_square

    if (crd[0] < BOARD_EDGE + BOARD_MARGIN) and (crd[1] < BOARD_EDGE + BOARD_MARGIN):
        if (crd[0] + crd[1] - 2 * BOARD_MARGIN) % (SQUARE_EDGE * 2) == 0:
            image.paste(white_square, crd, white_square)
        else:
            image.paste(black_square, crd, black_square)


def generate_board():
    global initial_board, ttfont
    global bk, bq, bb, bn, br, bp, wk, wq, wb, wn, wr, wp

    for i in range(0 + BOARD_MARGIN, BOARD_EDGE + 2 * BOARD_MARGIN, SQUARE_EDGE):
        for j in range(0 + BOARD_MARGIN, BOARD_EDGE + 2 * BOARD_MARGIN, SQUARE_EDGE):
            clear(initial_board, (i, j))

    row = ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r']
    order = ('b', 'w')

    # show chess.
    for i in range(8):
        col = SQUARE_EDGE * i
        # draw rock, knight, bishop, queen and king.
        exec('initial_board.paste({0}, (col + BOARD_MARGIN, 0 + BOARD_MARGIN), {0})'.format(order[0] + row[i]))
        exec('initial_board.paste({0}, (col + BOARD_MARGIN, BOARD_MARGIN + BOARD_EDGE - SQUARE_EDGE), {0})'.format(order[1] + row[i]))
        # draw pawn.
        exec('initial_board.paste({0}p, (col + BOARD_MARGIN, BOARD_MARGIN + SQUARE_EDGE), {0}p)'.format(order[0]))
        exec('initial_board.paste({0}p, (col + BOARD_MARGIN, BOARD_MARGIN + BOARD_EDGE - (SQUARE_EDGE * 2)), {0}p)'.format(order[1]))

    draw = ImageDraw.Draw(initial_board)
    # write text.
    for i in range(8):
        col = SQUARE_EDGE * i
        text = chr(ord('a') + i)
        width, height = ttfont.getsize(text)
        padding_vert = (BOARD_MARGIN - height) // 2
        padding_hor = (SQUARE_EDGE - width) // 2
        # draw top 'a' to 'h'
        draw.text((col + BOARD_MARGIN + padding_hor, padding_vert), text, fill=(255, 255, 255), font=ttfont)
        # draw bottom 'a' to 'h'
        draw.text((col + BOARD_MARGIN + padding_hor, BOARD_EDGE + BOARD_MARGIN), text, fill=(255, 255, 255), font=ttfont)

        text = chr(ord('8') - i)
        width, height = ttfont.getsize(text)
        padding_vert = (BOARD_MARGIN - height) // 2
        padding_hor = (SQUARE_EDGE - width) // 2
        # draw left '1' to '8'
        draw.text((BOARD_MARGIN - padding_vert - width, BOARD_MARGIN + col + padding_hor), text, fill=(255, 255, 255), font=ttfont)
        draw.text((BOARD_EDGE + BOARD_MARGIN + padding_vert, BOARD_MARGIN + col + padding_hor), text, fill=(255, 255, 255), font=ttfont)


def init(args):
    # initialize board and font.
    global initial_board, ttfont
    initial_board = Image.new('RGB', (BOARD_EDGE + 2 * BOARD_MARGIN, BOARD_EDGE + 2 * BOARD_MARGIN))
    ttfont = ImageFont.truetype('/Library/Fonts/Arial.ttf', FONT_SIZE)
    # initialize black and white squares.
    global white_square, black_square
    white_square = Image.new('RGBA', (SQUARE_EDGE, SQUARE_EDGE), args.white)
    black_square = Image.new('RGBA', (SQUARE_EDGE, SQUARE_EDGE), args.black)

    # load chess images
    global bk, bq, bb, bn, br, bp, wk, wq, wb, wn, wr, wp
    bk = Image.open(os.path.join(args.asset, 'bk.png'))
    bq = Image.open(os.path.join(args.asset, 'bq.png'))
    bb = Image.open(os.path.join(args.asset, 'bb.png'))
    bn = Image.open(os.path.join(args.asset, 'bn.png'))
    br = Image.open(os.path.join(args.asset, 'br.png'))
    bp = Image.open(os.path.join(args.asset, 'bp.png'))

    wk = Image.open(os.path.join(args.asset, 'wk.png'))
    wq = Image.open(os.path.join(args.asset, 'wq.png'))
    wb = Image.open(os.path.join(args.asset, 'wb.png'))
    wn = Image.open(os.path.join(args.asset, 'wn.png'))
    wr = Image.open(os.path.join(args.asset, 'wr.png'))
    wp = Image.open(os.path.join(args.asset, 'wp.png'))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('path', nargs='*', help='path to the pgn file/folder')
    parser.add_argument('-a', '--asset', help='path to the asset folder', default=os.path.join(os.getcwd(), 'asset'))
    parser.add_argument('-d', '--delay', help='delay between moves in seconds', default=1.0)
    parser.add_argument('-o', '--out', help='name of the output folder', default=os.getcwd())
    parser.add_argument('--black', help='color of the black in hex', default='#4B7399')
    parser.add_argument('--white', help='color of the white in hex', default='#EAE9D2')
    args = parser.parse_args()

    init(args)

    if not args.path:
        print('Please specify path or directory of png files')

    generate_board()

    for path in args.path:
        if os.path.isfile(path):
            process_file(path, args.delay, args.out)
        elif os.path.isdir(path):
            for pgn in glob.glob(path + '/*.pgn'):
                process_file(pgn, args.delay, args.out)


if __name__ == '__main__':
    main()
