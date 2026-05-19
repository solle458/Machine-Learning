from logging import getLogger

import matplotlib.pyplot as plt
import networkx as nx
from torch_geometric.utils import to_networkx

logger = getLogger(__name__)

def visualize_graph(data):
    """
    Visualize a graph.
    Args:
        data: A PyTorch Geometric Data object.
    Returns:
        None
    Raises:
        None
    Example:
        >>> visualize_graph(data)
    """
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
