# interpoladores/config.py

from dataclasses import dataclass
from typing import Optional

@dataclass
class IDWConfig:
    power: float = 2.0
    n_neighbors: Optional[int] = None
    max_distance: Optional[float] = None  # se quiser limitar a influência

@dataclass
class KrigagemConfig:
    modelo_variograma: str = "spherical"
    enable_plot: bool = False  # futuramente útil
