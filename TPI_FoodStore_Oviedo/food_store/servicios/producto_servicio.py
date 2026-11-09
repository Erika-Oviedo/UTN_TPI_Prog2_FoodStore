from entidades import Producto, Usuario
from excepciones import EntidadNoEncontradaError
from servicios.categoria_servicio import CategoriaServicio
from servicios.permisos import exigir_admin


class ProductoServicio:
    """Colección de productos y sus reglas de negocio."""

    def __init__(self, categorias: CategoriaServicio) -> None:
        self.__categorias: CategoriaServicio = categorias
        self.__productos: list[Producto] = []

    def crear(
        self,
        actor: Usuario,
        nombre: str,
        descripcion: str,
        precio: float,
        stock: int,
        imagen: str,
        disponible: bool,
        id_categoria: int,
    ) -> Producto:
        exigir_admin(actor)
        categoria = self.__categorias.obtener(id_categoria)
        producto = Producto(nombre, descripcion, precio, stock, imagen, disponible, categoria)
        self.__productos.append(producto)
        return producto

    def obtener(self, id_producto: int) -> Producto:
        for producto in self.__productos:
            if producto.id == id_producto and not producto.eliminado:
                return producto
        raise EntidadNoEncontradaError(f"No existe el producto con id {id_producto}")

    def listar(self, id_categoria: int | None = None) -> list[Producto]:
        """Productos no eliminados (vista del administrador), opcionalmente por categoría."""
        productos = [p for p in self.__productos if not p.eliminado]
        if id_categoria is not None:
            productos = [p for p in productos if p.categoria.id == id_categoria]
        return productos

    def listar_disponibles(self, id_categoria: int | None = None) -> list[Producto]:
        """Vista del cliente: no eliminados, disponibles y con stock mayor a 0."""
        return [p for p in self.listar(id_categoria) if p.disponible and p.stock > 0]

    def editar(
        self,
        actor: Usuario,
        id_producto: int,
        nombre: str | None = None,
        descripcion: str | None = None,
        precio: float | None = None,
        stock: int | None = None,
        imagen: str | None = None,
        disponible: bool | None = None,
        id_categoria: int | None = None,
    ) -> Producto:
        """Modifica solo los campos recibidos; si alguno es inválido no se cambia nada."""
        exigir_admin(actor)
        producto = self.obtener(id_producto)
        categoria = self.__categorias.obtener(id_categoria) if id_categoria is not None else None
        anterior = (
            producto.nombre, producto.descripcion, producto.precio, producto.stock,
            producto.imagen, producto.disponible, producto.categoria,
        )
        try:
            if nombre is not None:
                producto.nombre = nombre
            if descripcion is not None:
                producto.descripcion = descripcion
            if precio is not None:
                producto.precio = precio
            if stock is not None:
                producto.stock = stock
            if imagen is not None:
                producto.imagen = imagen
            if disponible is not None:
                producto.disponible = disponible
            if categoria is not None:
                producto.categoria = categoria
        except Exception:
            (producto.nombre, producto.descripcion, producto.precio, producto.stock,
             producto.imagen, producto.disponible, producto.categoria) = anterior
            raise
        return producto

    def eliminar(self, actor: Usuario, id_producto: int) -> None:
        exigir_admin(actor)
        self.obtener(id_producto).eliminado = True
