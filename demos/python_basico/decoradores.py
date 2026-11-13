"""Demo de decoradores en Python.

Uso: python -m demos.python_basico.decoradores
"""

# functools.wraps conserva el nombre y la documentación originales
import functools
# time mide cuánto tarda una función
import time


def cronometrar(funcion):
    """Decorador que imprime cuánto tarda en ejecutarse la función."""

    # Conserva el nombre y la documentación de la función original
    @functools.wraps(funcion)
    def envoltura(*args, **kwargs):
        # Marca el instante de inicio
        inicio = time.perf_counter()
        # Ejecuta la función original con sus argumentos
        resultado = funcion(*args, **kwargs)
        # Imprime el tiempo transcurrido
        print(
            f"   [{funcion.__name__}] tardó "
            f"{time.perf_counter() - inicio:.4f} s"
        )
        # Devuelve el resultado original
        return resultado

    # Entrega la función envuelta en lugar de la original
    return envoltura


@cronometrar
def sumar_hasta(n):
    """Suma los números de 0 a n-1."""
    return sum(range(n))


print("1. Decorador simple")
print("   resultado:", sumar_hasta(1_000_000))
print("   nombre:", sumar_hasta.__name__, "| doc:", sumar_hasta.__doc__)


def restar(a, b):
    """Resta b de a."""
    return a - b


# Es lo mismo que usar @cronometrar encima de la función
restar = cronometrar(restar)
print("2. Sin la sintaxis @:")
print("   restar(10, 3) =", restar(10, 3))


def reintentar(veces):
    """Decorador con argumentos: reintenta si falla la conexión."""

    def decorador(funcion):
        # Conserva el nombre y la documentación de la función original
        @functools.wraps(funcion)
        def envoltura(*args, **kwargs):
            # Intenta todas las veces menos la última
            for intento in range(1, veces):
                # Prueba ejecutar la función
                try:
                    # Si funciona, devuelve el resultado y termina
                    return funcion(*args, **kwargs)
                # Si falla la conexión, informa y vuelve a intentar
                except ConnectionError as error:
                    print(f"   intento {intento} falló: {error}")
            # Último intento: si falla, el error sale hacia afuera
            return funcion(*args, **kwargs)

        # Entrega la función envuelta
        return envoltura

    # Entrega el decorador ya configurado
    return decorador


# Contador de llamadas para simular una API inestable
estado = {"llamadas": 0}


@reintentar(3)
def llamar_api():
    """Simula una API que falla las dos primeras veces."""
    # Cuenta esta llamada
    estado["llamadas"] += 1
    # Falla mientras lleve menos de 3 llamadas
    if estado["llamadas"] < 3:
        raise ConnectionError("sin red")
    # A la tercera llamada responde bien
    return "respuesta ok"


print("3. Decorador con argumentos")
print("   resultado:", llamar_api())

# Registro de rutas: (método, ruta) -> función
rutas = {}


def get(ruta):
    """Decorador que registra una función como ruta GET."""

    def registrar(funcion):
        # Guarda la función en el registro
        rutas[("GET", ruta)] = funcion
        # Devuelve la función sin modificarla
        return funcion

    # Entrega el decorador ya configurado
    return registrar


@get("/hola")
def saludar():
    """Responde con un saludo."""
    return {"mensaje": "hola"}


print("4. Registro de rutas, como hace FastAPI")
print("   rutas registradas:", list(rutas))
print("   simular GET /hola ->", rutas[("GET", "/hola")]())


def sin_wraps(funcion):
    """Decorador que NO usa functools.wraps (pierde el nombre)."""

    def envoltura(*args, **kwargs):
        # Ejecuta la función original
        return funcion(*args, **kwargs)

    # Entrega la envoltura, que tiene su propio nombre
    return envoltura


@sin_wraps
def tarea():
    """Documentación de tarea."""


print("5. Con y sin functools.wraps")
print("   sin wraps:", tarea.__name__, "| con wraps:", sumar_hasta.__name__)
