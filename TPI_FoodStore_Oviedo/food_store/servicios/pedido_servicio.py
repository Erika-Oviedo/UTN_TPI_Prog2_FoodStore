from entidades import Pedido, Usuario
from enums import Estado, FormaPago
from excepciones import (
    DatoInvalidoError,
    EntidadNoEncontradaError,
    OperacionNoPermitidaError,
    StockInsuficienteError,
)
from servicios.permisos import exigir_admin
from servicios.producto_servicio import ProductoServicio
from servicios.usuario_servicio import UsuarioServicio

ESTADOS_FINALES: tuple[Estado, ...] = (Estado.TERMINADO, Estado.CANCELADO)


class PedidoServicio:
    """Colección de pedidos, descuento/devolución de stock y reglas de negocio."""

    def __init__(self, usuarios: UsuarioServicio, productos: ProductoServicio) -> None:
        self.__usuarios: UsuarioServicio = usuarios
        self.__productos: ProductoServicio = productos
        self.__pedidos: list[Pedido] = []

    # ---- creación en tres pasos: borrador -> detalles -> registrar ----
    def crear_borrador(self, actor: Usuario, id_usuario: int, forma_pago: FormaPago) -> Pedido:
        """Crea el pedido PENDIENTE en memoria: todavía NO está en la colección."""
        exigir_admin(actor)
        usuario = self.__usuarios.obtener(id_usuario)
        return Pedido(usuario, forma_pago)

    def agregar_detalle(self, actor: Usuario, pedido: Pedido, id_producto: int, cantidad: int) -> None:
        """Usa Pedido.agregar_detalle: valida cantidad y stock pero no descuenta nada."""
        exigir_admin(actor)
        producto = self.__productos.obtener(id_producto)
        pedido.agregar_detalle(cantidad, producto)

    def registrar(self, actor: Usuario, pedido: Pedido) -> Pedido:
        """Cierra la creación: calcula el total, descuenta el stock y guarda el pedido."""
        exigir_admin(actor)
        if not pedido.detalles:
            raise DatoInvalidoError("El pedido necesita al menos un detalle")
        for detalle in pedido.detalles:  # se verifica todo antes de tocar el stock
            if detalle.cantidad > detalle.producto.stock:
                raise StockInsuficienteError(
                    f"Stock insuficiente de '{detalle.producto.nombre}': pedido "
                    f"{detalle.cantidad}, disponible {detalle.producto.stock}"
                )
        pedido.calcular_total()
        for detalle in pedido.detalles:
            detalle.producto.descontar_stock(detalle.cantidad)
        self.__pedidos.append(pedido)
        return pedido

    # ---- consultas ----
    def obtener(self, id_pedido: int) -> Pedido:
        for pedido in self.__pedidos:
            if pedido.id == id_pedido and not pedido.eliminado:
                return pedido
        raise EntidadNoEncontradaError(f"No existe el pedido con id {id_pedido}")

    def listar(self, actor: Usuario, id_usuario: int | None = None) -> list[Pedido]:
        """Vista del administrador: todos los pedidos no eliminados, opcionalmente de un usuario."""
        exigir_admin(actor)
        pedidos = [p for p in self.__pedidos if not p.eliminado]
        if id_usuario is not None:
            pedidos = [p for p in pedidos if p.usuario.id == id_usuario]
        return pedidos

    def listar_propios(self, usuario: Usuario) -> list[Pedido]:
        """Vista del cliente: solo sus pedidos no eliminados."""
        return [p for p in self.__pedidos if not p.eliminado and p.usuario is usuario]

    def obtener_propio(self, usuario: Usuario, id_pedido: int) -> Pedido:
        """El pedido de otro usuario se informa como inexistente."""
        for pedido in self.listar_propios(usuario):
            if pedido.id == id_pedido:
                return pedido
        raise EntidadNoEncontradaError(f"No existe el pedido con id {id_pedido}")

    # ---- modificaciones ----
    def actualizar(
        self,
        actor: Usuario,
        id_pedido: int,
        estado: Estado | None = None,
        forma_pago: FormaPago | None = None,
    ) -> Pedido:
        exigir_admin(actor)
        pedido = self.obtener(id_pedido)
        if forma_pago is not None and pedido.estado in ESTADOS_FINALES:
            raise OperacionNoPermitidaError(
                f"No se puede cambiar la forma de pago de un pedido {pedido.estado.name}"
            )
        if estado is not None:
            pedido.estado = estado  # valida la transición; si falla no cambia nada
            if estado is Estado.CANCELADO:
                self.__devolver_stock(pedido)
        if forma_pago is not None:
            pedido.forma_pago = forma_pago
        return pedido

    def eliminar(self, actor: Usuario, id_pedido: int) -> None:
        exigir_admin(actor)
        pedido = self.obtener(id_pedido)
        if pedido.estado not in ESTADOS_FINALES:
            self.__devolver_stock(pedido)
        pedido._marcar_eliminado()

    @staticmethod
    def __devolver_stock(pedido: Pedido) -> None:
        for detalle in pedido.detalles:
            detalle.producto.devolver_stock(detalle.cantidad)
