from entidades import Categoria, Usuario
from excepciones import DuplicadoError, EntidadNoEncontradaError, OperacionNoPermitidaError
from servicios.permisos import exigir_admin


class CategoriaServicio:
    """Colección de categorías y sus reglas de negocio."""

    def __init__(self) -> None:
        self.__categorias: list[Categoria] = []

    def crear(self, actor: Usuario, nombre: str, descripcion: str) -> Categoria:
        exigir_admin(actor)
        self.__validar_nombre_unico(nombre)
        categoria = Categoria(nombre, descripcion)
        self.__categorias.append(categoria)
        return categoria

    def obtener(self, id_categoria: int) -> Categoria:
        for categoria in self.__categorias:
            if categoria.id == id_categoria and not categoria.eliminado:
                return categoria
        raise EntidadNoEncontradaError(f"No existe la categoría con id {id_categoria}")

    def listar(self) -> list[Categoria]:
        return [c for c in self.__categorias if not c.eliminado]

    def editar(
        self,
        actor: Usuario,
        id_categoria: int,
        nombre: str | None = None,
        descripcion: str | None = None,
    ) -> Categoria:
        exigir_admin(actor)
        categoria = self.obtener(id_categoria)
        if nombre is not None:
            self.__validar_nombre_unico(nombre, excluir=categoria)
        anterior = (categoria.nombre, categoria.descripcion)
        try:
            if nombre is not None:
                categoria.nombre = nombre
            if descripcion is not None:
                categoria.descripcion = descripcion
        except Exception:
            categoria.nombre, categoria.descripcion = anterior  # sin cambios parciales
            raise
        return categoria

    def eliminar(self, actor: Usuario, id_categoria: int) -> None:
        exigir_admin(actor)
        categoria = self.obtener(id_categoria)
        activos = categoria.cantidad_productos_activos()
        if activos > 0:
            raise OperacionNoPermitidaError(
                f"No se puede eliminar la categoría '{categoria.nombre}': "
                f"tiene {activos} producto(s) activo(s)"
            )
        categoria.eliminado = True

    def __validar_nombre_unico(self, nombre: str, excluir: Categoria | None = None) -> None:
        buscado = nombre.strip().lower() if isinstance(nombre, str) else ""
        for categoria in self.listar():
            if categoria is not excluir and categoria.nombre.lower() == buscado:
                raise DuplicadoError(f"Ya existe una categoría llamada '{categoria.nombre}'")
