"""Pruebas de las rutas de ventas."""

# datetime crea las fechas de las ventas de prueba
from datetime import datetime
# Decimal permite comparar importes sin errores de redondeo
from decimal import Decimal

# Modelo de la tabla ventas
from app.models import Venta


def _crear_ventas(sesion, cantidad):
    """Inserta ventas de prueba con ids 1..cantidad."""
    # Recorre los números de 1 a cantidad
    for numero in range(1, cantidad + 1):
        # Marca una venta para guardarla (SQLite exige id explícito)
        sesion.add(
            Venta(
                id=numero,
                fecha=datetime(2026, 1, 1),
                cliente_id=numero,
                producto="Pan",
                cantidad=2,
                precio_unitario=Decimal("0.30"),
            )
        )
    # Confirma el guardado
    sesion.commit()


def test_listar_vacio(client):
    """Sin ventas, el total es 0 y no hay elementos."""
    # Pide la primera página
    respuesta = client.get("/ventas")
    # Debe responder 200 OK
    assert respuesta.status_code == 200
    # Total 0 y lista vacía
    assert respuesta.json() == {"total": 0, "items": []}


def test_paginacion(client, sesion_bd):
    """Limite y desplazamiento recortan la lista, el total no cambia."""
    # Prepara 5 ventas
    _crear_ventas(sesion_bd, 5)

    # Pide la segunda página de 2 elementos
    respuesta = client.get("/ventas?limite=2&desplazamiento=2")
    # Debe responder 200 OK
    assert respuesta.status_code == 200
    # Guarda el contenido recibido
    pagina = respuesta.json()
    # El total cuenta todas las ventas, no solo las de la página
    assert pagina["total"] == 5
    # La página trae las ventas 3 y 4
    assert [v["id"] for v in pagina["items"]] == [3, 4]


def test_limite_fuera_de_rango_devuelve_422(client):
    """Un límite mayor que 100 es inválido y debe devolver 422."""
    # Pide más ventas de las permitidas
    respuesta = client.get("/ventas?limite=101")
    # Debe responder 422 Unprocessable Entity
    assert respuesta.status_code == 422


def test_resumen(client, sesion_bd):
    """El resumen cuenta ventas y suma cantidad * precio."""
    # Prepara 5 ventas de 2 unidades a 0.30 (0.60 cada una)
    _crear_ventas(sesion_bd, 5)

    # Pide el resumen
    respuesta = client.get("/ventas/resumen")
    # Debe responder 200 OK
    assert respuesta.status_code == 200
    # Guarda el contenido recibido
    resumen = respuesta.json()
    # Debe contar las 5 ventas
    assert resumen["cantidad_ventas"] == 5
    # Los ingresos son 5 * 0.60 = 3.00
    assert Decimal(str(resumen["ingresos"])) == Decimal("3.00")
