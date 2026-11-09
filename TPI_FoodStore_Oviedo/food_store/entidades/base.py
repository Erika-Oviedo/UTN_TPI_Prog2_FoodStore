from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any


class Base(ABC):
    """Superclase abstracta de todas las entidades.

    Asigna el id automáticamente con un contador por clase (cada entidad
    numera desde 1), marca la baja lógica y guarda la fecha de creación.
    """

    __contadores: dict[type, int] = {}

    def __init__(self) -> None:
        clase: type = type(self)
        Base.__contadores[clase] = Base.__contadores.get(clase, 0) + 1
        self.__id: int = Base.__contadores[clase]
        self.__eliminado: bool = False
        self.__creado_en: datetime = datetime.now()

    @property
    def id(self) -> int:
        return self.__id

    @property
    def eliminado(self) -> bool:
        return self.__eliminado

    @eliminado.setter
    def eliminado(self, valor: bool) -> None:
        if not isinstance(valor, bool):
            raise TypeError("'eliminado' debe ser un booleano")
        self.__eliminado = valor

    @property
    def creado_en(self) -> datetime:
        return self.__creado_en

    @abstractmethod
    def __str__(self) -> str:
        """Cada entidad devuelve una línea útil para los listados de consola."""
        ...

    def __eq__(self, otro: Any) -> bool:
        if not isinstance(otro, Base):
            return NotImplemented
        # Los contadores son por clase: el id solo es único dentro de su tipo.
        return type(self) is type(otro) and self.id == otro.id

    def __hash__(self) -> int:
        return hash((type(self), self.id))
