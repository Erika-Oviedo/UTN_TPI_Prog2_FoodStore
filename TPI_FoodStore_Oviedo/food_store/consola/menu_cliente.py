from consola.entrada import ejecutar_seguro, leer_entero_opcional, leer_opcion
from consola.menu import Menu
from consola.vistas import (
    listar_categorias, listar_pedidos, listar_productos, mostrar_datos_usuario,
    mostrar_pedido_con_detalles,
)
from entidades import Usuario
from servicios import CategoriaServicio, PedidoServicio, ProductoServicio


class MenuCliente(Menu):
    """Menú de solo consulta: no ofrece ninguna opción que modifique datos."""

    def __init__(
        self,
        usuario: Usuario,
        categorias: CategoriaServicio,
        productos: ProductoServicio,
        pedidos: PedidoServicio,
    ) -> None:
        super().__init__(usuario)
        self.__categorias: CategoriaServicio = categorias
        self.__productos: ProductoServicio = productos
        self.__pedidos: PedidoServicio = pedidos

    def mostrar(self) -> bool:
        while True:
            print(f"\n=== FOOD STORE – CLIENTE ({self._usuario.nombre_completo}) ===")
            print("1. Ver categorías")
            print("2. Ver productos disponibles")
            print("3. Mis pedidos")
            print("4. Mis datos")
            print("9. Cerrar sesión")
            print("0. Salir")
            opcion = leer_opcion({0, 1, 2, 3, 4, 9})
            if opcion == 9:
                return True
            if opcion == 0:
                return False
            ejecutar_seguro({
                1: self.__ver_categorias,
                2: self.__ver_productos,
                3: self.__mis_pedidos,
                4: self.__mis_datos,
            }[opcion])

    def __ver_categorias(self) -> None:
        listar_categorias(self.__categorias.listar())

    def __ver_productos(self) -> None:
        listar_productos(self.__productos.listar_disponibles())

    def __mis_pedidos(self) -> None:
        listar_pedidos(self.__pedidos.listar_propios(self._usuario))
        id_pedido = leer_entero_opcional("Id del pedido para ver sus detalles (Enter para volver): ")
        if id_pedido is not None:
            mostrar_pedido_con_detalles(self.__pedidos.obtener_propio(self._usuario, id_pedido))

    def __mis_datos(self) -> None:
        mostrar_datos_usuario(self._usuario)
