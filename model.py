import torch
import torch.nn
from collections import (
    OrderedDict,
)

torch.manual_seed(1)


class MLP(torch.nn.Module):
    def __init__(self, sizes, device):
        super().__init__()
        layers = []
        for i in range(1, len(sizes)):
            layers.append(('fc{}'.format(i), torch.nn.Linear(sizes[i - 1], sizes[i])))
            if i + 1 != len(sizes):
                layers.append(('relu{}'.format(i), torch.nn.ReLU()))
        self.layers = torch.nn.Sequential(OrderedDict(layers)).to(device)

    def forward(self, x):
        return self.layers(x)

