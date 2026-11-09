from entidades import Usuario
from enums import Rol
from excepciones import OperacionNoPermitidaError


def exigir_admin(actor: Usuario) -> None:
    """Solo un usuario con rol ADMIN puede crear, editar o eliminar datos."""
    if actor is None or actor.eliminado or actor.rol is not Rol.ADMIN:
        raise OperacionNoPermitidaError("Solo un administrador puede realizar esta operación")
