from abc import ABC, abstractmethod


class Calculable(ABC):
    """Interfaz: el objeto que la implementa sabe actualizar su propio total."""

    @abstractmethod
    def calcular_total(self) -> None:
        """Actualiza el total del objeto."""
        ...
