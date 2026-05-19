from dataclasses import dataclass


@dataclass(frozen=True)
class TrainConfig:
    epochs: int = 200
    hidden_dim: int = 32
