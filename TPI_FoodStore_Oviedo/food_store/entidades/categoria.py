from typing import TYPE_CHECKING

from entidades.base import Base
from excepciones import DatoInvalidoError

if TYPE_CHECKING:
    from entidades.producto import Producto


class Categoria(Base):
    """Categoría del catálogo. Agrega (1..N) productos."""

    def __init__(self, nombre: str, descripcion: str) -> None:
        # Se valida antes de llamar a super().__init__() para no consumir ids
        # cuando el constructor falla (los ids quedan correlativos).
        self.nombre = nombre
        self.descripcion = descripcion
        super().__init__()
        self.__productos: list["Producto"] = []

    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        self.__nombre: str = _texto_obligatorio(valor, "El nombre de la categoría")

    @property
    def descripcion(self) -> str:
        return self.__descripcion

    @descripcion.setter
    def descripcion(self, valor: str) -> None:
        self.__descripcion: str = _texto_obligatorio(valor, "La descripción de la categoría")

    @property
    def productos(self) -> tuple["Producto", ...]:
        """Productos asociados (copia inmutable, incluye eliminados)."""
        return tuple(self.__productos)

    def cantidad_productos_activos(self) -> int:
        """Cantidad de productos no eliminados de esta categoría."""
        return sum(1 for p in self.__productos if not p.eliminado)

    def _agregar_producto(self, producto: "Producto") -> None:
        """Uso interno: lo invoca Producto al asignarse esta categoría."""
        if producto not in self.__productos:
            self.__productos.append(producto)

    def _quitar_producto(self, producto: "Producto") -> None:
        """Uso interno: lo invoca Producto al cambiar de categoría."""
        if producto in self.__productos:
            self.__productos.remove(producto)

    def __str__(self) -> str:
        return f"[{self.id}] {self.nombre} - {self.descripcion}"


def _texto_obligatorio(valor: str, campo: str) -> str:
    if not isinstance(valor, str) or not valor.strip():
        raise DatoInvalidoError(f"{campo} no puede estar en blanco")
    return valor.strip()
