from logging import getLogger

logger = getLogger(__name__)

def graph_info(data):
    """
    Print information about a graph.
    Args:
        data: A PyTorch Geometric Data object.
    Returns:
        None
    Raises:
        None
    Example:
        >>> graph_info(data)
    """
    logger.info("Number of nodes: %d", data.num_nodes)
    logger.info("Number of edges: %d", data.num_edges)
    logger.info("Number of features: %d", data.num_features)
    logger.info("Is undirected: %s", data.is_undirected())
    logger.info("Has isolated nodes: %s", data.has_isolated_nodes())
    logger.info("Has self-loops: %s", data.has_self_loops())
    logger.info("key: %s", data.keys)
    logger.info("features of each node: %s", data["x"])
    logger.info("labels of each node: %s", data["y"])
    logger.info("each edge: %s", data["edge_index"])
