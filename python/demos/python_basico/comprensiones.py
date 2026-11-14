"""Demo de comprensiones de listas y diccionarios.

Uso: python -m demos.python_basico.comprensiones
"""

# time mide la diferencia de velocidad entre bucle y comprensión
import time

# Lista de números de ejemplo
numeros = [1, 2, 3, 4, 5, 6]

# Lista vacía donde el bucle guardará los resultados
cuadrados = []
# Recorre cada número
for n in numeros:
    # Añade el cuadrado del número a la lista
    cuadrados.append(n * n)
print("1. Con bucle:       ", cuadrados)
# La misma operación en una sola línea
print("2. Comprensión:     ", [n * n for n in numeros])
# Solo se calculan los cuadrados de los números pares
print("3. Solo los pares:  ", [n * n for n in numeros if n % 2 == 0])

# Lista de diccionarios de ejemplo
productos = [
    {"nombre": "Agua", "precio": 0.75, "stock": 100},
    {"nombre": "Galletas", "precio": 1.5, "stock": 0},
    {"nombre": "Jugo", "precio": 2.5, "stock": 10},
]
# Extrae solo los nombres
print("4. Nombres:         ", [p["nombre"] for p in productos])
# Extrae los nombres de los productos con stock
print(
    "5. Con stock:       ",
    [p["nombre"] for p in productos if p["stock"] > 0],
)
# Crea un diccionario nombre -> precio
print("6. Diccionario:     ", {p["nombre"]: p["precio"] for p in productos})
# Elige un texto según el stock de cada producto
print(
    "7. Con condición:   ",
    ["agotado" if p["stock"] == 0 else "disponible" for p in productos],
)
# Combina cada elemento del primer ciclo con cada uno del segundo
print(
    "8. Dos ciclos:      ",
    [(a, b) for a in (1, 2) for b in ("x", "y")],
)

# Cantidad de elementos para la prueba de velocidad
N = 1_000_000

# Marca el inicio de la prueba con bucle
inicio = time.perf_counter()
# Lista vacía para los resultados
resultado = []
# Recorre un millón de números
for n in range(N):
    # Añade el doble de cada número
    resultado.append(n * 2)
# Tiempo que tardó el bucle
t_bucle = time.perf_counter() - inicio

# Marca el inicio de la prueba con comprensión
inicio = time.perf_counter()
# Genera la misma lista con una comprensión
resultado = [n * 2 for n in range(N)]
# Tiempo que tardó la comprensión
t_comp = time.perf_counter() - inicio

print(f"9. Bucle: {t_bucle:.3f} s | Comprensión: {t_comp:.3f} s")

# Con corchetes se crea la lista completa de inmediato
lista = [n * 2 for n in range(5)]
# Con paréntesis se crea un generador que calcula bajo demanda
gen = (n * 2 for n in range(5))
print("10. Corchetes:", lista, "| Paréntesis:", type(gen).__name__)
