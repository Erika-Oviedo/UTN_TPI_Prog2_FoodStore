"""Pruebas del modelo y los servicios (sin menú). Ejecutar con: python pruebas.py"""
from collections.abc import Callable

from consola import Menu, MenuAdministrador, MenuCliente, crear_menu
from entidades import Base, Calculable, Categoria, Pedido, Producto, Usuario
from enums import Estado, FormaPago, Rol
from excepciones import (
    CantidadInvalidaError,
    CredencialesInvalidasError,
    DatoInvalidoError,
    DuplicadoError,
    EntidadNoEncontradaError,
    FoodStoreError,
    OperacionNoPermitidaError,
    PrecioInvalidoError,
    StockInsuficienteError,
    StockInvalidoError,
)
from servicios import CategoriaServicio, PedidoServicio, ProductoServicio, UsuarioServicio

resultados: list[bool] = []


def titulo(texto: str) -> None:
    print(f"\n=== {texto} ===")


def verificar(descripcion: str, condicion: bool) -> None:
    resultados.append(condicion)
    print(f"  [{'OK' if condicion else 'FALLO'}] {descripcion}")


def esperar_error(descripcion: str, accion: Callable[[], object], tipo: type[Exception]) -> None:
    """Caso de error esperado: pasa si la acción lanza la excepción indicada."""
    try:
        accion()
    except tipo as error:
        resultados.append(True)
        print(f"  [OK] {descripcion} -> {tipo.__name__}: {error}")
    except Exception as error:
        resultados.append(False)
        print(f"  [FALLO] {descripcion}: se esperaba {tipo.__name__} y llegó {type(error).__name__}")
    else:
        resultados.append(False)
        print(f"  [FALLO] {descripcion}: no lanzó {tipo.__name__}")


def probar_entidades() -> None:
    titulo("ENTIDADES: clase abstracta, ids, encapsulamiento, __str__ y __eq__")
    esperar_error("Base no se puede instanciar", lambda: Base(), TypeError)  # type: ignore[abstract]
    esperar_error("Calculable (interfaz) no se puede instanciar", lambda: Calculable(), TypeError)  # type: ignore[abstract]

    categoria = Categoria("Pizzas", "Pizzas al horno")
    producto = Producto("Muzzarella", "Clásica", 7000, 10, "", True, categoria)
    usuario = Usuario("Ana", "Pérez", "ana@mail.com", "261555", "clave1", Rol.ADMIN)
    verificar("los ids se asignan solos y desde 1 en cada entidad", categoria.id >= 1 and producto.id >= 1)
    verificar("creado_en se asigna en el constructor", producto.creado_en is not None)
    verificar("eliminado arranca en False", producto.eliminado is False)
    verificar("__str__ de Producto es una línea útil", "Muzzarella" in str(producto) and "Pizzas" in str(producto))
    verificar("__eq__ compara por id y tipo", producto == producto and producto != categoria)
    verificar("la categoría agrega a su producto (agregación 1..N)", producto in categoria.productos)

    esperar_error("no se puede leer la contraseña", lambda: usuario.contrasenia, AttributeError)
    verificar("verificar_contrasenia acepta la correcta", usuario.verificar_contrasenia("clave1"))
    verificar("verificar_contrasenia rechaza la incorrecta", not usuario.verificar_contrasenia("otra"))

    def precio_negativo() -> None:
        producto.precio = -1

    def stock_negativo() -> None:
        producto.stock = -5

    def mail_malo() -> None:
        usuario.mail = "sin-arroba"

    esperar_error("precio negativo en el setter", precio_negativo, PrecioInvalidoError)
    esperar_error("stock negativo en el setter", stock_negativo, StockInvalidoError)
    esperar_error("mail sin '@' ni '.'", mail_malo, DatoInvalidoError)
    esperar_error("categoría con nombre vacío", lambda: Categoria("  ", "x"), DatoInvalidoError)
    esperar_error("producto con precio negativo en el constructor",
                lambda: Producto("X", "", -10, 1, "", True, categoria), PrecioInvalidoError)


