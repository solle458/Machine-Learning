from logging import getLogger
from typing import Literal

import networkx as nx
from torch_geometric.datasets import Planetoid
from torch_geometric.utils import to_networkx

from src.paths import DATA_DIR

logger = getLogger(__name__)

PlanetoidName = Literal["Cora", "Pubmed", "Citeseer"]

_DATASET_ALIASES: dict[str, PlanetoidName] = {
    "cora": "Cora",
    "pubmed": "Pubmed",
    "citeseer": "Citeseer",
}


def resolve_planetoid_name(name: str) -> PlanetoidName:
    """Map CLI dataset name to Planetoid dataset name."""
    key = name.lower()
    if key not in _DATASET_ALIASES:
        valid = ", ".join(sorted(_DATASET_ALIASES))
        msg = f"Unknown dataset {name!r}. Choose from: {valid}"
        raise ValueError(msg)
    return _DATASET_ALIASES[key]


def load_planetoid(name: PlanetoidName) -> Planetoid:
    """Download or load a Planetoid dataset under DATA_DIR."""
    root = DATA_DIR / name
    if root.exists():
        logger.info("Loading %s dataset from %s", name, root.resolve())
    else:
        logger.info("Downloading %s dataset to %s ...", name, root.resolve())
    dataset = Planetoid(root=str(root), name=name)
    logger.info("%s dataset ready (%d graph(s)).", name, len(dataset))
    return dataset


def visualize_graph(data) -> None:
    """Visualize a graph with matplotlib."""
    import matplotlib.pyplot as plt

    logger.info("Visualizing graph ...")
    g = to_networkx(data)
    plt.figure(figsize=(12, 10))
    nx.draw(
        g,
        node_color=data.y,
        node_size=10,
    )
    plt.show()
    logger.info("Graph visualized.")
