from enum import Enum


class FormaPago(Enum):
    """Formas de pago admitidas por el negocio."""

    TARJETA = "TARJETA"
    TRANSFERENCIA = "TRANSFERENCIA"
    EFECTIVO = "EFECTIVO"
