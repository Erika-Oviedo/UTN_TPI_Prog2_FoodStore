from entidades.base import Base
from enums import Rol
from excepciones import DatoInvalidoError


class Usuario(Base):
    """Usuario del sistema (cliente o administrador)."""

    def __init__(
        self,
        nombre: str,
        apellido: str,
        mail: str,
        celular: str,
        contrasenia: str,
        rol: Rol,
    ) -> None:
        # Se valida antes de llamar a super().__init__() para no consumir ids
        # cuando el constructor falla (los ids quedan correlativos).
        self.nombre = nombre
        self.apellido = apellido
        self.mail = mail
        self.celular = celular
        self.contrasenia = contrasenia
        self.rol = rol
        super().__init__()

    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        self.__nombre: str = _texto(valor, "El nombre")

    @property
    def apellido(self) -> str:
        return self.__apellido

    @apellido.setter
    def apellido(self, valor: str) -> None:
        self.__apellido: str = _texto(valor, "El apellido")

    @property
    def mail(self) -> str:
        return self.__mail

    @mail.setter
    def mail(self, valor: str) -> None:
        valor = _texto(valor, "El mail")
        if "@" not in valor or "." not in valor:
            raise DatoInvalidoError("El mail debe contener '@' y '.'")
        self.__mail: str = valor

    @property
    def celular(self) -> str:
        return self.__celular

    @celular.setter
    def celular(self, valor: str) -> None:
        self.__celular: str = _texto(valor, "El celular")

    def _establecer_contrasenia(self, valor: str) -> None:
        self.__contrasenia: str = _texto(valor, "La contraseña")

    # Propiedad de solo escritura: leer 'usuario.contrasenia' lanza AttributeError,
    # así la contraseña nunca sale del objeto.
    contrasenia = property(fset=_establecer_contrasenia)

    @property
    def rol(self) -> Rol:
        return self.__rol

    @rol.setter
    def rol(self, valor: Rol) -> None:
        if not isinstance(valor, Rol):
            raise DatoInvalidoError("El rol debe ser un valor del enumerado Rol")
        self.__rol: Rol = valor

    def verificar_contrasenia(self, contrasenia: str) -> bool:
        """Compara la contraseña recibida sin exponer la almacenada."""
        return self.__contrasenia == contrasenia

    @property
    def nombre_completo(self) -> str:
        return f"{self.nombre} {self.apellido}"

    def __str__(self) -> str:
        return f"[{self.id}] {self.nombre_completo} - {self.mail} - {self.rol.name}"


def _texto(valor: str, campo: str) -> str:
    if not isinstance(valor, str) or not valor.strip():
        raise DatoInvalidoError(f"{campo} no puede estar en blanco")
    return valor.strip()
