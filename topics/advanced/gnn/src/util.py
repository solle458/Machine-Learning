from logging import getLogger

import torch
from torch_geometric.data import Data

logger = getLogger(__name__)


def graph_info(data: Data) -> None:
    """Log a summary of graph structure and masks."""
    logger.info("Number of nodes: %d", data.num_nodes)
    logger.info("Number of edges: %d", data.num_edges)
    logger.info("Number of features: %d", data.num_features)
    logger.info("Is undirected: %s", data.is_undirected())
    logger.info("Has isolated nodes: %s", data.has_isolated_nodes())
    logger.info("Has self-loops: %s", data.has_self_loops())
    if hasattr(data, "num_classes"):
        logger.info("Number of classes: %d", data.num_classes)
    logger.info("x shape: %s", tuple(data.x.shape))
    logger.info("y shape: %s", tuple(data.y.shape))
    logger.info("edge_index shape: %s", tuple(data.edge_index.shape))
    logger.info("train nodes: %d", int(data.train_mask.sum()))
    logger.info("val nodes: %d", int(data.val_mask.sum()))
    logger.info("test nodes: %d", int(data.test_mask.sum()))
    class_counts = torch.bincount(data.y).tolist()
    logger.info("class distribution: %s", class_counts)
