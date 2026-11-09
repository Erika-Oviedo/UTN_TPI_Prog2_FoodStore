"""Funciones de impresión compartidas por los menús (no contienen reglas de negocio)."""
from collections.abc import Sequence

from entidades import Categoria, Pedido, Producto, Usuario


def listar_categorias(categorias: Sequence[Categoria]) -> None:
    if not categorias:
        print("No hay categorías cargadas.")
        return
    for categoria in categorias:
        print(f"  {categoria}")


def listar_productos(productos: Sequence[Producto]) -> None:
    if not productos:
        print("No hay productos para mostrar.")
        return
    for producto in productos:
        print(f"  {producto}")


def listar_usuarios(usuarios: Sequence[Usuario]) -> None:
    if not usuarios:
        print("No hay usuarios cargados.")
        return
    for usuario in usuarios:
        print(f"  {usuario}")


def listar_pedidos(pedidos: Sequence[Pedido]) -> None:
    if not pedidos:
        print("No hay pedidos para mostrar.")
        return
    for pedido in pedidos:
        print(f"  {pedido}")


def mostrar_pedido_con_detalles(pedido: Pedido) -> None:
    print(f"  {pedido}")
    for detalle in pedido.detalles:
        print(f"     - {detalle}")
    print(f"     TOTAL: ${pedido.total:.2f}")


def mostrar_datos_usuario(usuario: Usuario) -> None:
    print(f"  Nombre:   {usuario.nombre}")
    print(f"  Apellido: {usuario.apellido}")
    print(f"  Mail:     {usuario.mail}")
    print(f"  Celular:  {usuario.celular}")
    print(f"  Rol:      {usuario.rol.name}")
