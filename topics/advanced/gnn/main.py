import logging

from src.setup import setup_logger

setup_logger("INFO")
logger = logging.getLogger(__name__)
logger.info("Starting GNN experiment ...")


if __name__ == "__main__":
    # from src.data import visualize_graph
    from src.model import GCN
    from src.setup import download_data
    # from src.util import graph_info
    dataset = download_data()
    # graph_info(dataset[0])
    # visualize_graph(dataset[0])
    model = GCN(dataset)
    model.train_model(dataset[0])
    model.evaluate_model(dataset[0])
