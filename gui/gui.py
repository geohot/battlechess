#!/usr/bin/env python3
import os
os.chdir(os.path.dirname(__file__))

import sys
import chess
import traceback
sys.path.append("../")
from engine import get_move
from flask import Flask, Response, request
board = chess.Board()

def computer_move(board):
  if not board.is_game_over():
    board.push(get_move(board))

app = Flask(__name__)
@app.route("/")
def hello():
  ret = open("index.html").read()
  return ret.replace('start', board.fen())

# moves given as coordinates of piece moved
@app.route("/move_coordinates", methods=['POST'])
def move_coordinates():
  if not board.is_game_over():
    source = int(request.form.get('from', default=''))
    target = int(request.form.get('to', default=''))
    promotion = True if request.form.get('promotion', default='') == 'true' else False

    move = board.san(chess.Move(source, target, promotion=chess.QUEEN if promotion else None))
    if move is not None and move != "":
      try:
        board.push_san(move)
        computer_move(board)
      except Exception:
        traceback.print_exc()
  return board.fen()

@app.route("/newgame", methods=['POST'])
def newgame():
  board.reset()
  return board.fen()

@app.route("/computermove", methods=['POST'])
def computermove():
  computer_move(board)
  return board.fen()

if __name__ == "__main__":
  app.run()

