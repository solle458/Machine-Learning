from logging import getLogger

import torch.nn as nn
from rich.progress import track
from torch import optim
from torch_geometric.datasets import Planetoid
from torch_geometric.nn import GCNConv

logger = getLogger(__name__)

class GCN(nn.Module):
    """
    Graph Convolutional Network.
    Args:
        dataset: A PyTorch Geometric Planetoid object.
    Returns:
        None
    Raises:
        None
    Example:
        >>> model = GCN(dataset)
    """
    def __init__(self, dataset: Planetoid):
        logger.info("Initializing GCN model ...")
        super().__init__()
        self.conv1 = GCNConv(dataset.num_features, 32)
        self.relu = nn.ReLU()
        self.conv2 = GCNConv(32, dataset.num_classes)
        logger.info("GCN model initialized.")

    def forward(self, data):
        """
        Forward pass.
        Args:
            data: A PyTorch Geometric Data object.
        Returns:
            None
        Raises:
            None
        Example:
            >>> model = GCN(dataset)
            >>> model(data)
        """
        x = data.x
        edge_index = data.edge_index

        x = self.conv1(x, edge_index)
        x = self.relu(x)
        x = self.conv2(x, edge_index)
        return x

    def train_model(self, data: Planetoid):
        """
        Train the model.
        Args:
            data: A PyTorch Geometric Data object.
        Returns:
            None
        Raises:
            None
        Example:
            >>> model = GCN(dataset)
            >>> model.train_model(data)
        """
        loss_fnc = nn.CrossEntropyLoss()
        optimizer = optim.Adam(self.parameters())
        self.train()
        for _ in track(range(200), description="Training model ..."):
            optimizer.zero_grad()
            out = self(data)
            loss = loss_fnc(out[data.train_mask], data.y[data.train_mask])
            loss.backward()
            optimizer.step()
        logger.info("Model trained.")

    def evaluate_model(self, data: Planetoid):
        """
        Evaluate the model.
        Args:
            data: A PyTorch Geometric Data object.
        Returns:
            None
        Raises:
            None
        Example:
            >>> model = GCN(dataset)
            >>> model.evaluate_model(data)
        """
        self.eval()
        pred = self(data).argmax(dim=1)
        correct = (pred[data.test_mask] == data.y[data.test_mask]).sum()
        acc = int(correct) / int(data.test_mask.sum())
        logger.info("Accuracy: %f", acc)
