"""Lectura validada por teclado y utilidades de menú (capa de consola)."""
from collections.abc import Callable
from enum import Enum
from getpass import getpass
from typing import TypeVar

from excepciones import FoodStoreError

E = TypeVar("E", bound=Enum)


def mostrar_exito(mensaje: str) -> None:
    print(f"[OK] {mensaje}")


def mostrar_error(mensaje: str) -> None:
    print(f"[ERROR] {mensaje}")


def leer_texto(prompt: str) -> str:
    """Texto obligatorio: repite hasta que no esté vacío."""
    while True:
        valor = input(prompt).strip()
        if valor:
            return valor
        mostrar_error("El texto no puede estar vacío.")


def leer_texto_libre(prompt: str) -> str:
    """Texto que puede quedar vacío."""
    return input(prompt).strip()


def leer_texto_opcional(prompt: str) -> str | None:
    """Enter conserva el valor anterior (devuelve None)."""
    valor = input(prompt).strip()
    return valor or None


def leer_contrasenia(prompt: str) -> str:
    return getpass(prompt)


def leer_contrasenia_opcional(prompt: str) -> str | None:
    valor = getpass(prompt)
    return valor or None


def leer_entero(prompt: str) -> int:
    while True:
        try:
            return int(input(prompt).strip())
        except ValueError:
            mostrar_error("Ingrese un número entero válido.")


def leer_entero_opcional(prompt: str) -> int | None:
    while True:
        texto = input(prompt).strip()
        if not texto:
            return None
        try:
            return int(texto)
        except ValueError:
            mostrar_error("Ingrese un número entero válido o Enter para omitir.")


def leer_flotante(prompt: str) -> float:
    while True:
        try:
            return float(input(prompt).strip().replace(",", "."))
        except ValueError:
            mostrar_error("Ingrese un número válido (ej: 1500.50).")


def leer_flotante_opcional(prompt: str) -> float | None:
    while True:
        texto = input(prompt).strip().replace(",", ".")
        if not texto:
            return None
        try:
            return float(texto)
        except ValueError:
            mostrar_error("Ingrese un número válido o Enter para omitir.")


def leer_si_no(prompt: str) -> bool:
    while True:
        respuesta = input(prompt).strip().upper()
        if respuesta in ("S", "N"):
            return respuesta == "S"
        mostrar_error("Responda S o N.")


def leer_si_no_opcional(prompt: str) -> bool | None:
    while True:
        respuesta = input(prompt).strip().upper()
        if not respuesta:
            return None
        if respuesta in ("S", "N"):
            return respuesta == "S"
        mostrar_error("Responda S, N o Enter para conservar.")


def _mostrar_opciones_enum(enumerado: type[E], titulo: str) -> list[E]:
    miembros = list(enumerado)
    print(f"{titulo}:")
    for numero, miembro in enumerate(miembros, start=1):
        print(f"  {numero}. {miembro.name}")
    return miembros


def elegir_enum(enumerado: type[E], titulo: str) -> E:
    """Las opciones de un enumerado se eligen por número, nunca escribiendo el texto."""
    miembros = _mostrar_opciones_enum(enumerado, titulo)
    while True:
        numero = leer_entero("Seleccione: ")
        if 1 <= numero <= len(miembros):
            return miembros[numero - 1]
        mostrar_error(f"Elija un número entre 1 y {len(miembros)}.")


def elegir_enum_opcional(enumerado: type[E], titulo: str) -> E | None:
    """Igual que elegir_enum, pero Enter conserva el valor actual."""
    miembros = _mostrar_opciones_enum(enumerado, titulo)
    while True:
        numero = leer_entero_opcional("Seleccione (Enter conserva): ")
        if numero is None:
            return None
        if 1 <= numero <= len(miembros):
            return miembros[numero - 1]
        mostrar_error(f"Elija un número entre 1 y {len(miembros)}.")


def leer_opcion(validas: set[int]) -> int:
    """Lee una opción de menú; las fuera de rango o no numéricas se informan y se repiten."""
    while True:
        texto = input("Seleccione: ").strip()
        if texto.isdigit() and int(texto) in validas:
            return int(texto)
        mostrar_error("Opción inválida.")


def ejecutar_seguro(accion: Callable[[], None]) -> None:
    """Ejecuta una acción de menú: un error se informa y se vuelve al menú, nunca cierra el programa."""
    try:
        accion()
    except FoodStoreError as error:
        mostrar_error(str(error))
    except ValueError as error:
        mostrar_error(f"Valor inválido: {error}")
    except EOFError:
        raise  # entrada cerrada: lo maneja main() para terminar ordenadamente
    except Exception as error:  # red de seguridad: el menú nunca se cae
        mostrar_error(f"Error inesperado: {error}")


def ejecutar_submenu(titulo: str, acciones: list[tuple[str, Callable[[], None]]]) -> None:
    """Muestra un submenú numerado (más '0. Volver') y ejecuta la acción elegida."""
    validas = set(range(len(acciones) + 1))
    while True:
        print(f"\n--- {titulo} ---")
        for numero, (nombre, _) in enumerate(acciones, start=1):
            print(f"{numero}. {nombre}")
        print("0. Volver")
        opcion = leer_opcion(validas)
        if opcion == 0:
            return
        ejecutar_seguro(acciones[opcion - 1][1])
