from entidades import Usuario
from enums import Rol
from excepciones import (
    CredencialesInvalidasError,
    DuplicadoError,
    EntidadNoEncontradaError,
    OperacionNoPermitidaError,
)
from servicios.permisos import exigir_admin

MENSAJE_CREDENCIALES = "Mail o contraseña incorrectos"


class UsuarioServicio:
    """Colección de usuarios, autenticación y reglas de negocio."""

    def __init__(self) -> None:
        self.__usuarios: list[Usuario] = []

    def registrar_administrador_inicial(
        self, nombre: str, apellido: str, mail: str, celular: str, contrasenia: str
    ) -> Usuario:
        """Alta del primer administrador (arranque del sistema). Solo si no hay ninguno activo."""
        if any(u.rol is Rol.ADMIN and not u.eliminado for u in self.__usuarios):
            raise OperacionNoPermitidaError("Ya existe un administrador activo")
        return self.__agregar(nombre, apellido, mail, celular, contrasenia, Rol.ADMIN)

    def crear(
        self,
        actor: Usuario,
        nombre: str,
        apellido: str,
        mail: str,
        celular: str,
        contrasenia: str,
        rol: Rol,
    ) -> Usuario:
        exigir_admin(actor)
        return self.__agregar(nombre, apellido, mail, celular, contrasenia, rol)

    def autenticar(self, mail: str, contrasenia: str) -> Usuario:
        """Devuelve el usuario o lanza CredencialesInvalidasError (mismo mensaje en los 3 casos)."""
        buscado = mail.strip().lower() if isinstance(mail, str) else ""
        for usuario in self.__usuarios:
            if usuario.mail.lower() == buscado:
                if usuario.eliminado or not usuario.verificar_contrasenia(contrasenia):
                    break
                return usuario
        raise CredencialesInvalidasError(MENSAJE_CREDENCIALES)

    def obtener(self, id_usuario: int) -> Usuario:
        for usuario in self.__usuarios:
            if usuario.id == id_usuario and not usuario.eliminado:
                return usuario
        raise EntidadNoEncontradaError(f"No existe el usuario con id {id_usuario}")

    def listar(self) -> list[Usuario]:
        return [u for u in self.__usuarios if not u.eliminado]

    def editar(
        self,
        actor: Usuario,
        id_usuario: int,
        nombre: str | None = None,
        apellido: str | None = None,
        mail: str | None = None,
        celular: str | None = None,
        contrasenia: str | None = None,
        rol: Rol | None = None,
    ) -> Usuario:
        exigir_admin(actor)
        usuario = self.obtener(id_usuario)
        if mail is not None:
            self.__validar_mail_unico(mail, excluir=usuario)
        if rol is not None and rol is not Rol.ADMIN and usuario is actor:
            raise OperacionNoPermitidaError("Un administrador no puede quitarse su propio rol")
        anterior = (usuario.nombre, usuario.apellido, usuario.mail, usuario.celular, usuario.rol)
        try:
            if nombre is not None:
                usuario.nombre = nombre
            if apellido is not None:
                usuario.apellido = apellido
            if mail is not None:
                usuario.mail = mail
            if celular is not None:
                usuario.celular = celular
            if contrasenia is not None:
                usuario.contrasenia = contrasenia
            if rol is not None:
                usuario.rol = rol
        except Exception:
            usuario.nombre, usuario.apellido, usuario.mail, usuario.celular, usuario.rol = anterior
            raise
        return usuario

    def eliminar(self, actor: Usuario, id_usuario: int) -> None:
        exigir_admin(actor)
        usuario = self.obtener(id_usuario)
        if usuario is actor:
            raise OperacionNoPermitidaError("Un administrador no puede eliminarse a sí mismo")
        usuario.eliminado = True

    def __agregar(
        self, nombre: str, apellido: str, mail: str, celular: str, contrasenia: str, rol: Rol
    ) -> Usuario:
        self.__validar_mail_unico(mail)
        usuario = Usuario(nombre, apellido, mail, celular, contrasenia, rol)
        self.__usuarios.append(usuario)
        return usuario

    def __validar_mail_unico(self, mail: str, excluir: Usuario | None = None) -> None:
        buscado = mail.strip().lower() if isinstance(mail, str) else ""
        for usuario in self.__usuarios:  # incluye eliminados: el mail sigue reservado
            if usuario is not excluir and usuario.mail.lower() == buscado:
                raise DuplicadoError(f"Ya existe un usuario con el mail '{mail.strip()}'")