def probar_pedido() -> None:
    titulo("PEDIDO: composición, detalles y cálculo del total")
    categoria = Categoria("Bebidas", "Bebidas")
    gaseosa = Producto("Gaseosa", "", 1800, 5, "", True, categoria)
    agua = Producto("Agua", "", 1200, 10, "", True, categoria)
    cliente = Usuario("Juan", "Gómez", "juan@mail.com", "261", "x", Rol.USUARIO)
    pedido = Pedido(cliente, FormaPago.EFECTIVO)
    verificar("Pedido implementa Calculable", isinstance(pedido, Calculable))
    verificar("arranca PENDIENTE con fecha del día", pedido.estado is Estado.PENDIENTE)

    pedido.agregar_detalle(2, gaseosa)
    pedido.agregar_detalle(1, agua)
    pedido.calcular_total()
    verificar("subtotal = cantidad x precio del producto (2 x 1800)", pedido.detalles[0].subtotal == 3600)
    verificar("total = suma de subtotales (3600 + 1200)", pedido.total == 4800)
    pedido.agregar_detalle(2, gaseosa)
    verificar("mismo producto: se suma la cantidad al detalle existente", len(pedido.detalles) == 2
            and pedido.buscar_detalle_por_producto(gaseosa).cantidad == 4)  # type: ignore[union-attr]
    verificar("buscar_detalle_por_producto devuelve None si no está",
            pedido.buscar_detalle_por_producto(Producto("Otro", "", 1, 1, "", True, categoria)) is None)
    verificar("la property detalles devuelve una tupla (no se modifica desde afuera)",
            isinstance(pedido.detalles, tuple))
    pedido.eliminar_detalle_por_producto(agua)
    verificar("eliminar_detalle_por_producto recalcula el total", pedido.total == 7200)

    esperar_error("cantidad 0", lambda: pedido.agregar_detalle(0, gaseosa), CantidadInvalidaError)
    esperar_error("cantidad negativa", lambda: pedido.agregar_detalle(-3, gaseosa), CantidadInvalidaError)
    esperar_error("cantidad mayor al stock (4 + 2 > 5)", lambda: pedido.agregar_detalle(2, gaseosa),
                StockInsuficienteError)
    esperar_error("eliminar un detalle inexistente", lambda: pedido.eliminar_detalle_por_producto(agua),
                EntidadNoEncontradaError)
    esperar_error("pedido sin usuario", lambda: Pedido(None, FormaPago.EFECTIVO), DatoInvalidoError)  # type: ignore[arg-type]
    cliente.eliminado = True
    esperar_error("pedido con usuario eliminado", lambda: Pedido(cliente, FormaPago.EFECTIVO),
                OperacionNoPermitidaError)

    nuevo = Pedido(Usuario("A", "B", "a@b.com", "1", "x", Rol.USUARIO), FormaPago.TARJETA)
    nuevo.estado = Estado.CONFIRMADO
    nuevo.estado = Estado.TERMINADO
    verificar("transición PENDIENTE -> CONFIRMADO -> TERMINADO", nuevo.estado is Estado.TERMINADO)
    esperar_error("TERMINADO no cambia más", lambda: setattr(nuevo, "estado", Estado.CANCELADO),
                OperacionNoPermitidaError)
    saltado = Pedido(Usuario("C", "D", "c@d.com", "1", "x", Rol.USUARIO), FormaPago.TARJETA)
    esperar_error("PENDIENTE -> TERMINADO no es válida", lambda: setattr(saltado, "estado", Estado.TERMINADO),
                OperacionNoPermitidaError)


def preparar_servicios() -> tuple[UsuarioServicio, CategoriaServicio, ProductoServicio, PedidoServicio, Usuario, Usuario]:
    usuarios = UsuarioServicio()
    categorias = CategoriaServicio()
    productos = ProductoServicio(categorias)
    pedidos = PedidoServicio(usuarios, productos)
    admin = usuarios.registrar_administrador_inicial("Ana", "Pérez", "admin@foodstore.com", "261", "admin123")
    cliente = usuarios.crear(admin, "Juan", "Gómez", "juan@foodstore.com", "262", "cliente123", Rol.USUARIO)
    return usuarios, categorias, productos, pedidos, admin, cliente


