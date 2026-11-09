from consola.entrada import (
    ejecutar_submenu, elegir_enum, elegir_enum_opcional, leer_contrasenia,
    leer_contrasenia_opcional, leer_entero, leer_si_no, leer_texto, leer_texto_opcional,
    mostrar_error, mostrar_exito,
)
from consola.vistas import listar_usuarios
from entidades import Usuario
from enums import Rol
from excepciones import DatoInvalidoError, DuplicadoError
from servicios import UsuarioServicio


class GestionUsuarios:
    """Submenú de administrador: alta, baja, modificación y consulta de usuarios."""

    def __init__(self, actor: Usuario, usuarios: UsuarioServicio) -> None:
        self.__actor: Usuario = actor
        self.__usuarios: UsuarioServicio = usuarios

    def mostrar(self) -> None:
        ejecutar_submenu("USUARIOS", [
            ("Listar", self.__listar),
            ("Crear", self.__crear),
            ("Editar", self.__editar),
            ("Eliminar", self.__eliminar),
        ])

    def __listar(self) -> None:
        listar_usuarios(self.__usuarios.listar())

    def __crear(self) -> None:
        nombre = leer_texto("Nombre: ")
        apellido = leer_texto("Apellido: ")
        celular = leer_texto("Celular: ")
        contrasenia = leer_contrasenia("Contraseña: ")
        while not contrasenia.strip():
            mostrar_error("La contraseña no puede estar vacía.")
            contrasenia = leer_contrasenia("Contraseña: ")
        rol = elegir_enum(Rol, "Rol")
        while True:  # si el mail es inválido o ya existe, se informa y se pide otro
            mail = leer_texto("Mail: ")
            try:
                usuario = self.__usuarios.crear(
                    self.__actor, nombre, apellido, mail, celular, contrasenia, rol
                )
                break
            except (DuplicadoError, DatoInvalidoError) as error:
                mostrar_error(str(error))
        mostrar_exito(f"Usuario creado con id {usuario.id}.")

    def __editar(self) -> None:
        self.__listar()
        usuario = self.__usuarios.obtener(leer_entero("Id del usuario a editar: "))
        print("Enter conserva el valor actual en cada campo.")
        nombre = leer_texto_opcional(f"Nombre ({usuario.nombre}): ")
        apellido = leer_texto_opcional(f"Apellido ({usuario.apellido}): ")
        mail = leer_texto_opcional(f"Mail ({usuario.mail}): ")
        celular = leer_texto_opcional(f"Celular ({usuario.celular}): ")
        contrasenia = leer_contrasenia_opcional("Nueva contraseña (Enter conserva): ")
        rol = elegir_enum_opcional(Rol, f"Rol actual: {usuario.rol.name}")
        self.__usuarios.editar(
            self.__actor, usuario.id, nombre, apellido, mail, celular, contrasenia, rol
        )
        mostrar_exito("Usuario actualizado.")

    def __eliminar(self) -> None:
        self.__listar()
        usuario = self.__usuarios.obtener(leer_entero("Id del usuario a eliminar: "))
        if not leer_si_no(f"¿Eliminar a '{usuario.nombre_completo}'? (S/N): "):
            print("Operación cancelada.")
            return
        self.__usuarios.eliminar(self.__actor, usuario.id)
        mostrar_exito("Usuario eliminado.")
