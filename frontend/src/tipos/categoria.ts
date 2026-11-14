// Forma de una categoría, igual a CategoriaRead en
// python/app/schemas/categoria.py
export interface Categoria {
  // Identificador único de la categoría
  id: number
  // Nombre de la categoría
  nombre: string
}

// Datos que se envían para crear una categoría, igual a CategoriaCreate
export interface NuevaCategoria {
  // Nombre de la categoría
  nombre: string
}
