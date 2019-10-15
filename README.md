# chess-game

A tool that generate GIFs from pgn files of a chess game.

### Usage

The tool can be called using the following options:

```
usage: main.py [-h] [-i INIT_STATE] [-d DELAY] [-o OUT] [--black BLACK]
               [--white WHITE] [--font_path FONT_PATH] [-v]
               [-L {debug,info,warn}] [-V]
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
  --black BLACK         color of the black in hex
  --white WHITE         color of the white in hex
  --font_path FONT_PATH
                        path of the display font used in board
  -v, --verbose         print final board state
  -L {debug,info,warn}, --level {debug,info,warn}
                        log level: debug, info
  -V, --version         print version information
```

### How To

#### Convert GIF to PNG

Here is a example that convert `file.gif` to `file.png`.

    sips -s format png ./file.gif --out file.png
