from consola.entrada import leer_opcion
from consola.gestion_categorias import GestionCategorias
from consola.gestion_pedidos import GestionPedidos
from consola.gestion_productos import GestionProductos
from consola.gestion_usuarios import GestionUsuarios
from consola.menu import Menu
from entidades import Usuario
from servicios import CategoriaServicio, PedidoServicio, ProductoServicio, UsuarioServicio


class MenuAdministrador(Menu):
    """Menú completo de gestión (alta, baja, modificación y consulta)."""

    def __init__(
        self,
        usuario: Usuario,
        categorias: CategoriaServicio,
        productos: ProductoServicio,
        usuarios: UsuarioServicio,
        pedidos: PedidoServicio,
    ) -> None:
        super().__init__(usuario)
        self.__gestiones: dict[int, GestionCategorias | GestionProductos | GestionUsuarios | GestionPedidos] = {
            1: GestionCategorias(usuario, categorias),
            2: GestionProductos(usuario, productos, categorias),
            3: GestionUsuarios(usuario, usuarios),
            4: GestionPedidos(usuario, pedidos, usuarios, productos),
        }

    def mostrar(self) -> bool:
        while True:
            print(f"\n=== FOOD STORE – ADMINISTRADOR ({self._usuario.nombre_completo}) ===")
            print("1. Categorías")
            print("2. Productos")
            print("3. Usuarios")
            print("4. Pedidos")
            print("9. Cerrar sesión")
            print("0. Salir")
            opcion = leer_opcion({0, 1, 2, 3, 4, 9})
            if opcion == 9:
                return True
            if opcion == 0:
                return False
            self.__gestiones[opcion].mostrar()
