from entidades.base import Base
from entidades.producto import Producto
from excepciones import CantidadInvalidaError


class DetallePedido(Base):
    """Línea de un pedido. Solo Pedido debe crearla: nace y muere con él."""

    def __init__(self, cantidad: int, producto: Producto) -> None:
        self.__producto: Producto = producto
        # El precio se toma del producto en el momento de agregarlo.
        self.__precio_unitario: float = producto.precio
        self.cantidad = cantidad
        super().__init__()

    @property
    def producto(self) -> Producto:
        return self.__producto

    @property
    def precio_unitario(self) -> float:
        return self.__precio_unitario

    @property
    def cantidad(self) -> int:
        return self.__cantidad

    @cantidad.setter
    def cantidad(self, valor: int) -> None:
        if isinstance(valor, bool) or not isinstance(valor, int) or valor <= 0:
            raise CantidadInvalidaError("La cantidad debe ser un entero mayor a 0")
        self.__cantidad: int = valor
        self.__subtotal: float = valor * self.__precio_unitario

    @property
    def subtotal(self) -> float:
        return self.__subtotal

    def __str__(self) -> str:
        return (
            f"{self.producto.nombre} x{self.cantidad} "
            f"(${self.precio_unitario:.2f} c/u) = ${self.subtotal:.2f}"
        )
