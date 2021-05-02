import torch
import torch.nn

torch.manual_seed(1)


class MLP(nn.Module):
    def __init__(self, sizes, device):
        super().__init__()
        layers = []
        for i in range(1, len(sizes)):
            layers.append(('fc{}'.format(i), nn.Linear(sizes[i - 1], sizes[i])))
            if i + 1 != len(sizes):
                layers.append(('relu{}'.format(i), nn.ReLU()))
        self.layers = nn.Sequential(OrderedDict(layers))

    def forward(self, x):
        return self.layers(x)

