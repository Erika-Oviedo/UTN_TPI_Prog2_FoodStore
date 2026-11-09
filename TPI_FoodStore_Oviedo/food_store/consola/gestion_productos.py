from consola.entrada import (
    ejecutar_submenu, leer_entero, leer_entero_opcional, leer_flotante, leer_flotante_opcional,
    leer_si_no, leer_si_no_opcional, leer_texto, leer_texto_libre, leer_texto_opcional,
    mostrar_exito,
)
from consola.vistas import listar_categorias, listar_productos
from entidades import Usuario
from servicios import CategoriaServicio, ProductoServicio


class GestionProductos:
    """Submenú de administrador: alta, baja, modificación y consulta de productos."""

    def __init__(
        self, actor: Usuario, productos: ProductoServicio, categorias: CategoriaServicio
    ) -> None:
        self.__actor: Usuario = actor
        self.__productos: ProductoServicio = productos
        self.__categorias: CategoriaServicio = categorias

    def mostrar(self) -> None:
        ejecutar_submenu("PRODUCTOS", [
            ("Listar", self.__listar),
            ("Crear", self.__crear),
            ("Editar", self.__editar),
            ("Eliminar", self.__eliminar),
        ])

    def __listar(self) -> None:
        id_categoria = leer_entero_opcional("Id de categoría para filtrar (Enter = todas): ")
        listar_productos(self.__productos.listar(id_categoria))

    def __crear(self) -> None:
        nombre = leer_texto("Nombre: ")
        descripcion = leer_texto_libre("Descripción: ")
        precio = leer_flotante("Precio: ")
        stock = leer_entero("Stock: ")
        imagen = leer_texto_libre("Imagen (ruta o URL): ")
        disponible = leer_si_no("¿Disponible? (S/N): ")
        listar_categorias(self.__categorias.listar())
        id_categoria = leer_entero("Id de la categoría: ")
        producto = self.__productos.crear(
            self.__actor, nombre, descripcion, precio, stock, imagen, disponible, id_categoria
        )
        mostrar_exito(f"Producto creado con id {producto.id}.")

    def __editar(self) -> None:
        listar_productos(self.__productos.listar())
        producto = self.__productos.obtener(leer_entero("Id del producto a editar: "))
        print("Enter conserva el valor actual en cada campo.")
        nombre = leer_texto_opcional(f"Nombre ({producto.nombre}): ")
        descripcion = leer_texto_opcional(f"Descripción ({producto.descripcion}): ")
        precio = leer_flotante_opcional(f"Precio ({producto.precio:.2f}): ")
        stock = leer_entero_opcional(f"Stock ({producto.stock}): ")
        imagen = leer_texto_opcional(f"Imagen ({producto.imagen}): ")
        disponible = leer_si_no_opcional(f"¿Disponible? S/N ({'S' if producto.disponible else 'N'}): ")
        id_categoria = leer_entero_opcional(f"Id de categoría ({producto.categoria.id}): ")
        self.__productos.editar(
            self.__actor, producto.id, nombre, descripcion, precio, stock, imagen,
            disponible, id_categoria,
        )
        mostrar_exito("Producto actualizado.")

    def __eliminar(self) -> None:
        listar_productos(self.__productos.listar())
        producto = self.__productos.obtener(leer_entero("Id del producto a eliminar: "))
        if not leer_si_no(f"¿Eliminar el producto '{producto.nombre}'? (S/N): "):
            print("Operación cancelada.")
            return
        self.__productos.eliminar(self.__actor, producto.id)
        mostrar_exito("Producto eliminado.")
