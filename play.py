#!/usr/bin/env python3
import sys
import asyncio
import time
import chess
import chess.engine
import requests
import traceback
from datetime import datetime
from collections import defaultdict

import logging
logging.basicConfig(level=logging.ERROR)

async def open_engine(engine_path):
  try:
    transport, engine = await chess.engine.popen_uci(engine_path, stderr=open('/dev/null'))
    return engine
  except Exception:
    return None

async def play_handler(engine, board):
  try:
    # 100ms max
    result = await asyncio.wait_for(engine.play(board, chess.engine.Limit(time=0.01)), 0.1)
    return result
  except asyncio.TimeoutError:
    print("engine took longer than 100ms")
  except chess.engine.EngineTerminatedError:
    print("engine process died unexpectedly")
  except Exception:
    traceback.print_exc()
  return None

# battle two github users
async def battle(user1, user2):
  print("battle %s %s" % (user1, user2))
  engine1_path = ["./launch.sh", user1]
  engine2_path = ["./launch.sh", user2]

  engine1 = await open_engine(engine1_path)
  engine2 = await open_engine(engine2_path)

  # check if engines didn't boot
  outcome = None
  if engine1 is None and engine2 is None:
    outcome = "1/2-1/2"
  elif engine1 is None:
    outcome = "0-1"
  elif engine2 is None:
    outcome = "1-0"

  if outcome is None:
    board = chess.Board()
    while not board.is_game_over():
      #print("***** move %d turn %d *****" % (board.fullmove_number, board.turn))
      #print(board)
      if board.turn:
        # white
        result = await play_handler(engine1, board)
        if result is None:
          print("%s(white) forfeits" % user1)
          outcome = "0-1"
          break
      else:
        # black
        result = await play_handler(engine2, board)
        if result is None:
          print("%s(black) forfeits" % user2)
          outcome = "1-0"
          break
      board.push(result.move)

  await engine1.quit()
  await engine2.quit()
  result = outcome if outcome is not None else board.result()

  # print outcome of match
  print(board)
  print("result of %s vs %s is %s" % (user1, user2, result))

  return result

async def main():
  forks = ["geohot"]
  for i in range(1, 51):
    r = requests.get("https://api.github.com/repos/geohot/battlechess/forks")
    print("fetch forks: %d" % r.status_code)
    if r.status_code != 200:
      print(r.text)
    else:
      break
    time.sleep(i)
  else:
    raise Exception("fetch forks failed")
  dat = r.json()
  # filter stupid forks that didn't change anything
  def format_time(x):
    return datetime.strptime(x, "%Y-%m-%dT%H:%M:%SZ")
  earliest_time = format_time("2019-04-26T00:00:00Z")
  forks += [arr['full_name'].replace("/battlechess", "") for arr in dat \
    if format_time(arr['pushed_at']) > earliest_time]
  print("battling", forks)

  score = defaultdict(int)
  # TODO: not n^2 tournament, double elimination?
  for u1 in forks:
    for u2 in forks:
      if u1 != u2:
        result = await battle(u1, u2)
        if result == '1-0':
          score[u1] += 2
          score[u2] += 0
        elif result == '0-1':
          score[u1] += 0
          score[u2] += 2
        elif result == '1/2-1/2':
          score[u1] += 1
          score[u2] += 1
  print("final scores:")
  for k,v in sorted(score.items(), key=lambda x: -x[1]):
    print("%30s : %d" % (k,v))

if __name__ == "__main__":
  asyncio.set_event_loop_policy(chess.engine.EventLoopPolicy())
  loop = asyncio.get_event_loop()

  if len(sys.argv) == 3:
    loop.run_until_complete(battle(sys.argv[1], sys.argv[2]))
  else:
    loop.run_until_complete(main())

