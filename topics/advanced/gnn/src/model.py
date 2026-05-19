from logging import getLogger

import torch.nn as nn
from torch import Tensor
from torch_geometric.data import Data
from torch_geometric.nn import GCNConv

logger = getLogger(__name__)


class GCN(nn.Module):
    """Two-layer Graph Convolutional Network."""

    def __init__(
        self,
        num_features: int,
        num_classes: int,
        hidden_dim: int = 32,
    ) -> None:
        logger.info("Initializing GCN model ...")
        super().__init__()
        self.conv1 = GCNConv(num_features, hidden_dim)
        self.relu = nn.ReLU()
        self.conv2 = GCNConv(hidden_dim, num_classes)
        logger.info("GCN model initialized.")

    def forward(self, data: Data) -> Tensor:
        x = self.conv1(data.x, data.edge_index)
        x = self.relu(x)
        return self.conv2(x, data.edge_index)
