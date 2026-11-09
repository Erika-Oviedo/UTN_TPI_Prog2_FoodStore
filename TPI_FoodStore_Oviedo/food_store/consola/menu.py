from abc import ABC, abstractmethod

from entidades import Usuario


class Menu(ABC):
    """Menú principal de un rol. Cada rol tiene su subclase (polimorfismo)."""

    def __init__(self, usuario: Usuario) -> None:
        self._usuario: Usuario = usuario

    @abstractmethod
    def mostrar(self) -> bool:
        """Muestra el menú. True = cerrar sesión, False = salir del programa."""
        ...
