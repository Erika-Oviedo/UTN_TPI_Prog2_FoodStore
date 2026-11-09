from consola.entrada import (
    ejecutar_submenu, elegir_enum, elegir_enum_opcional, leer_entero, leer_si_no, mostrar_error,
    mostrar_exito,
)
from consola.vistas import (
    listar_pedidos, listar_productos, listar_usuarios, mostrar_pedido_con_detalles,
)
from entidades import Pedido, Usuario
from enums import Estado, FormaPago
from excepciones import FoodStoreError
from servicios import PedidoServicio, ProductoServicio, UsuarioServicio


class GestionPedidos:
    """Submenú de administrador: alta, baja, modificación y consulta de pedidos."""

    def __init__(
        self,
        actor: Usuario,
        pedidos: PedidoServicio,
        usuarios: UsuarioServicio,
        productos: ProductoServicio,
    ) -> None:
        self.__actor: Usuario = actor
        self.__pedidos: PedidoServicio = pedidos
        self.__usuarios: UsuarioServicio = usuarios
        self.__productos: ProductoServicio = productos

    def mostrar(self) -> None:
        ejecutar_submenu("PEDIDOS", [
            ("Listar todos", self.__listar),
            ("Listar por usuario", self.__listar_por_usuario),
            ("Ver detalles de un pedido", self.__ver_detalles),
            ("Crear pedido", self.__crear),
            ("Cambiar estado y/o forma de pago", self.__actualizar),
            ("Eliminar", self.__eliminar),
        ])

    def __listar(self) -> None:
        listar_pedidos(self.__pedidos.listar(self.__actor))

    def __listar_por_usuario(self) -> None:
        listar_usuarios(self.__usuarios.listar())
        id_usuario = leer_entero("Id del usuario: ")
        listar_pedidos(self.__pedidos.listar(self.__actor, id_usuario))

    def __ver_detalles(self) -> None:
        self.__listar()
        pedido = self.__pedidos.obtener(leer_entero("Id del pedido: "))
        mostrar_pedido_con_detalles(pedido)

    def __crear(self) -> None:
        listar_usuarios(self.__usuarios.listar())
        id_usuario = leer_entero("Id del usuario: ")
        forma_pago = elegir_enum(FormaPago, "Forma de pago")
        pedido = self.__pedidos.crear_borrador(self.__actor, id_usuario, forma_pago)
        try:
            self.__cargar_detalles(pedido)
            registrado = self.__pedidos.registrar(self.__actor, pedido)
        except FoodStoreError as error:
            mostrar_error(str(error))
            print("Creación cancelada: el pedido no se guardó y no se modificó ningún stock.")
            return
        mostrar_exito(f"Pedido creado con id {registrado.id}. Total: ${registrado.total:.2f}")

    def __cargar_detalles(self, pedido: Pedido) -> None:
        while True:
            listar_productos(self.__productos.listar())
            id_producto = leer_entero("Id del producto: ")
            cantidad = leer_entero("Cantidad: ")
            self.__pedidos.agregar_detalle(self.__actor, pedido, id_producto, cantidad)
            mostrar_exito(f"Detalle agregado. Total parcial: ${pedido.total:.2f}")
            if not leer_si_no("¿Agregar otro producto? (S/N): "):
                return

    def __actualizar(self) -> None:
        self.__listar()
        pedido = self.__pedidos.obtener(leer_entero("Id del pedido: "))
        estado = elegir_enum_opcional(Estado, f"Estado actual: {pedido.estado.name}. Nuevo estado")
        forma_pago = elegir_enum_opcional(
            FormaPago, f"Forma de pago actual: {pedido.forma_pago.name}. Nueva forma de pago"
        )
        if estado is None and forma_pago is None:
            print("No se indicó ningún cambio.")
            return
        self.__pedidos.actualizar(self.__actor, pedido.id, estado, forma_pago)
        mostrar_exito("Pedido actualizado.")

    def __eliminar(self) -> None:
        self.__listar()
        pedido = self.__pedidos.obtener(leer_entero("Id del pedido a eliminar: "))
        if not leer_si_no(f"¿Eliminar el pedido {pedido.id}? (S/N): "):
            print("Operación cancelada.")
            return
        self.__pedidos.eliminar(self.__actor, pedido.id)
        mostrar_exito("Pedido eliminado.")
