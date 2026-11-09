"""Punto de entrada de Food Store: crea los servicios y arranca el ciclo de sesión."""
from consola import crear_menu, iniciar_sesion
from datos_iniciales import cargar_datos_iniciales
from servicios import CategoriaServicio, PedidoServicio, ProductoServicio, UsuarioServicio


def main() -> None:
    usuarios = UsuarioServicio()
    categorias = CategoriaServicio()
    productos = ProductoServicio(categorias)
    pedidos = PedidoServicio(usuarios, productos)
    cargar_datos_iniciales(usuarios, categorias, productos, pedidos)

    try:
        while True:
            sesion = iniciar_sesion(usuarios)  # la sesión es una variable local, no global
            if sesion is None:
                break
            menu = crear_menu(sesion, categorias, productos, usuarios, pedidos)
            if not menu.mostrar():  # False = salir del programa
                break
    except (EOFError, KeyboardInterrupt):
        print("\nEntrada interrumpida.")
    print("\nHasta luego, ¡gracias por usar Food Store!")


if __name__ == "__main__":
    main()
