import sys
sys.path.append('..')
from utils import *

import argparse
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision import datasets, transforms
from torch.autograd import Variable


class ResidualBlock(nn.Module):
    def __init__(self, size=7, channel=64):
        super(ResidualBlock, self).__init__()
        self.size = size
        self.channel = channel
        self.conv1 = nn.Conv2d(channel, channel, kernel_size=3, padding=1, bias=False)
        self.bn1 = nn.BatchNorm2d(channel)
        self.relu = nn.LeakyReLU(inplace=True)
        self.conv2 = nn.Conv2d(channel, channel, kernel_size=3, padding=1, bias=False)
        self.bn2 = nn.BatchNorm2d(channel)

    def forward(self, input):
        x = self.conv1(input)
        x = self.bn1(x)
        x = self.relu(x)
        x = self.conv2(x)
        x = self.bn2(x)
        x += input
        x = self.relu(x)
        return x

class AtaxxNNet(nn.Module):
    def __init__(self, size=7):
        self.size = size
        
        super(AtaxxNNet, self).__init__()
        self.conv1a = nn.Conv2d(2, 32, kernel_size=3, padding=1, bias=False)
        self.conv1b = nn.Conv2d(2, 16, kernel_size=5, padding=2, bias=False)
        self.conv1c = nn.Conv2d(2, 16, kernel_size=7, padding=3, bias=False)
        self.relu = nn.LeakyReLU(inplace=True)
        self.bn1 = nn.BatchNorm2d(64)

        self.res_layers = nn.Sequential(*[ResidualBlock() for i in range(19)])

        self.conv_val = nn.Conv2d(64, 1, kernel_size=1, bias=False)
        self.bn_val = nn.BatchNorm2d(1)
        self.fc_val1 = nn.Linear(size*size, size*size)
        self.fc_val2 = nn.Linear(size*size, 1)

        self.conv_pol = nn.Conv2d(64, 24, kernel_size=1, bias=False)
        self.bn_pol = nn.BatchNorm2d(24)
        self.fc_pol = nn.Linear(24*size*size, 530)
        
    def forward(self, batch):
        x = batch.view(-1, 2, self.size, self.size)

        xa = self.relu(self.conv1a(x))
        xb = self.relu(self.conv1b(x))
        xc = self.relu(self.conv1c(x))
        x = torch.cat((xa, xb, xc), dim=1)
        x = self.bn1(x)
        x = self.relu(x)

        x = self.res_layers(x)

        x_val = self.conv_val(x)
        x_val = self.bn_val(x_val)
        x_val = self.relu(x_val)
        x_val = x_val.view(-1, 1*self.size*self.size)
        x_val = self.fc_val1(x_val)
        x_val = self.relu(x_val)
        x_val = self.fc_val2(x_val)

        x_pol = self.conv_pol(x)
        x_pol = self.bn_pol(x_pol)
        x_pol = self.relu(x_pol)
        x_pol = x_pol.view(-1, 24*self.size*self.size)
        x_pol = self.fc_pol(x_pol)
        
        return F.log_softmax(x_pol, dim=1), torch.tanh(x_val)
