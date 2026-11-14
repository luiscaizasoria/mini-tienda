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

// Datos que se envían para crear un producto, igual a ProductoCreate
// en python/app/schemas/producto.py (todavía no tiene id: lo genera la BD)
export interface NuevoProducto {
  // Nombre del producto
  nombre: string
  // Precio como texto, para no perder decimales (por ejemplo "2.50")
  precio: string
  // Unidades disponibles
  stock: number
}
