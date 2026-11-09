from enum import Enum


class Estado(Enum):
    """Estados posibles de un pedido."""

    PENDIENTE = "PENDIENTE"
    CONFIRMADO = "CONFIRMADO"
    TERMINADO = "TERMINADO"
    CANCELADO = "CANCELADO"
