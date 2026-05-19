from logging import getLogger

import torch
import torch.nn as nn
from rich.progress import track
from torch import optim
from torch_geometric.data import Data

from src.config import TrainConfig
from src.model import GCN

logger = getLogger(__name__)


def train(model: GCN, data: Data, config: TrainConfig) -> None:
    """Train the model on the training mask."""
    loss_fnc = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters())
    model.train()
    for _ in track(range(config.epochs), description="Training model ..."):
        optimizer.zero_grad()
        out = model(data)
        loss = loss_fnc(out[data.train_mask], data.y[data.train_mask])
        loss.backward()
        optimizer.step()
    logger.info("Model trained.")


def evaluate(model: GCN, data: Data) -> float:
    """Return test-set accuracy."""
    model.eval()
    with torch.no_grad():
        pred = model(data).argmax(dim=1)
        correct = (pred[data.test_mask] == data.y[data.test_mask]).sum()
        return int(correct) / int(data.test_mask.sum())
