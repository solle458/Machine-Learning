import torch
from src.model import GCN
from src.train import evaluate
from torch_geometric.data import Data


def _synthetic_data(
    num_nodes: int = 10,
    num_features: int = 3,
    num_classes: int = 2,
) -> Data:
    x = torch.randn(num_nodes, num_features)
    edge_index = torch.tensor([[0, 1, 2], [1, 2, 0]], dtype=torch.long)
    y = torch.randint(0, num_classes, (num_nodes,))
    train_mask = torch.zeros(num_nodes, dtype=torch.bool)
    val_mask = torch.zeros(num_nodes, dtype=torch.bool)
    test_mask = torch.zeros(num_nodes, dtype=torch.bool)
    train_mask[:6] = True
    val_mask[6:8] = True
    test_mask[8:] = True
    return Data(
        x=x,
        edge_index=edge_index,
        y=y,
        train_mask=train_mask,
        val_mask=val_mask,
        test_mask=test_mask,
    )


def test_forward_shape() -> None:
    data = _synthetic_data()
    model = GCN(num_features=3, num_classes=2, hidden_dim=4)
    out = model(data)
    assert out.shape == (10, 2)


def test_evaluate_returns_valid_accuracy() -> None:
    data = _synthetic_data()
    model = GCN(num_features=3, num_classes=2, hidden_dim=4)
    acc = evaluate(model, data)
    assert 0.0 <= acc <= 1.0
