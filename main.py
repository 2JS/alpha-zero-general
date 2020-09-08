import argparse
import logging
import coloredlogs
from Coach import Coach
from othello.OthelloGame import OthelloGame as Game
from othello.pytorch.NNet import NNetWrapper as nn
from utils import *
import sys


parser = argparse.ArgumentParser()
parser.add_argument("-i", "--iters", type=int, default=5, metavar='N', help="Number of iteration")
parser.add_argument("-e", "--eps", type=int, default=100, metavar='N', help="Number of complete self-play games")
parser.add_argument("-t", "--updateThreshold", type=float, default=0.6, metavar='N', help="During arena playoff, new neural net will be accepted if threshold or more of games are won.")
parser.add_argument("-m", "--mcts", type=int, default=25, metavar='N', help="Number of games moves for MCTS to simulate.")
parser.add_argument("-a", "--arena", type=int, default=40, metavar='N', help="Number of games to play during arena play to determine if new net will be accepted.")
parser.add_argument("-c", "--checkpoint", default='./temp/', metavar='PATH', help="Path to dir where checkpoints will be saved.")
parser.add_argument("-f", "--model-file", default=None, metavar='PATH', help="")
parser.add_argument("-y", "--history", type=int, default=20, metavar='N', help="Number of iterations for train examples history.")
a = parser.parse_args()

if a.model_file != None:
    path = a.model_file.split('/')
    model_dir = '/'.join(path[:-1])
    model_file = path[-1]
else:
    model_dir = '/dev/models/8x100x50'
    model_file = 'best.pth.tar'

log = logging.getLogger(__name__)

coloredlogs.install(level='INFO')  # Change this to DEBUG to see more info.

args = dotdict({
    'numIters': a.iters,
    'numEps': a.eps,              # Number of complete self-play games to simulate during a new iteration.
    'tempThreshold': 15,        #
    'updateThreshold': a.updateThreshold,     # During arena playoff, new neural net will be accepted if threshold or more of games are won.
    'maxlenOfQueue': 200000,    # Number of game examples to train the neural networks.
    'numMCTSSims': a.mcts,          # Number of games moves for MCTS to simulate.
    'arenaCompare': a.arena,         # Number of games to play during arena play to determine if new net will be accepted.
    'cpuct': 1,

    'checkpoint': a.checkpoint,
    'load_model': True if a.model_file != None else False,
    'load_folder_file': (model_dir, model_file),
    'numItersForTrainExamplesHistory': a.history,
    'task': 'germ',
    'board_size': 7
})

assert args.task in ['othello', 'germ']
assert args.board_size > 0

if args.task == 'othello':
    from othello.OthelloGame import OthelloGame as Game
    from othello.pytorch.NNet import NNetWrapper as nn

elif args.task == 'germ':
    from ataxx.AtaxxGame import AtaxxGame as Game
    from ataxx.pytorch.NNet import NNetWrapper as nn

def main():

    log.info('Loading %s...', Game.__name__)

    g = Game(args.board_size)

    log.info('Loading %s...', nn.__name__)
    nnet = nn(g)

    if args.load_model:
        log.info('Loading checkpoint "%s/%s"...', args.load_folder_file[0], args.load_folder_file[1])
        nnet.load_checkpoint(args.load_folder_file[0], args.load_folder_file[1])
    else:
        log.warning('Not loading a checkpoint!')

    log.info('Loading the Coach...')
    c = Coach(g, nnet, args)

    if args.load_model:
        log.info("Loading 'trainExamples' from file...")
        c.loadTrainExamples()

    log.info('Starting the learning process 🎉')
    c.learn()


if __name__ == "__main__":
    main()
