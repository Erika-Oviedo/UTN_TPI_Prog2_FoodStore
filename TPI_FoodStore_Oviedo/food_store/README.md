# Food Store – Sistema de Gestión de Pedidos de Comida (consola)

Trabajo Práctico Integrador de **Programación II** – Tecnicatura Universitaria en Programación (UTN).
Sistema de consola en Python con Programación Orientada a Objetos: categorías, productos, usuarios y
pedidos con inicio de sesión por rol. Toda la información vive en memoria (se pierde al cerrar).

## Cómo ejecutarlo

- **Versión de Python:** 3.12 o superior (solo biblioteca estándar, sin instalar nada).
- **Programa:** `python main.py`
- **Pruebas del modelo y servicios (sin menú):** `python pruebas.py`

## Credenciales de ejemplo

| Rol     | Mail                  | Contraseña   |
|---------|-----------------------|--------------|
| ADMIN   | admin@foodstore.com   | admin123     |
| USUARIO | juan@foodstore.com    | cliente123   |

Al iniciar se cargan además 4 categorías, 8 productos y un pedido de ejemplo.
Hay 3 intentos de inicio de sesión; al tercer error el programa termina.

## Estructura

```
food_store/
├── main.py              # crea los servicios y arranca el ciclo de sesión
├── datos_iniciales.py   # administrador inicial y datos de ejemplo (vía servicios)
├── pruebas.py           # pruebas del modelo y servicios, sin menú
├── entidades/           # Base (abstracta), Calculable (interfaz), Categoria, Producto, Usuario, Pedido, DetallePedido
├── enums/               # Rol, Estado, FormaPago
├── excepciones/         # FoodStoreError y sus subclases
├── servicios/           # un servicio por entidad + permisos
└── consola/             # Menu (abstracta), MenuAdministrador, MenuCliente, gestiones y lectura validada
```

Dependencia en un solo sentido: consola → servicios → entidades.

## Enlaces (completar antes de entregar)

- Video demostración: _<pegar enlace con permisos públicos de visualización>_
- Informe en PDF: `Informe_TPI_FoodStore.pdf` (en la raíz de este repositorio)
