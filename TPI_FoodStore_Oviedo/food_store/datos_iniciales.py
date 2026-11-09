"""Datos de arranque: administrador inicial y datos de ejemplo (todo vía servicios)."""
from enums import FormaPago, Rol
from servicios import CategoriaServicio, PedidoServicio, ProductoServicio, UsuarioServicio

ADMIN_MAIL = "admin@foodstore.com"
ADMIN_CONTRASENIA = "admin123"


def cargar_datos_iniciales(
    usuarios: UsuarioServicio,
    categorias: CategoriaServicio,
    productos: ProductoServicio,
    pedidos: PedidoServicio,
) -> None:
    admin = usuarios.registrar_administrador_inicial(
        "Ana", "Pérez", ADMIN_MAIL, "2615550001", ADMIN_CONTRASENIA
    )
    cliente = usuarios.crear(
        admin, "Juan", "Gómez", "juan@foodstore.com", "2615550002", "cliente123", Rol.USUARIO
    )

    hamburguesas = categorias.crear(admin, "Hamburguesas", "Hamburguesas artesanales")
    pizzas = categorias.crear(admin, "Pizzas", "Pizzas al horno de piedra")
    bebidas = categorias.crear(admin, "Bebidas", "Gaseosas y aguas")
    postres = categorias.crear(admin, "Postres", "Dulces caseros")

    clasica = productos.crear(admin, "Hamburguesa clásica", "Carne, lechuga y tomate", 4500, 20, "", True, hamburguesas.id)
    productos.crear(admin, "Hamburguesa doble cheddar", "Doble carne y cheddar", 6200, 15, "", True, hamburguesas.id)
    productos.crear(admin, "Pizza muzzarella", "Muzzarella y aceitunas", 7000, 10, "", True, pizzas.id)
    productos.crear(admin, "Pizza napolitana", "Tomate, ajo y muzzarella", 8200, 3, "", True, pizzas.id)
    gaseosa = productos.crear(admin, "Gaseosa 500 ml", "Línea cola", 1800, 40, "", True, bebidas.id)
    productos.crear(admin, "Agua mineral", "Sin gas, 500 ml", 1200, 50, "", True, bebidas.id)
    productos.crear(admin, "Flan casero", "Con dulce de leche", 2500, 12, "", True, postres.id)
    productos.crear(admin, "Brownie con helado", "Temporalmente fuera de carta", 3800, 8, "", False, postres.id)

    pedido = pedidos.crear_borrador(admin, cliente.id, FormaPago.TARJETA)
    pedidos.agregar_detalle(admin, pedido, clasica.id, 2)
    pedidos.agregar_detalle(admin, pedido, gaseosa.id, 1)
    pedidos.registrar(admin, pedido)
