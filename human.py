#!/usr/bin/env python3
import chess
from engine import get_move

if __name__ == "__main__":
  board = chess.Board()

  while not board.is_game_over():
    # computer plays white
    computer_move = get_move(board)
    board.push(computer_move)

    # display the board
    print(board)

    # human plays black
    human_move = chess.Move.from_uci(input("move:"))
    board.push(human_move)

