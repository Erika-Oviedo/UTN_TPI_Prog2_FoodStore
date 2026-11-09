from consola.entrada import (
    ejecutar_submenu, leer_entero, leer_si_no, leer_texto, leer_texto_opcional, mostrar_exito,
)
from consola.vistas import listar_categorias
from entidades import Usuario
from servicios import CategoriaServicio


class GestionCategorias:
    """Submenú de administrador: alta, baja, modificación y consulta de categorías."""

    def __init__(self, actor: Usuario, categorias: CategoriaServicio) -> None:
        self.__actor: Usuario = actor
        self.__categorias: CategoriaServicio = categorias

    def mostrar(self) -> None:
        ejecutar_submenu("CATEGORÍAS", [
            ("Listar", self.__listar),
            ("Crear", self.__crear),
            ("Editar", self.__editar),
            ("Eliminar", self.__eliminar),
        ])

    def __listar(self) -> None:
        listar_categorias(self.__categorias.listar())

    def __crear(self) -> None:
        nombre = leer_texto("Nombre: ")
        descripcion = leer_texto("Descripción: ")
        categoria = self.__categorias.crear(self.__actor, nombre, descripcion)
        mostrar_exito(f"Categoría creada con id {categoria.id}.")

    def __editar(self) -> None:
        self.__listar()
        categoria = self.__categorias.obtener(leer_entero("Id de la categoría a editar: "))
        nombre = leer_texto_opcional(f"Nuevo nombre (Enter conserva '{categoria.nombre}'): ")
        descripcion = leer_texto_opcional("Nueva descripción (Enter conserva la actual): ")
        self.__categorias.editar(self.__actor, categoria.id, nombre, descripcion)
        mostrar_exito("Categoría actualizada.")

    def __eliminar(self) -> None:
        self.__listar()
        categoria = self.__categorias.obtener(leer_entero("Id de la categoría a eliminar: "))
        if not leer_si_no(f"¿Eliminar la categoría '{categoria.nombre}'? (S/N): "):
            print("Operación cancelada.")
            return
        self.__categorias.eliminar(self.__actor, categoria.id)
        mostrar_exito("Categoría eliminada.")
