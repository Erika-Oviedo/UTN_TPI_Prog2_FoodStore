from entidades.base import Base
from entidades.categoria import Categoria
from excepciones import (
    DatoInvalidoError,
    PrecioInvalidoError,
    StockInsuficienteError,
    StockInvalidoError,
)


class Producto(Base):
    """Producto del catálogo (N..1 con Categoria)."""

    def __init__(
        self,
        nombre: str,
        descripcion: str,
        precio: float,
        stock: int,
        imagen: str,
        disponible: bool,
        categoria: Categoria,
    ) -> None:
        # Se valida antes de llamar a super().__init__() para no consumir ids
        # cuando el constructor falla (los ids quedan correlativos).
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
        self.stock = stock
        self.imagen = imagen
        self.disponible = disponible
        if not isinstance(categoria, Categoria) or categoria.eliminado:
            raise DatoInvalidoError("El producto necesita una categoría válida y no eliminada")
        super().__init__()
        self.__categoria: Categoria | None = None
        self.categoria = categoria

    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        if not isinstance(valor, str) or not valor.strip():
            raise DatoInvalidoError("El nombre del producto no puede estar en blanco")
        self.__nombre: str = valor.strip()

    @property
    def descripcion(self) -> str:
        return self.__descripcion

    @descripcion.setter
    def descripcion(self, valor: str) -> None:
        if not isinstance(valor, str):
            raise DatoInvalidoError("La descripción debe ser texto")
        self.__descripcion: str = valor.strip()

    @property
    def precio(self) -> float:
        return self.__precio

    @precio.setter
    def precio(self, valor: float) -> None:
        if isinstance(valor, bool) or not isinstance(valor, (int, float)):
            raise PrecioInvalidoError("El precio debe ser un número")
        if valor < 0:
            raise PrecioInvalidoError("El precio no puede ser negativo")
        self.__precio: float = float(valor)

    @property
    def stock(self) -> int:
        return self.__stock

    @stock.setter
    def stock(self, valor: int) -> None:
        if isinstance(valor, bool) or not isinstance(valor, int):
            raise StockInvalidoError("El stock debe ser un número entero")
        if valor < 0:
            raise StockInvalidoError("El stock no puede ser negativo")
        self.__stock: int = valor

    @property
    def imagen(self) -> str:
        return self.__imagen

    @imagen.setter
    def imagen(self, valor: str) -> None:
        if not isinstance(valor, str):
            raise DatoInvalidoError("La imagen debe ser texto")
        self.__imagen: str = valor.strip()

    @property
    def disponible(self) -> bool:
        return self.__disponible

    @disponible.setter
    def disponible(self, valor: bool) -> None:
        if not isinstance(valor, bool):
            raise DatoInvalidoError("La disponibilidad debe ser verdadero o falso")
        self.__disponible: bool = valor

    @property
    def categoria(self) -> Categoria:
        return self.__categoria  # type: ignore[return-value]

    @categoria.setter
    def categoria(self, valor: Categoria) -> None:
        if not isinstance(valor, Categoria):
            raise DatoInvalidoError("El producto necesita una categoría válida")
        if valor.eliminado:
            raise DatoInvalidoError("La categoría está eliminada")
        if self.__categoria is not None:
            self.__categoria._quitar_producto(self)
        self.__categoria = valor
        valor._agregar_producto(self)

    def descontar_stock(self, cantidad: int) -> None:
        """Resta unidades al stock; falla si no alcanza."""
        if cantidad > self.__stock:
            raise StockInsuficienteError(
                f"Stock insuficiente de '{self.nombre}': pedido {cantidad}, disponible {self.__stock}"
            )
        self.__stock -= cantidad

    def devolver_stock(self, cantidad: int) -> None:
        """Suma unidades al stock (cancelaciones y bajas de pedidos)."""
        self.__stock += cantidad

    def __str__(self) -> str:
        estado = "disponible" if self.disponible else "no disponible"
        return (
            f"[{self.id}] {self.nombre} - ${self.precio:.2f} - stock {self.stock} "
            f"- {self.categoria.nombre} ({estado})"
        )
