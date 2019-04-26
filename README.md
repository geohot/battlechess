# battlechess

### A decentralized chess tournament using GitHub and Travis CI.

[![Build Status](https://travis-ci.org/geohot/battlechess.svg?branch=master)](https://travis-ci.org/geohot/battlechess) **Click the CI link for the latest battle results**

Currently, the engine makes random moves. Fork this, modify get_move in engine.py, and join the battle! play.py uses the GitHub API to look for forks on this repo, so once you fork it you are registered as a competitor.

The idea isn't to modify stockfish, it's to write clever short python algorithms. Will add checks for running time and code shortness soon. And if there's cheating, I'll add a sandbox. If you want to use a Python library, send a pull request to modify requirements.txt and we can discuss if it's fair.

<pre>
# Play vs your engine in a GUI
cd gui; ./gui.py

# Run a tournament
./play.py

# Run a battle (geohot vs geohot)
DEBUG=1 ./play.py geohot geohot

# Launch your engine in Docker (quit to quit)
./launch.sh geohot
</pre>

UPDATE: You have at most 500ms to make your move. Go over, and you forfeit the match.

UPDATE: seccomp sandbox will be added, do not use exec, the internet, or the filesystem.

