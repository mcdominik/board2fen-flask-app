# board2fen-flask-app

## What it is
Simple Flask application, enables web usage of package board_to_fen package [https://github.com/mcdominik/board_to_fen]
Forsyth–Edwards Notation explained: https://en.wikipedia.org/wiki/Forsyth%E2%80%93Edwards_Notation

#Available at

# https://board2fen.bieda.it

<img width="1512" alt="Screenshot 2023-01-05 at 16 46 44" src="https://user-images.githubusercontent.com/81818614/210822074-38586ea4-a1b9-4af0-864c-6fd315e1b62b.png">


# or docker image:
```
docker pull mcdominik/board2fen_cpu
```

## How to use it

Simple FEN options:

- black view: toggle if you provide image with black player perspective

Full FEN options:

- black view: toggle if you provide image with black player perspective
- next move: who make next move
- who can castle: castle availability
- "en passant" target square: en passant square -> player has to move pawn 2 squares forward in the last move
- full-move number: numbers of moves since game stared
- half-move number: numbers of moves since the last capture or pawn advance, used for the [fifty-move rule](https://en.wikipedia.org/wiki/Fifty-move_rule)

## Warnings
- Image has to be provided in neutral angle (player's perspective).
- Image has to be square.
- Image can't contain paddings, borders etc. other than 64 squares (with pieces) itself.
