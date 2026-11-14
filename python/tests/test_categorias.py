"""Pruebas de las rutas de categorías."""


def test_listar_vacio(client):
    """Sin categorías creadas, la lista debe estar vacía."""
    # Pide la lista de categorías
    respuesta = client.get("/categorias")
    # Debe responder 200 OK
    assert respuesta.status_code == 200
    # Y devolver una lista vacía
    assert respuesta.json() == []


def test_crear_y_listar(client):
    """Una categoría creada aparece en la lista."""
    # Crea una categoría
    respuesta = client.post("/categorias", json={"nombre": "Bebidas"})
    # Debe responder 201 Created
    assert respuesta.status_code == 201
    # Debe devolver el nombre enviado y un id generado
    assert respuesta.json()["nombre"] == "Bebidas"
    assert respuesta.json()["id"] == 1

    # Pide la lista de categorías
    lista = client.get("/categorias").json()
    # Debe contener únicamente la categoría creada
    assert [c["nombre"] for c in lista] == ["Bebidas"]


def test_nombre_corto_devuelve_422(client):
    """Un nombre de una sola letra es inválido y debe devolver 422."""
    # Intenta crear una categoría con nombre demasiado corto
    respuesta = client.post("/categorias", json={"nombre": "A"})
    # Debe responder 422 Unprocessable Entity
    assert respuesta.status_code == 422