def probar_categorias_y_productos() -> None:
    titulo("SERVICIOS: categorías y productos")
    usuarios, categorias, productos, pedidos, admin, cliente = preparar_servicios()
    pizzas = categorias.crear(admin, "Pizzas", "Pizzas al horno")
    verificar("crear categoría válida", pizzas in categorias.listar())
    esperar_error("nombre de categoría repetido (sin distinguir mayúsculas)",
                lambda: categorias.crear(admin, "PIZZAS", "otra"), DuplicadoError)
    esperar_error("categoría con descripción vacía", lambda: categorias.crear(admin, "Postres", ""), DatoInvalidoError)
    categorias.editar(admin, pizzas.id, nombre="Pizzas y empanadas")
    verificar("editar categoría", pizzas.nombre == "Pizzas y empanadas")
    esperar_error("editar categoría inexistente", lambda: categorias.editar(admin, 999, nombre="x"),
                EntidadNoEncontradaError)

    muzza = productos.crear(admin, "Muzzarella", "", 7000, 10, "", True, pizzas.id)
    verificar("crear producto válido", muzza in productos.listar())
    esperar_error("producto con precio negativo", lambda: productos.crear(admin, "X", "", -1, 1, "", True, pizzas.id),
                PrecioInvalidoError)
    esperar_error("producto con stock negativo", lambda: productos.crear(admin, "X", "", 1, -1, "", True, pizzas.id),
                StockInvalidoError)
    esperar_error("producto con categoría inexistente", lambda: productos.crear(admin, "X", "", 1, 1, "", True, 99),
                EntidadNoEncontradaError)
    esperar_error("editar producto con precio inválido",
                lambda: productos.editar(admin, muzza.id, nombre="Nuevo", precio=-5), PrecioInvalidoError)
    verificar("una edición inválida no deja cambios parciales", muzza.nombre == "Muzzarella")
    productos.editar(admin, muzza.id, precio=7500, stock=4)
    verificar("editar precio y stock", muzza.precio == 7500 and muzza.stock == 4)

    esperar_error("eliminar categoría con productos activos", lambda: categorias.eliminar(admin, pizzas.id),
                OperacionNoPermitidaError)
    sin_stock = productos.crear(admin, "Agotada", "", 100, 0, "", True, pizzas.id)
    oculto = productos.crear(admin, "Oculta", "", 100, 5, "", False, pizzas.id)
    visibles = productos.listar_disponibles()
    verificar("el cliente ve solo productos disponibles y con stock > 0",
            muzza in visibles and sin_stock not in visibles and oculto not in visibles)
    productos.eliminar(admin, muzza.id)
    productos.eliminar(admin, sin_stock.id)
    productos.eliminar(admin, oculto.id)
    verificar("baja lógica: el producto sale de los listados", muzza not in productos.listar())
    verificar("baja lógica: el objeto sigue en memoria", muzza.eliminado is True)
    categorias.eliminar(admin, pizzas.id)
    verificar("categoría sin productos activos se puede eliminar (baja lógica)", pizzas.eliminado)

    esperar_error("un cliente no puede crear categorías", lambda: categorias.crear(cliente, "Nueva", "x"),
                OperacionNoPermitidaError)
    esperar_error("un cliente no puede crear productos", lambda: productos.crear(cliente, "X", "", 1, 1, "", True, 1),
                OperacionNoPermitidaError)


