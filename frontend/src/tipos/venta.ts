// Tipos de las ventas, iguales a los de python/app/schemas/venta.py

// Una venta tal como la devuelve la API
export interface Venta {
  // Identificador de la venta
  id: number
  // Fecha y hora en formato ISO, por ejemplo "2026-09-26T08:55:00"
  fecha: string
  // Número del cliente
  cliente_id: number
  // Nombre del producto vendido
  producto: string
  // Unidades vendidas
  cantidad: number
  // Precio de cada unidad, como texto para no perder decimales
  precio_unitario: string
}

// Una página de ventas con el total de ventas existentes
export interface PaginaVentas {
  // Cantidad total de ventas en la tabla
  total: number
  // Ventas de esta página
  items: Venta[]
}

// Totales calculados por la base de datos
export interface ResumenVentas {
  // Número de ventas registradas
  cantidad_ventas: number
  // Suma de cantidad * precio de todas las ventas, como texto
  ingresos: string
}
