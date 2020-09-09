import Arena
from MCTS import MCTS
from ataxx.AtaxxGame import AtaxxGame
from ataxx.AtaxxPlayers import *
from ataxx.pytorch.NNet import NNetWrapper as NNet


import numpy as np
from utils import *
import argparse

"""
use this script to play any two agents against each other, or play manually with
any agent.
"""

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--model-file', default='./temp/best.pth.tar', metavar='PATH', help='Path to model file. Default is ./temp/best.pth.tar')
parser.add_argument('-m', '--mcts', default=300, type=int, metavar='N', help='Number of MCTS simulation per turn')
# parser.add_argument('')
a = parser.parse_args()

path = a.model_file.split('/')
model_dir = '/'.join(path[:-1])
model_file = path[-1]

human_vs_cpu = True

g = AtaxxGame(7)

# all players
rp = RandomPlayer(g).play
gp = GreedyAtaxxPlayer(g).play
hp = HumanAtaxxPlayer(g).play



# nnet players
n1 = NNet(g)
n1.load_checkpoint(model_dir, model_file)
args1 = dotdict({'numMCTSSims': a.mcts, 'cpuct':1.0})
mcts1 = MCTS(g, n1, args1)
n1p = lambda x: np.argmax(mcts1.getActionProb(x, temp=0))

if human_vs_cpu:
    player2 = hp
else:
    n2 = NNet(g)
    n2.load_checkpoint(model_dir, model_file)
    args2 = dotdict({'numMCTSSims': a.mcts, 'cpuct': 1.0})
    mcts2 = MCTS(g, n2, args2)
    n2p = lambda x: np.argmax(mcts2.getActionProb(x, temp=0))

    player2 = n2p  # Player 2 is neural network if it's cpu vs cpu.

arena = Arena.Arena(n1p, player2, g, display=AtaxxGame.display)

print(arena.playGames(2, verbose=True))
