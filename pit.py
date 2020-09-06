import Arena
from MCTS import MCTS
from main import args
import numpy as np
from utils import *

if args.task == 'othello':
    from othello.OthelloGame import OthelloGame
    from othello.OthelloPlayers import *
    from othello.pytorch.NNet import NNetWrapper as NNet

elif args.task == 'germ':
    from germ.GermGame import GermGame as OthelloGame
    from germ.GermPlayers import *
    from germ.pytorch.NNet import NNetWrapper as NNet


"""
use this script to play any two agents against each other, or play manually with
any agent.
"""

mini_othello = False  # Play in 6x6 instead of the normal 8x8.
human_vs_cpu = True


g = OthelloGame(args.board_size)

# all players
rp = RandomPlayer(g).play
gp = GreedyOthelloPlayer(g).play
hp = HumanOthelloPlayer(g).play


# nnet players
n1 = NNet(g)

# # board_size = 6
# if mini_othello:
#     n1.load_checkpoint('./pretrained_models/othello/pytorch/', '6x100x25_best.pth.tar')
# # board_size = 8
# else:
#     n1.load_checkpoint('./pretrained_models/othello/pytorch/', '8x8_100checkpoints_best.pth.tar')

n1.load_checkpoint('./pretrained_models/germ/', 'temp.pth.tar')


args1 = dotdict({'numMCTSSims': 50, 'cpuct': 1.0})
mcts1 = MCTS(g, n1, args1)
n1p = lambda x: np.argmax(mcts1.getActionProb(x, temp=0))

if human_vs_cpu:
    player2 = hp
else:
    n2 = NNet(g)
    n2.load_checkpoint('./pretrained_models/othello/pytorch/', '8x8_100checkpoints_best.pth.tar')
    args2 = dotdict({'numMCTSSims': 50, 'cpuct': 1.0})
    mcts2 = MCTS(g, n2, args2)
    n2p = lambda x: np.argmax(mcts2.getActionProb(x, temp=0))

    player2 = n2p  # Player 2 is neural network if it's cpu vs cpu.

arena = Arena.Arena(n1p, player2, g, display=OthelloGame.display)

print(arena.playGames(2, verbose=True))