def probar_usuarios() -> None:
    titulo("SERVICIOS: usuarios e inicio de sesión")
    usuarios, categorias, productos, pedidos, admin, cliente = preparar_servicios()
    verificar("autenticar con credenciales correctas", usuarios.autenticar("admin@foodstore.com", "admin123") is admin)
    esperar_error("contraseña incorrecta", lambda: usuarios.autenticar("admin@foodstore.com", "mala"),
                CredencialesInvalidasError)
    esperar_error("mail inexistente", lambda: usuarios.autenticar("nadie@foodstore.com", "x"),
                CredencialesInvalidasError)
    mensajes: set[str] = set()
    for mail, clave in (("admin@foodstore.com", "mala"), ("nadie@foodstore.com", "x")):
        try:
            usuarios.autenticar(mail, clave)
        except CredencialesInvalidasError as error:
            mensajes.add(str(error))
    verificar("el mensaje no revela qué dato falló", mensajes == {"Mail o contraseña incorrectos"})
    esperar_error("mail duplicado",
                lambda: usuarios.crear(admin, "X", "Y", "JUAN@foodstore.com", "1", "x", Rol.USUARIO), DuplicadoError)
    esperar_error("mail sin formato válido",
                lambda: usuarios.crear(admin, "X", "Y", "mail-malo", "1", "x", Rol.USUARIO), DatoInvalidoError)
    esperar_error("segundo administrador inicial", lambda: usuarios.registrar_administrador_inicial(
        "A", "B", "otro@foodstore.com", "1", "x"), OperacionNoPermitidaError)
    esperar_error("un administrador no puede eliminarse a sí mismo", lambda: usuarios.eliminar(admin, admin.id),
                OperacionNoPermitidaError)
    esperar_error("un cliente no puede eliminar usuarios", lambda: usuarios.eliminar(cliente, admin.id),
                OperacionNoPermitidaError)
    usuarios.eliminar(admin, cliente.id)
    verificar("usuario eliminado: baja lógica y fuera de listados", cliente.eliminado and cliente not in usuarios.listar())
    esperar_error("un usuario eliminado no puede iniciar sesión",
                lambda: usuarios.autenticar("juan@foodstore.com", "cliente123"), CredencialesInvalidasError)


