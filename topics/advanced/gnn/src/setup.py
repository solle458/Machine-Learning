import logging
import pathlib
from logging import getLogger

from rich.logging import RichHandler
from torch_geometric.datasets import Planetoid

logger = getLogger(__name__)


def download_data() -> Planetoid:
    """
    Download the Cora dataset and return a PyTorch Geometric Dataset object.
    Args:
        None
    Returns:
        Planetoid: A PyTorch Geometric Planetoid object.
    Raises:
        None
    Example:
        >>> dataset = download_data()
        >>> print(dataset[0])
    """
    root = pathlib.Path("data/Cora")
    if root.exists():
        logger.info("Loading Cora dataset from %s", root.resolve())
    else:
        logger.info("Downloading Cora dataset to %s ...", root.resolve())
    dataset = Planetoid(root=str(root), name="Cora")
    logger.info("Cora dataset ready (%d graph(s)).", len(dataset))
    return dataset

def setup_logger(level: str = "NOTSET") -> None:
    """
    Setup the logger.
    Args:
        level: The level of the logger.
    Returns:
        None
    Raises:
        None
    Example:
    """
    root = pathlib.Path("logs")
    if root.exists():
        logger.info("Loading logs from %s", root.resolve())
    else:
        logger.info("Creating logs directory at %s", root.resolve())
        root.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level="NOTSET", #レベルはRichHandlerで設定する
        format="%(message)s",
        datefmt="[%X]",
        handlers=[
            RichHandler(
                rich_tracebacks=True,
                tracebacks_show_locals=True,
                level=level,
            ),
            logging.FileHandler(root / "app.log", encoding="utf-8")
        ],
    )
    logger.info("Logger setup complete.")
