import argparse
import logging

from src.config import TrainConfig
from src.data import load_planetoid, resolve_planetoid_name, visualize_graph
from src.model import GCN
from src.setup import setup_logger
from src.train import evaluate, train
from src.util import graph_info

logger = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train a GCN on a Planetoid dataset.")
    parser.add_argument(
        "--dataset",
        default="pubmed",
        help="Planetoid dataset name (cora, pubmed, citeseer). Default: pubmed",
    )
    parser.add_argument(
        "--epochs",
        type=int,
        default=200,
        help="Number of training epochs. Default: 200",
    )
    parser.add_argument(
        "--log-level",
        default="INFO",
        help="Logging level for Rich console output. Default: INFO",
    )
    parser.add_argument(
        "--info",
        action="store_true",
        help="Log graph summary before training.",
    )
    parser.add_argument(
        "--visualize",
        action="store_true",
        help="Show a graph visualization before training.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    setup_logger(args.log_level)
    logger.info("Starting GNN experiment ...")

    planetoid_name = resolve_planetoid_name(args.dataset)
    config = TrainConfig(epochs=args.epochs)
    dataset = load_planetoid(planetoid_name)
    data = dataset[0]

    if args.info:
        graph_info(data)
    if args.visualize:
        visualize_graph(data)

    model = GCN(dataset.num_features, dataset.num_classes, config.hidden_dim)
    train(model, data, config)
    acc = evaluate(model, data)
    logger.info("Accuracy: %f", acc)


if __name__ == "__main__":
    main()