def probar_pedidos_y_stock() -> None:
    titulo("SERVICIOS: pedidos, stock y transiciones")
    usuarios, categorias, productos, pedidos, admin, cliente = preparar_servicios()
    otro = usuarios.crear(admin, "Luz", "Díaz", "luz@foodstore.com", "263", "x", Rol.USUARIO)
    bebidas = categorias.crear(admin, "Bebidas", "Bebidas")
    gaseosa = productos.crear(admin, "Gaseosa", "", 1800, 5, "", True, bebidas.id)
    agua = productos.crear(admin, "Agua", "", 1200, 10, "", True, bebidas.id)

    pedido = pedidos.crear_borrador(admin, cliente.id, FormaPago.TARJETA)
    pedidos.agregar_detalle(admin, pedido, gaseosa.id, 3)
    pedidos.agregar_detalle(admin, pedido, agua.id, 2)
    verificar("el stock NO se toca mientras se arma el pedido", gaseosa.stock == 5 and agua.stock == 10)
    pedidos.registrar(admin, pedido)
    verificar("al registrar se descuenta el stock", gaseosa.stock == 2 and agua.stock == 8)
    verificar("el total se calculó con calcular_total()", pedido.total == 3 * 1800 + 2 * 1200)

    fallido = pedidos.crear_borrador(admin, cliente.id, FormaPago.EFECTIVO)
    pedidos.agregar_detalle(admin, fallido, agua.id, 1)
    esperar_error("pedido con más cantidad que stock (queda cancelado)",
                lambda: pedidos.agregar_detalle(admin, fallido, gaseosa.id, 3), StockInsuficienteError)
    verificar("pedido cancelado por falta de stock: no se guardó y el stock no cambió",
            fallido not in pedidos.listar(admin) and gaseosa.stock == 2 and agua.stock == 8)
    esperar_error("crear pedido con usuario inexistente", lambda: pedidos.crear_borrador(admin, 999, FormaPago.EFECTIVO),
                EntidadNoEncontradaError)
    esperar_error("registrar un pedido sin detalles",
                lambda: pedidos.registrar(admin, pedidos.crear_borrador(admin, cliente.id, FormaPago.EFECTIVO)),
                DatoInvalidoError)

    pedidos.actualizar(admin, pedido.id, estado=Estado.CONFIRMADO, forma_pago=FormaPago.TRANSFERENCIA)
    verificar("cambio de estado y de forma de pago", pedido.estado is Estado.CONFIRMADO
            and pedido.forma_pago is FormaPago.TRANSFERENCIA)
    esperar_error("transición inválida CONFIRMADO -> PENDIENTE",
                lambda: pedidos.actualizar(admin, pedido.id, estado=Estado.PENDIENTE), OperacionNoPermitidaError)
    pedidos.actualizar(admin, pedido.id, estado=Estado.CANCELADO)
    verificar("al CANCELAR se devuelve el stock", gaseosa.stock == 5 and agua.stock == 10)
    esperar_error("CANCELADO no cambia más",
                lambda: pedidos.actualizar(admin, pedido.id, estado=Estado.TERMINADO), OperacionNoPermitidaError)

    p2 = pedidos.crear_borrador(admin, cliente.id, FormaPago.EFECTIVO)
    pedidos.agregar_detalle(admin, p2, gaseosa.id, 4)
    pedidos.registrar(admin, p2)
    pedidos.eliminar(admin, p2.id)
    verificar("eliminar un pedido no terminado devuelve el stock", gaseosa.stock == 5)
    verificar("baja lógica del pedido y de sus detalles",
            p2.eliminado and all(d.eliminado for d in p2.detalles) and p2 not in pedidos.listar(admin))

    p3 = pedidos.crear_borrador(admin, cliente.id, FormaPago.EFECTIVO)
    pedidos.agregar_detalle(admin, p3, agua.id, 2)
    pedidos.registrar(admin, p3)
    pedidos.actualizar(admin, p3.id, estado=Estado.CONFIRMADO)
    pedidos.actualizar(admin, p3.id, estado=Estado.TERMINADO)
    pedidos.eliminar(admin, p3.id)
    verificar("eliminar un pedido TERMINADO NO devuelve el stock", agua.stock == 8)

    p4 = pedidos.crear_borrador(admin, cliente.id, FormaPago.EFECTIVO)
    pedidos.agregar_detalle(admin, p4, agua.id, 1)
    pedidos.registrar(admin, p4)
    verificar("el cliente ve solo sus pedidos", p4 in pedidos.listar_propios(cliente)
            and p4 not in pedidos.listar_propios(otro))
    esperar_error("pedido de otro usuario se informa como inexistente",
                lambda: pedidos.obtener_propio(otro, p4.id), EntidadNoEncontradaError)
    esperar_error("un cliente no puede listar todos los pedidos", lambda: pedidos.listar(cliente),
                OperacionNoPermitidaError)
    esperar_error("un cliente no puede crear pedidos",
                lambda: pedidos.crear_borrador(cliente, cliente.id, FormaPago.EFECTIVO), OperacionNoPermitidaError)

    productos.eliminar(admin, agua.id)
    verificar("producto eliminado: el pedido existente se sigue mostrando", "Agua" in str(p4.detalles[0]))
    nuevo = pedidos.crear_borrador(admin, cliente.id, FormaPago.EFECTIVO)
    esperar_error("producto eliminado no se puede agregar a pedidos nuevos",
                lambda: pedidos.agregar_detalle(admin, nuevo, agua.id, 1), EntidadNoEncontradaError)


def probar_menus_polimorficos() -> None:
    titulo("CONSOLA: menú por rol resuelto con polimorfismo")
    usuarios, categorias, productos, pedidos, admin, cliente = preparar_servicios()
    menu_admin = crear_menu(admin, categorias, productos, usuarios, pedidos)
    menu_cliente = crear_menu(cliente, categorias, productos, usuarios, pedidos)
    verificar("ADMIN recibe MenuAdministrador", isinstance(menu_admin, MenuAdministrador))
    verificar("USUARIO recibe MenuCliente", isinstance(menu_cliente, MenuCliente))
    verificar("ambos son Menu y se usan con menu.mostrar()", isinstance(menu_admin, Menu) and isinstance(menu_cliente, Menu))
    esperar_error("Menu es abstracta", lambda: Menu(admin), TypeError)  # type: ignore[abstract]


def main() -> None:
    print("PRUEBAS DE FOOD STORE")
    probar_entidades()
    probar_pedido()
    probar_categorias_y_productos()
    probar_usuarios()
    probar_pedidos_y_stock()
    probar_menus_polimorficos()
    ok = sum(resultados)
    print(f"\nRESUMEN: {ok} de {len(resultados)} verificaciones correctas.")
    if ok != len(resultados):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
