"""Excepciones propias de Food Store. Todas heredan de FoodStoreError."""


class FoodStoreError(Exception):
    """Error base del dominio: la consola la captura para mostrar mensajes de negocio."""


class EntidadNoEncontradaError(FoodStoreError):
    """El id buscado no existe o la entidad está eliminada."""


class DatoInvalidoError(FoodStoreError):
    """Texto vacío, formato incorrecto o valor fuera de rango."""


class PrecioInvalidoError(DatoInvalidoError):
    """El precio es negativo o no es numérico."""


class StockInvalidoError(DatoInvalidoError):
    """El stock es negativo o no es un entero."""


class CantidadInvalidaError(DatoInvalidoError):
    """La cantidad de un detalle debe ser un entero mayor a cero."""


class StockInsuficienteError(FoodStoreError):
    """La cantidad pedida supera el stock disponible del producto."""


class DuplicadoError(FoodStoreError):
    """Mail de usuario o nombre de categoría repetido."""


class OperacionNoPermitidaError(FoodStoreError):
    """Transición de estado inválida, categoría con productos activos, falta de permisos, etc."""


class CredencialesInvalidasError(FoodStoreError):
    """Mail o contraseña incorrectos, o usuario eliminado."""
