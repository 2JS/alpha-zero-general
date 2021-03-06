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
parser.add_argument('-p', '--player', default='human', metavar='P', help='AI vs PLAYER. Default P is human', choices=['human', 'random', 'greedy', 'ai'])
parser.add_argument('-g', '--model-file-p2', default='./temp/best.pth.tar', metavar='PATH', help='Path to model file of second ai player.')
# parser.add_argument('')
a = parser.parse_args()

path = a.model_file.split('/')
model_dir = '/'.join(path[:-1])
model_file = path[-1]

path2 = a.model_file_p2.split('/')
model_dir2 = '/'.join(path2[:-1])
model_file2 = path2[-1]

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


if a.player == 'human':
    player2 = hp
elif a.player == 'random':
    player2 = rp
elif a.player == 'greedy':
    player2 = gp
else:
    n2 = NNet(g)
    n2.load_checkpoint(model_dir2, model_file2)
    args2 = dotdict({'numMCTSSims': a.mcts, 'cpuct': 1.0})
    mcts2 = MCTS(g, n2, args2)
    n2p = lambda x: np.argmax(mcts2.getActionProb(x, temp=0))

    player2 = n2p  # Player 2 is neural network if it's cpu vs cpu.

arena = Arena.Arena(n1p, player2, g, display=AtaxxGame.display)

print(arena.playGames(2, verbose=True))
