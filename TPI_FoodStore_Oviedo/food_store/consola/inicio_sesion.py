from consola.entrada import leer_contrasenia, mostrar_error
from entidades import Usuario
from excepciones import CredencialesInvalidasError
from servicios import UsuarioServicio

MAX_INTENTOS = 3


def iniciar_sesion(usuarios: UsuarioServicio) -> Usuario | None:
    """Pide mail y contraseña (hasta 3 intentos). Devuelve None si se agotan."""
    print("\n=== FOOD STORE – INICIO DE SESIÓN ===")
    for intento in range(1, MAX_INTENTOS + 1):
        mail = input("Mail: ").strip()
        contrasenia = leer_contrasenia("Contraseña: ")
        try:
            usuario = usuarios.autenticar(mail, contrasenia)
        except CredencialesInvalidasError as error:
            mostrar_error(f"{error} (intento {intento} de {MAX_INTENTOS})")
            continue
        print(f"\nBienvenido/a, {usuario.nombre_completo} [{usuario.rol.name}]")
        return usuario
    print(f"\nSe superó el máximo de {MAX_INTENTOS} intentos. El programa finalizará.")
    return None
