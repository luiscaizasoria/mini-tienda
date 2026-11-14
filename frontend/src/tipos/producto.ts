// Forma de un producto, igual a ProductoRead en python/app/schemas/producto.py
export interface Producto {
  // Identificador único del producto
  id: number
  // Nombre del producto
  nombre: string
  // Precio como TEXTO: Pydantic envía los Decimal como "2.50", no como número
  precio: string
  // Unidades disponibles
  stock: number
}
