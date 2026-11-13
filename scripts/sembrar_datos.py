"""Inserta usuarios y pedidos de prueba en la base de datos.

Uso: python -m scripts.sembrar_datos
"""

# select construye consultas SQL
from sqlalchemy import select

# Fábrica de sesiones de base de datos
from app.db.database import SessionLocal
# Modelos de las tablas pedidos y usuarios
from app.models import Pedido, Usuario

# Abre una sesión y la cierra sola al terminar
with SessionLocal() as session:
    # Busca si ya se sembraron los datos de prueba
    ya_existe = session.scalars(
        select(Usuario).where(Usuario.email == "cliente1@ejemplo.com")
    ).first()

    # Si ya existen, no se vuelve a insertar nada
    if ya_existe:
        print("Los datos de prueba ya existen, no se inserta nada")
    else:
        # Crea 5 usuarios
        for i in range(1, 6):
            # Usuario de prueba numerado
            usuario = Usuario(
                nombre=f"Cliente {i}",
                email=f"cliente{i}@ejemplo.com",
            )
            # Crea 3 pedidos para cada usuario
            for j in range(1, 4):
                # Añade el pedido a la lista del usuario
                usuario.pedidos.append(Pedido(total=i * 10 + j))
            # Marca el usuario (y sus pedidos) para guardarlos
            session.add(usuario)

        # Confirma todo el guardado de una vez
        session.commit()
        print("Sembrados 5 usuarios con 3 pedidos cada uno")
