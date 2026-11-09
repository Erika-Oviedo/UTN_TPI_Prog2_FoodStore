from datetime import date

from entidades.base import Base
from entidades.calculable import Calculable
from entidades.detalle_pedido import DetallePedido
from entidades.producto import Producto
from entidades.usuario import Usuario
from enums import Estado, FormaPago
from excepciones import (
    CantidadInvalidaError,
    DatoInvalidoError,
    EntidadNoEncontradaError,
    OperacionNoPermitidaError,
    StockInsuficienteError,
)

TRANSICIONES_VALIDAS: dict[Estado, tuple[Estado, ...]] = {
    Estado.PENDIENTE: (Estado.CONFIRMADO, Estado.CANCELADO),
    Estado.CONFIRMADO: (Estado.TERMINADO, Estado.CANCELADO),
    Estado.TERMINADO: (),
    Estado.CANCELADO: (),
}


class Pedido(Base, Calculable):
    """Pedido de un usuario. Compone (1..N) objetos DetallePedido."""

    def __init__(self, usuario: Usuario, forma_pago: FormaPago) -> None:
        if usuario is None or not isinstance(usuario, Usuario):
            raise DatoInvalidoError("No se puede crear un pedido sin usuario")
        if usuario.eliminado:
            raise OperacionNoPermitidaError("No se puede crear un pedido con un usuario eliminado")
        self.forma_pago = forma_pago
        super().__init__()
        self.__usuario: Usuario = usuario
        self.__fecha: date = date.today()
        self.__estado: Estado = Estado.PENDIENTE
        self.__total: float = 0.0
        self.__detalles: list[DetallePedido] = []

    @property
    def usuario(self) -> Usuario:
        return self.__usuario

    @property
    def fecha(self) -> date:
        return self.__fecha

    @property
    def estado(self) -> Estado:
        return self.__estado

    @estado.setter
    def estado(self, nuevo: Estado) -> None:
        if not isinstance(nuevo, Estado):
            raise DatoInvalidoError("El estado debe ser un valor del enumerado Estado")
        if nuevo not in TRANSICIONES_VALIDAS[self.__estado]:
            raise OperacionNoPermitidaError(
                f"Transición inválida: {self.__estado.name} -> {nuevo.name}"
            )
        self.__estado = nuevo

    @property
    def total(self) -> float:
        return self.__total

    @property
    def forma_pago(self) -> FormaPago:
        return self.__forma_pago

    @forma_pago.setter
    def forma_pago(self, valor: FormaPago) -> None:
        if not isinstance(valor, FormaPago):
            raise DatoInvalidoError("La forma de pago debe ser un valor del enumerado FormaPago")
        self.__forma_pago: FormaPago = valor

    @property
    def detalles(self) -> tuple[DetallePedido, ...]:
        """Copia inmutable: los detalles solo se modifican a través del pedido."""
        return tuple(self.__detalles)

    def agregar_detalle(self, cantidad: int, producto: Producto) -> None:
        """Agrega un detalle; si el producto ya está, suma la cantidad al existente."""
        if self.__estado is not Estado.PENDIENTE:
            raise OperacionNoPermitidaError("Solo se pueden modificar pedidos PENDIENTES")
        if isinstance(cantidad, bool) or not isinstance(cantidad, int) or cantidad <= 0:
            raise CantidadInvalidaError("La cantidad debe ser un entero mayor a 0")
        if producto.eliminado:
            raise EntidadNoEncontradaError("El producto está eliminado")
        if not producto.disponible:
            raise OperacionNoPermitidaError(f"El producto '{producto.nombre}' no está disponible")
        existente = self.buscar_detalle_por_producto(producto)
        cantidad_final = cantidad + (existente.cantidad if existente else 0)
        if cantidad_final > producto.stock:
            raise StockInsuficienteError(
                f"Stock insuficiente de '{producto.nombre}': pedido {cantidad_final}, "
                f"disponible {producto.stock}"
            )
        if existente:
            existente.cantidad = cantidad_final
        else:
            self.__detalles.append(DetallePedido(cantidad, producto))
        self.calcular_total()

    def buscar_detalle_por_producto(self, producto: Producto) -> DetallePedido | None:
        for detalle in self.__detalles:
            if detalle.producto == producto:
                return detalle
        return None

    def eliminar_detalle_por_producto(self, producto: Producto) -> None:
        if self.__estado is not Estado.PENDIENTE:
            raise OperacionNoPermitidaError("Solo se pueden modificar pedidos PENDIENTES")
        detalle = self.buscar_detalle_por_producto(producto)
        if detalle is None:
            raise EntidadNoEncontradaError(f"El pedido no incluye '{producto.nombre}'")
        self.__detalles.remove(detalle)
        self.calcular_total()

    def calcular_total(self) -> None:
        self.__total = sum(d.subtotal for d in self.__detalles)

    def _marcar_eliminado(self) -> None:
        """Baja lógica del pedido y de sus detalles (los detalles mueren con él)."""
        self.eliminado = True
        for detalle in self.__detalles:
            detalle.eliminado = True

    def __str__(self) -> str:
        return (
            f"[{self.id}] {self.usuario.nombre_completo} | {self.estado.name} | "
            f"{self.forma_pago.name} | ${self.total:.2f} | {self.fecha.isoformat()}"
        )
