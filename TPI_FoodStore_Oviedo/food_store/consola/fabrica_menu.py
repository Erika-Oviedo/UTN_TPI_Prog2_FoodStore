from consola.menu import Menu
from consola.menu_administrador import MenuAdministrador
from consola.menu_cliente import MenuCliente
from entidades import Usuario
from enums import Rol
from servicios import CategoriaServicio, PedidoServicio, ProductoServicio, UsuarioServicio


def crear_menu(
    usuario: Usuario,
    categorias: CategoriaServicio,
    productos: ProductoServicio,
    usuarios: UsuarioServicio,
    pedidos: PedidoServicio,
) -> Menu:
    """Único lugar donde se pregunta el rol; después solo se llama a menu.mostrar()."""
    if usuario.rol == Rol.ADMIN:
        return MenuAdministrador(usuario, categorias, productos, usuarios, pedidos)
    return MenuCliente(usuario, categorias, productos, pedidos)
