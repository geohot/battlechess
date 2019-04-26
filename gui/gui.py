#!/usr/bin/env python3
import sys
import chess
import traceback
sys.path.append("../")
from engine import get_move
from flask import Flask, Response, request
board = chess.Board()

app = Flask(__name__)
@app.route("/")
def hello():
  ret = open("index.html").read()
  return ret.replace('start', board.fen())

# moves given as coordinates of piece moved
@app.route("/move_coordinates")
def move_coordinates():
  if not board.is_game_over():
    source = int(request.args.get('from', default=''))
    target = int(request.args.get('to', default=''))
    promotion = True if request.args.get('promotion', default='') == 'true' else False

    move = board.san(chess.Move(source, target, promotion=chess.QUEEN if promotion else None))
    if move is not None and move != "":
      try:
        board.push_san(move)
        board.push(get_move(board))
      except Exception:
        traceback.print_exc()
    return board.fen()

  print("GAME IS OVER")
  return "game over"

@app.route("/newgame")
def newgame():
  board.reset()
  return board.fen()

@app.route("/computermove")
def computermove():
  board.push(get_move(board))
  return board.fen()

if __name__ == "__main__":
  app.run(debug=True)

