# chess-game

A tool-set for chess game.

### Usage

The tool-set contains two sub-command: 

```
usage: main.py [-h] [-V] {image,manual} ...

positional arguments:
  {image,manual}  sub-command help
    image         tool that generates GIF picture
    manual        tool that loads chess manual text

optional arguments:
  -h, --help      show this help message and exit
  -V, --version   print version information
```

The `image` sub-command can be called using the following options:

```
usage: main.py image [-h] [-i INIT_STATE] [-d DELAY] [-o OUT] [-b]
                  [--black BLACK] [--white WHITE] [--font_path FONT_PATH] [-v]
                  [-L {debug,info,warn}]
                  [path [path ...]]

positional arguments:
  path                  path to the pgn file/folder

optional arguments:
  -h, --help            show this help message and exit
  -i INIT_STATE, --init_state INIT_STATE
                        initialize board state: empty, default, or target
                        state file path
  -d DELAY, --delay DELAY
                        delay between moves in seconds
  -o OUT, --out OUT     name of the output folder
  -b, --black_first     run black first
  --black BLACK         color of the black in hex
  --white WHITE         color of the white in hex
  --font_path FONT_PATH
                        path of the display font used in board
  -v, --verbose         print final board state
  -L {debug,info,warn}, --level {debug,info,warn}
                        log level: debug, info
```

The `manual` sub-command can be called using the following options:

```
usage: main.py manual [-h] [-n NUM] [-b] [-L {debug,info,warn}] [path [path ...]]

positional arguments:
  path                  path to the pgn file/folder

optional arguments:
  -h, --help            show this help message and exit
  -n NUM, --num NUM     start number
  -b, --black_first     run black first
  -L {debug,info,warn}, --level {debug,info,warn}
                        log level: debug, info
```

### How To

#### Convert GIF to PNG

Here is a example that convert `file.gif` to `file.png`.

    sips -s format png ./file.gif --out file.png
