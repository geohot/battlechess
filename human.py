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
    while 1:
      try:
        human_move = chess.Move.from_uci(input("move:"))
        if human_move in board.legal_moves:
          break
        else:
          print("illegal move")
      except Exception:
        print("invalid move")
        pass
    board.push(human_move)

