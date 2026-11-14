"""Pruebas de las rutas de productos."""

# Decimal permite comparar precios sin errores de redondeo
from decimal import Decimal


def test_listar_vacio(client):
    """Sin productos creados, la lista debe estar vacía."""
    # Pide la lista de productos
    respuesta = client.get("/productos")
    # Debe responder 200 OK
    assert respuesta.status_code == 200
    # Y devolver una lista vacía
    assert respuesta.json() == []


def test_crear_y_obtener(client):
    """Un producto creado se puede consultar por su id."""
    # Crea un producto
    respuesta = client.post(
        "/productos",
        json={"nombre": "Jugo", "precio": "2.50", "stock": 10},
    )
    # Debe responder 201 Created
    assert respuesta.status_code == 201
    # Guarda el producto devuelto
    creado = respuesta.json()
    # El nombre debe ser el enviado
    assert creado["nombre"] == "Jugo"

    # Consulta el producto por su id
    consulta = client.get(f"/productos/{creado['id']}")
    # Debe responder 200 OK
    assert consulta.status_code == 200
    # El precio debe coincidir exactamente
    assert Decimal(consulta.json()["precio"]) == Decimal("2.50")


def test_obtener_inexistente(client):
    """Pedir un id que no existe debe devolver 404."""
    # Consulta un producto que no existe
    respuesta = client.get("/productos/999")
    # Debe responder 404 Not Found
    assert respuesta.status_code == 404


def test_precio_negativo_devuelve_422(client):
    """Un precio negativo es inválido y debe devolver 422."""
    # Intenta crear un producto con precio negativo
    respuesta = client.post(
        "/productos",
        json={"nombre": "Jugo", "precio": "-1"},
    )
    # Debe responder 422 Unprocessable Entity
    assert respuesta.status_code == 422
